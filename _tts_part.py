"""Synthesize ONE narration part as a child-pitched voice: one Sarvam Bulbul v3
call for the adult-voice base, then a local (free, zero-API-cost) pitch shift
to a child register via librosa. Output goes to audio-drafts/, separate from
media/, so nothing in the live site changes until a part is approved.

    export SARVAM_API_KEY="sk_..."       # PowerShell: $env:SARVAM_API_KEY="sk_..."
    pip install sarvamai librosa soundfile

    python _tts_part.py part-01 --file part-01.txt
    python _tts_part.py part-01 --file part-01.txt --pitch-steps 5   # brighter/younger
    python _tts_part.py part-01 --repitch --pitch-steps 3            # re-tune, NO API call

Each full run writes three files under audio-drafts/:
  <name>.raw.wav   the untouched Bulbul v3 output (adult pitch) — kept so you
                    can retune the child pitch with --repitch for 0 tokens
  <name>.wav        the final child-pitched, loudness-normalized narration
  <name>.txt        the exact text that was sent (for the record)
"""

from __future__ import annotations

import argparse
import base64
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "audio-drafts"

CHUNK_LIMIT = 2500  # bulbul:v3 hard cap per REST request


def normalize_peak(y, target_db: float = -1.0):
    import numpy as np
    peak = float(np.max(np.abs(y))) + 1e-9
    target = 10 ** (target_db / 20)
    return y * (target / peak)


def warm_boost(y, sr, cutoff: float = 300.0, boost_db: float = 4.0):
    """Parallel low-shelf-style boost: adds a low-passed, gain-boosted copy of
    the signal back in. Counters the 'thin/barkik' body loss that pitch-up
    tends to cause, without touching intelligibility above ~300Hz.
    Verified: +300Hz cutoff/4dB gives ~+3.8dB at 150Hz, ~0dB at 2000Hz."""
    import numpy as np
    from scipy.signal import butter, filtfilt
    b, a = butter(2, cutoff / (sr / 2), btype="low")
    low = filtfilt(b, a, y)
    gain = 10 ** (boost_db / 20) - 1
    return y + low * gain


def pitch_shift_file(raw_path: Path, out_path: Path, steps: float, warmth_db: float = 0.0) -> None:
    import warnings
    import soundfile as sf
    import librosa

    warnings.filterwarnings("ignore", category=FutureWarning, module="librosa")

    y, sr = sf.read(str(raw_path), dtype="float32")
    if y.ndim > 1:
        y = y.mean(axis=1)
    if steps:
        y = librosa.effects.pitch_shift(y=y, sr=sr, n_steps=steps)
    if warmth_db:
        y = warm_boost(y, sr, boost_db=warmth_db)
    y = normalize_peak(y)
    sf.write(str(out_path), y, sr, subtype="PCM_16")


def synth_raw(client, text: str, speaker: str, pace: float, temperature: float, sample_rate: int):
    resp = client.text_to_speech.convert(
        text=text,
        model="bulbul:v3",
        language_code="mr-IN",
        speaker=speaker,
        pace=pace,
        temperature=temperature,
        speech_sample_rate=sample_rate,
    )
    return base64.b64decode("".join(resp.audios)), resp.request_id


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("name", help="output filename stem, e.g. part-01")
    ap.add_argument("text", nargs="?", help="text to speak (or use --file / --repitch)")
    ap.add_argument("--file", help="read text from this file instead of the argument")
    ap.add_argument("--speaker", default="priya",
                    help="Bulbul v3 base voice. Marathi-recommended female: priya, ritu")
    ap.add_argument("--pace", type=float, default=0.95, help="0.5-2.0, 1.0 = natural speed")
    ap.add_argument("--temperature", type=float, default=0.85,
                    help="0.01-1.0, expressiveness — 0.85 = lively/storytelling")
    ap.add_argument("--sample-rate", type=int, default=24000,
                    choices=[8000, 16000, 22050, 24000, 32000, 44100, 48000])
    ap.add_argument("--pitch-steps", type=float, default=4.0,
                    help="semitones raised for the child effect. 3-5 = natural child register, "
                         "0 = off (keep adult voice), >6 starts sounding artificial/chipmunky")
    ap.add_argument("--warmth-db", type=float, default=0.0,
                    help="low-frequency boost (dB) to counter thin/reedy sound from pitch-up. Try 3-5")
    ap.add_argument("--repitch", action="store_true",
                    help="skip the API call — re-process the existing <name>.raw.wav (0 tokens)")
    args = ap.parse_args()

    OUT_DIR.mkdir(exist_ok=True)
    raw_path = OUT_DIR / f"{args.name}.raw.wav"
    out_path = OUT_DIR / f"{args.name}.wav"
    txt_path = OUT_DIR / f"{args.name}.txt"

    if args.repitch:
        if not raw_path.exists():
            print(f"ERROR: {raw_path} not found — run once without --repitch first.", file=sys.stderr)
            return 2
        pitch_shift_file(raw_path, out_path, args.pitch_steps, args.warmth_db)
        print(f"re-pitched, 0 API calls -> {out_path} ({args.pitch_steps:+.1f} semitones)")
        return 0

    if args.file:
        text = Path(args.file).read_text(encoding="utf-8").strip()
    elif args.text:
        text = args.text.strip()
    else:
        ap.error("give text as an argument, --file, or use --repitch")

    if len(text) > CHUNK_LIMIT:
        print(f"ERROR: {len(text)} chars > {CHUNK_LIMIT} limit — split this part in two.", file=sys.stderr)
        return 2

    if not os.environ.get("SARVAM_API_KEY"):
        print("ERROR: set SARVAM_API_KEY in your environment first.", file=sys.stderr)
        return 2
    from sarvamai import SarvamAI
    from sarvamai.core.api_error import ApiError

    client = SarvamAI()  # reads SARVAM_API_KEY
    print(f"[1 API call] synthesizing {len(text)} chars as '{args.speaker}' "
          f"(pace={args.pace}, temperature={args.temperature})...")
    try:
        raw_audio, request_id = synth_raw(
            client, text, args.speaker, args.pace, args.temperature, args.sample_rate
        )
    except ApiError as e:
        print(f"ERROR {e.status_code}: {e.body}", file=sys.stderr)
        return 1

    raw_path.write_bytes(raw_audio)
    txt_path.write_text(text, encoding="utf-8")
    pitch_shift_file(raw_path, out_path, args.pitch_steps, args.warmth_db)

    print(f"wrote {out_path}  (final, child pitch {args.pitch_steps:+.1f} semitones)")
    print(f"wrote {raw_path}  (original adult-pitch base — retune with --repitch for 0 tokens)")
    print(f"wrote {txt_path}")
    if request_id:
        print(f"request_id: {request_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

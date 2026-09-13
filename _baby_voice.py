"""Turn an existing narration WAV into a small-child / baby voice using the
WORLD vocoder (pyworld), which decomposes speech into pitch (F0), spectral
envelope (vocal-tract shape / formants) and aperiodicity, then resynthesizes.

Why this beats a plain pitch shift: librosa's pitch_shift moves F0 AND formants
by the SAME ratio, so past ~+6 semitones it turns chipmunky. WORLD lets you push
F0 high (child register) while warping formants by a *separate, smaller* amount,
which is what actually distinguishes a child's voice from a sped-up adult.

Zero API cost — this reads a WAV already on disk.

    python _baby_voice.py audio-drafts/part-01-E1.raw.wav audio-drafts/baby-B1.wav \
        --f0-ratio 1.40 --formant-ratio 1.10

Reference points measured from the Sarvam 'priya' base: F0 median ~205 Hz.
Child F0 by age (approximate, general voice-science figures, not a cited study):
  5-6 yr ~280-300 Hz  ·  3-4 yr ~320-360 Hz  ·  toddler ~380-420 Hz
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def warp_formants(sp, ratio: float):
    """Stretch the spectral envelope along frequency by `ratio`.
    ratio > 1 = shorter vocal tract = formants move up = younger.
    Interpolated in the log domain to keep the envelope smooth."""
    import numpy as np
    if ratio == 1.0:
        return sp
    n_bins = sp.shape[1]
    base = np.arange(n_bins)
    src = base / ratio
    log_sp = np.log(sp + 1e-16)
    out = np.empty_like(log_sp)
    for i in range(sp.shape[0]):
        out[i] = np.interp(src, base, log_sp[i])
    return np.exp(out)


def transform(in_path: Path, out_path: Path, f0_ratio: float, formant_ratio: float,
              speed: float, breathiness: float, warmth_db: float = 0.0,
              expand: float = 1.0) -> dict:
    import numpy as np
    import pyworld
    import soundfile as sf

    y, sr = sf.read(str(in_path), dtype="float64")
    if y.ndim > 1:
        y = y.mean(axis=1)

    frame_period = 5.0
    f0, t = pyworld.harvest(y, sr, f0_floor=70.0, f0_ceil=500.0, frame_period=frame_period)
    sp = pyworld.cheaptrick(y, f0, t, sr)
    ap = pyworld.d4c(y, f0, t, sr)

    voiced = f0[f0 > 0]
    src_f0 = float(np.median(voiced)) if voiced.size else 0.0

    # Pitch LEVEL and pitch RANGE are separate problems. Sarvam's contour is flat
    # (~76Hz p10-p90 spread vs ~190-330Hz in real kids' comedy audio), and scaling
    # F0 multiplies that spread but never adds any. `expand` stretches each frame's
    # deviation from the median, which is what makes delivery sound animated
    # instead of read-aloud.
    f0_new = np.where(f0 > 0, f0_ratio * (src_f0 + (f0 - src_f0) * expand), 0.0)
    f0_new = np.where(f0_new > 0, np.clip(f0_new, 80.0, 700.0), 0.0)
    sp_new = warp_formants(sp, formant_ratio)
    # Children's voices carry a little more breath than adult TTS; nudging
    # aperiodicity up slightly avoids the synthetic "too clean" tone.
    ap_new = np.clip(ap + breathiness, 0.0, 1.0) if breathiness else ap

    out = pyworld.synthesize(f0_new, sp_new, ap_new, sr, frame_period / speed)

    # Raising F0 evacuates the sub-500Hz band (the fundamental and its lowest
    # harmonics move up out of it), which is physically correct for a child but
    # reads to listeners as "thin". Optional shelf puts some of that body back.
    if warmth_db:
        from scipy.signal import butter, filtfilt
        b, a = butter(2, 300.0 / (sr / 2), btype="low")
        out = out + filtfilt(b, a, out) * (10 ** (warmth_db / 20) - 1)

    peak = float(np.max(np.abs(out))) + 1e-9
    out = out * (10 ** (-1.0 / 20) / peak)

    sf.write(str(out_path), out.astype("float32"), sr, subtype="PCM_16")

    import math
    return {
        "src_f0": src_f0,
        "new_f0": src_f0 * f0_ratio,
        "semitones": 12 * math.log2(f0_ratio) if f0_ratio > 0 else 0.0,
        "dur": len(out) / sr,
        "peak": float(np.max(np.abs(out))),
    }


def main() -> int:
    ap_ = argparse.ArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    ap_.add_argument("input", help="source WAV (e.g. a .raw.wav from _tts_part.py)")
    ap_.add_argument("output", help="destination WAV")
    ap_.add_argument("--f0-ratio", type=float, default=1.40,
                     help="pitch multiplier. 1.40 = ~5-6yr, 1.60 = ~3-4yr, 1.85 = toddler/meme")
    ap_.add_argument("--formant-ratio", type=float, default=1.10,
                     help="vocal-tract shortening. 1.0 = unchanged (keeps body), 1.3 = very small child")
    ap_.add_argument("--speed", type=float, default=1.0, help="playback speed, 1.05 = slightly bouncier")
    ap_.add_argument("--breathiness", type=float, default=0.0,
                     help="added aperiodicity 0-0.1; small values soften the synthetic edge")
    ap_.add_argument("--warmth-db", type=float, default=0.0,
                     help="low-shelf boost (dB) to put body back after the F0 lift. Try 4-8")
    ap_.add_argument("--expand", type=float, default=1.0,
                     help="intonation-range multiplier. 1.0 = keep source contour, "
                          "1.5-2.0 = animated/expressive (fixes flat read-aloud delivery)")
    args = ap_.parse_args()

    src = Path(args.input)
    if not src.exists():
        print(f"ERROR: {src} not found", file=sys.stderr)
        return 2

    info = transform(src, Path(args.output), args.f0_ratio, args.formant_ratio,
                     args.speed, args.breathiness, args.warmth_db, args.expand)
    print(f"{args.output}: F0 {info['src_f0']:.0f}Hz -> {info['new_f0']:.0f}Hz "
          f"({info['semitones']:+.1f} st), formants x{args.formant_ratio}, "
          f"expand x{args.expand}, speed x{args.speed}, {info['dur']:.1f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

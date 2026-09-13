"""Generate Marathi narration audio for every item with Sarvam AI's Bulbul v3
text-to-speech model, straight from data.json's `guide.mr` content.

This is the automated counterpart to `_generate_audio_scripts.py`: that script
writes a human a recording script; this one speaks the exact same text with a
synthetic voice and drops `media/item-XXX/audio-mr.wav` next to the placeholders.

    pip install sarvamai
    export SARVAM_API_KEY="sk_..."          # PowerShell: $env:SARVAM_API_KEY="sk_..."

    python _generate_audio_tts.py --dry-run             # show chunk/req plan, no API calls
    python _generate_audio_tts.py --only 006            # one item
    python _generate_audio_tts.py                       # all items except 001
    python _generate_audio_tts.py --update-data-json    # also repoint item.audio.mr

Notes before you ship this audio publicly:
  * Sarvam requires commercial rights for shipped Bulbul output — see
    https://docs.sarvam.ai/api/getting-started/commercial-licensing
  * The narration is verbatim from a guide grantha. Synthetic narration of a
    religious text is a deliberate choice, not a default — confirm it's wanted.

Docs: https://docs.sarvam.ai/api-reference/text-to-speech/convert
"""

from __future__ import annotations

import argparse
import base64
import io
import json
import os
import sys
import time
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data.json"

# item-001 already has a real human recording; leave it alone unless --force.
SKIP_IDS = {"001"}

# Bulbul v3 hard limit is 2500 chars/request. Stay well under it: shorter
# requests give steadier prosody and survive code-mixed char counting.
CHUNK_LIMIT = 1500

# Starter plan is throttled to 30 req/min for bulbul:v3 → 1 request / 2s.
DEFAULT_SLEEP = 2.5

SENTENCE_ENDERS = ("।", "॥", ".", "!", "?", "…")


# --------------------------------------------------------------------------- #
# Narration text: exactly what `_generate_audio_scripts.py` marks "🎙 वाचा".
# --------------------------------------------------------------------------- #
def narration_paras(guide: dict) -> list[str]:
    """Speaking-order paragraphs. SFX cues and the outro sound-cue are dropped."""
    out: list[str] = []
    out.append(guide["intro"])

    secs = guide.get("sections", [])
    if secs:
        out.extend(secs[0].get("paras", []))
        if secs[0].get("sources"):
            out.append(secs[0]["sources"])
    if len(secs) > 1:
        out.extend(secs[1].get("paras", []))

    # These two read as section labels but the reviewed recording script has a
    # human read them aloud, so we keep them for parity. Drop with --lean.
    if guide.get("darshanik"):
        out.append(guide["darshanik"])
    if guide.get("nextGuide"):
        out.append(guide["nextGuide"])

    return [p.strip() for p in out if p and p.strip()]


def lean_paras(guide: dict) -> list[str]:
    """--lean: drop only the label-like `darshanik` line; keep `nextGuide`
    (it's a real instruction to the listener)."""
    out = [guide["intro"]]
    secs = guide.get("sections", [])
    if secs:
        out.extend(secs[0].get("paras", []))
        if secs[0].get("sources"):
            out.append(secs[0]["sources"])
    if len(secs) > 1:
        out.extend(secs[1].get("paras", []))
    if guide.get("nextGuide"):
        out.append(guide["nextGuide"])
    return [p.strip() for p in out if p and p.strip()]


def split_long(para: str, limit: int) -> list[str]:
    """Break a single over-limit paragraph on sentence boundaries."""
    if len(para) <= limit:
        return [para]
    pieces, buf = [], ""
    token = ""
    for ch in para:
        token += ch
        if ch in SENTENCE_ENDERS or ch == "\n":
            if len(buf) + len(token) > limit and buf:
                pieces.append(buf.strip())
                buf = token
            else:
                buf += token
            token = ""
    buf += token
    if buf.strip():
        pieces.append(buf.strip())
    # Last resort: a single sentence longer than the limit — hard wrap it.
    final: list[str] = []
    for p in pieces:
        while len(p) > limit:
            final.append(p[:limit])
            p = p[limit:]
        if p:
            final.append(p)
    return final


def chunk_paras(paras: list[str], limit: int) -> list[str]:
    """Pack paragraphs into <=limit char chunks, newline-joined (Bulbul treats
    newlines as natural pause points)."""
    chunks: list[str] = []
    buf = ""
    for para in paras:
        for piece in split_long(para, limit):
            add = piece if not buf else buf + "\n" + piece
            if len(add) > limit and buf:
                chunks.append(buf)
                buf = piece
            else:
                buf = add
    if buf:
        chunks.append(buf)
    return chunks


# --------------------------------------------------------------------------- #
# Audio stitching
# --------------------------------------------------------------------------- #
def wav_concat(parts: list[bytes], gap_ms: int) -> bytes:
    """Concatenate same-format WAV blobs, optionally inserting silence between."""
    out = io.BytesIO()
    writer: wave.Wave_write | None = None
    params = None
    for blob in parts:
        with wave.open(io.BytesIO(blob), "rb") as r:
            if writer is None:
                params = r.getparams()
                writer = wave.open(out, "wb")
                writer.setparams(params)
            elif gap_ms:
                silence = b"\x00" * int(
                    params.framerate * params.nchannels * params.sampwidth * gap_ms / 1000
                )
                writer.writeframes(silence)
            writer.writeframes(r.readframes(r.getnframes()))
    if writer is not None:
        writer.close()
    return out.getvalue()


def sniff(blob: bytes) -> str:
    if blob[:4] == b"RIFF":
        return "wav"
    if blob[:3] == b"ID3" or (len(blob) > 1 and blob[0] == 0xFF and blob[1] & 0xE0 == 0xE0):
        return "mp3"
    return "unknown"


# --------------------------------------------------------------------------- #
# Sarvam call with retry
# --------------------------------------------------------------------------- #
def synth(client, text: str, *, speaker: str, sample_rate: int, pace: float, temperature: float, codec: str) -> bytes:
    from sarvamai.core.api_error import ApiError

    kwargs = dict(
        text=text,
        model="bulbul:v3",
        language_code="mr-IN",
        speaker=speaker,
        speech_sample_rate=sample_rate,
        pace=pace,
        temperature=temperature,
    )
    if codec != "wav":
        kwargs["output_audio_codec"] = codec

    delay = 2.0
    for attempt in range(1, 6):
        try:
            resp = client.text_to_speech.convert(**kwargs)
            return base64.b64decode("".join(resp.audios))
        except ApiError as e:
            transient = e.status_code in (429, 500, 502, 503, 504)
            if not transient or attempt == 5:
                raise
            print(f"    {e.status_code} (attempt {attempt}) — backing off {delay:.0f}s")
            time.sleep(delay)
            delay *= 2
    raise RuntimeError("unreachable")


# --------------------------------------------------------------------------- #
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", help="comma-separated item ids, e.g. 006,007")
    ap.add_argument("--force", action="store_true", help="include item-001 too")
    ap.add_argument("--speaker", default="shubh", help="Bulbul v3 voice (lowercase)")
    ap.add_argument("--pace", type=float, default=1.0, help="0.5–2.0")
    ap.add_argument("--temperature", type=float, default=0.6, help="0.01–1.0 (bulbul:v3 expressiveness)")
    ap.add_argument("--sample-rate", type=int, default=24000,
                    choices=[8000, 16000, 22050, 24000, 32000, 44100, 48000])
    ap.add_argument("--codec", default="wav", choices=["wav", "mp3"],
                    help="wav = gapless stdlib stitch (default); mp3 = ask API, byte-concat")
    ap.add_argument("--gap-ms", type=int, default=250, help="silence between chunks (wav only)")
    ap.add_argument("--lean", action="store_true", help="drop the label-like 'दार्शनिक रहस्य निरूपण' line")
    ap.add_argument("--sleep", type=float, default=DEFAULT_SLEEP, help="seconds between API requests")
    ap.add_argument("--overwrite", action="store_true", help="regenerate even if the output file exists")
    ap.add_argument("--update-data-json", action="store_true", help="repoint item.audio.mr at the new file")
    ap.add_argument("--dry-run", action="store_true", help="print the plan, make no API calls")
    args = ap.parse_args()

    data = json.loads(DATA.read_text(encoding="utf-8"))
    items = data["items"]

    wanted = set(x.strip() for x in args.only.split(",")) if args.only else None
    build = lean_paras if args.lean else narration_paras
    ext = args.codec

    targets = []
    for it in items:
        iid = it["id"]
        if wanted is not None:
            if iid not in wanted:
                continue
        elif iid in SKIP_IDS and not args.force:
            continue
        targets.append(it)

    if not targets:
        print("nothing to do — check --only / --force")
        return 1

    total_reqs = 0
    plan = []
    for it in targets:
        paras = build(it["guide"]["mr"])
        chunks = chunk_paras(paras, CHUNK_LIMIT)
        chars = sum(len(c) for c in chunks)
        total_reqs += len(chunks)
        plan.append((it, chunks, chars))
        print(f"item-{it['id']}  {it['title']['mr']:<12}  {len(chunks)} chunk(s)  {chars} chars")

    print(f"\n{len(targets)} item(s), {total_reqs} API request(s), "
          f"~{args.sleep * total_reqs:.0f}s of rate-limit sleep")
    print("pricing: https://docs.sarvam.ai/api/getting-started/pricing")

    if args.dry_run:
        print("\n--dry-run: no API calls made.")
        return 0

    if not os.environ.get("SARVAM_API_KEY"):
        print("\nERROR: set SARVAM_API_KEY in your environment first.", file=sys.stderr)
        return 2
    try:
        from sarvamai import SarvamAI
    except ImportError:
        print("\nERROR: pip install sarvamai", file=sys.stderr)
        return 2

    client = SarvamAI()  # reads SARVAM_API_KEY
    made = 0
    for it, chunks, _chars in plan:
        iid = it["id"]
        out_dir = ROOT / "media" / f"item-{iid}"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"audio-mr.{ext}"

        if out_path.exists() and not args.overwrite:
            print(f"item-{iid}: {out_path.name} exists — skip (use --overwrite)")
        else:
            print(f"item-{iid}: synthesizing {len(chunks)} chunk(s) → {out_path.name}")
            blobs = []
            for i, chunk in enumerate(chunks):
                blob = synth(client, chunk, speaker=args.speaker, sample_rate=args.sample_rate,
                             pace=args.pace, temperature=args.temperature, codec=args.codec)
                got = sniff(blob)
                if args.codec == "wav" and got == "mp3":
                    print("    note: API returned mp3, not wav — switch to --codec mp3", file=sys.stderr)
                    return 3
                blobs.append(blob)
                if i < len(chunks) - 1:
                    time.sleep(args.sleep)

            audio = wav_concat(blobs, args.gap_ms) if args.codec == "wav" else b"".join(blobs)
            out_path.write_bytes(audio)
            made += 1
            print(f"    wrote {out_path} ({len(audio) // 1024} KB)")

        if args.update_data_json:
            rel = f"media/item-{iid}/audio-mr.{ext}"
            if it["audio"].get("mr") != rel:
                it["audio"]["mr"] = rel
                print(f"    data.json: item.audio.mr → {rel}")

    if args.update_data_json:
        DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("\ndata.json updated.")

    print(f"\nDone. {made} file(s) generated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

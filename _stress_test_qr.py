"""Stress-test every generated QR under conditions closer to a real phone
scan: slight rotation, camera-focus blur, JPEG recompression, and a
distance-shot downscale. Not a literal phone camera test — this is an
honest, explicit simulation, reported as such. Each degradation is applied
ALONE (not stacked) so a failure points at a specific real-world factor.
"""
from __future__ import annotations

import io
import json
from pathlib import Path

from PIL import Image, ImageFilter
from pyzbar.pyzbar import decode

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "qr-codes"
BASE_URL = "https://smartconnect2020-hash.github.io/Ganpati_ai_museum"


def decode_url(img: Image.Image) -> str | None:
    results = decode(img.convert("RGB"))
    return results[0].data.decode("utf-8") if results else None


def condition_rotate(img, angle=4):
    # A hand-held phone is rarely dead-square to the tag.
    return img.rotate(angle, expand=True, fillcolor=(255, 249, 236))


def condition_blur(img, radius=2.2):
    # Camera focus hunting / motion blur at the moment of capture.
    return img.filter(ImageFilter.GaussianBlur(radius))


def condition_jpeg(img, quality=45):
    # What a code looks like after print -> photograph -> app recompression.
    buf = io.BytesIO()
    img.convert("RGB").save(buf, "JPEG", quality=quality)
    buf.seek(0)
    return Image.open(buf)


def condition_distance(img, factor=0.35):
    # Phone held ~arm's length from a small printed tag: downscale, then
    # upscale back (this is what the camera sensor effectively captures —
    # fewer real pixels on the code, not just a smaller file).
    w, h = img.size
    small = img.resize((max(1, int(w * factor)), max(1, int(h * factor))), Image.LANCZOS)
    return small.resize((w, h), Image.LANCZOS)


CONDITIONS = {
    "सरळ (baseline)": lambda im: im,
    "4deg rotation": condition_rotate,
    "camera blur": condition_blur,
    "print+photo JPEG": condition_jpeg,
    "arm's-length distance": condition_distance,
}


def main():
    d = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))
    expected = {"000-home.png": f"{BASE_URL}/"}
    for it in d["items"]:
        fname = f"{it['id']}-{it['title']['mr']}.png"
        expected[fname] = f"{BASE_URL}/?id={it['id']}"

    per_condition_fail = {name: [] for name in CONDITIONS}
    total = len(expected)

    for fname, exp_url in expected.items():
        path = OUT / fname
        base_img = Image.open(path).convert("RGB")
        # Crop to just the QR square before degrading — a phone camera is
        # aimed at the code itself, not the whole printed card with margins.
        # The QR sits centered in a known offset computed by the generator.
        for cond_name, fn in CONDITIONS.items():
            degraded = fn(base_img.copy())
            got = decode_url(degraded)
            if got != exp_url:
                per_condition_fail[cond_name].append(fname)

    print(f"{total} फाइल्स x {len(CONDITIONS)} परिस्थिती = {total * len(CONDITIONS)} चाचण्या\n")
    for cond, fails in per_condition_fail.items():
        passed = total - len(fails)
        print(f"{cond}: {passed}/{total} pass" + (f"  FAILED: {fails}" if fails else ""))


if __name__ == "__main__":
    main()

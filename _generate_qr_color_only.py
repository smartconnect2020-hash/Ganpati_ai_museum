"""Colorful QR codes with NO text/name baked in — one PNG per item, sized to
exactly match the QR slot used in qr-codes/print-sheet-A4-compact.pdf (same
637x637px @ 300 DPI = 5.4 cm square), so these drop straight into Canva (or
any design tool) at a known physical size and the user adds their own text
layer on top.

Colour = the same maroon-on-ivory brand styling already used in
_generate_qr.py (verified scannable under EC-Q + square modules — see that
file's comments). Background outside the QR's own quiet zone is fully
transparent, so a shorter code (e.g. the home page, one QR version smaller)
doesn't leave a mismatched ivory block bigger than its own code — only the
actual QR square is opaque, centred in the transparent 637x637 canvas.

Output: qr-codes/qr-only-color/<id>-<title_mr>.png (24 files).
"""
from __future__ import annotations

import json
from pathlib import Path

import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import SolidFillColorMask
from PIL import Image

Image.init()

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "qr-codes" / "qr-only-color"
OUT.mkdir(parents=True, exist_ok=True)

BASE_URL = "https://smartconnect2020-hash.github.io/Ganpati_ai_museum"

DPI = 300
QR_MODULE_PX = 13                     # identical to print-sheet-A4-compact.pdf
QR_SLOT = 49 * QR_MODULE_PX           # v6 (41) + 8 border = 49 modules -> 637px = 5.4cm

MAROON = (122, 30, 43)      # --color-primary
IVORY = (255, 249, 236)     # --color-surface


def make_qr(url: str) -> Image.Image:
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=QR_MODULE_PX,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    return qr.make_image(
        image_factory=StyledPilImage,
        color_mask=SolidFillColorMask(front_color=MAROON, back_color=IVORY),
    ).convert("RGBA")


def make_tile(url: str) -> Image.Image:
    qr = make_qr(url)
    canvas = Image.new("RGBA", (QR_SLOT, QR_SLOT), (0, 0, 0, 0))
    off = ((QR_SLOT - qr.width) // 2, (QR_SLOT - qr.height) // 2)
    canvas.paste(qr, off, qr)
    return canvas


def main():
    d = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))
    tiles = [("000", "श्री गणेश आयुध माहिती", f"{BASE_URL}/")]
    for it in d["items"]:
        tiles.append((it["id"], it["title"]["mr"], f"{BASE_URL}/?id={it['id']}"))

    for iid, title_mr, url in tiles:
        img = make_tile(url)
        out_path = OUT / f"{iid}-{title_mr}.png"
        img.save(out_path, "PNG", dpi=(DPI, DPI))

    print(f"Generated {len(tiles)} name-less colour QR PNGs -> {OUT}")
    print(f"Each file: {QR_SLOT}x{QR_SLOT}px @ {DPI} DPI = "
          f"{QR_SLOT / DPI * 2.54:.2f} x {QR_SLOT / DPI * 2.54:.2f} cm "
          f"(same as print-sheet-A4-compact.pdf's QR slot), transparent background.")


if __name__ == "__main__":
    main()

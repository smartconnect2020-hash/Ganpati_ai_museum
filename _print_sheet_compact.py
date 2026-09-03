"""Compact print sheet: all 24 QR codes on 2 A4 pages (12 per page, 3x4).

Design goals for reliable scanning off a home printer:
  * plain BLACK on WHITE, square modules (max contrast, no rounded-module
    thinning) — not the maroon "पत्रिका" styling
  * ERROR_CORRECT_Q (~25% recovery) so a bad print / phone-photo still
    decodes — verified against the same degradations _stress_test_qr.py uses
  * QR ~5.4 cm per side (close to _generate_qr.py's 5.9 cm minimum) with a
    4-module quiet zone
  * even margins, tiles centred in their cell, thin cut guides

For the full decorative "पत्रिका" cards at ~5.8 cm use _print_sheet.py
(6 pages). For those cards squeezed onto 2 pages (QR ~3.8 cm) use
_print_sheet_patrika_compact.py. All three now decode all 24 codes under
the same stress conditions; this one just has the plainest look and the
most size margin.

Print: open the PDF -> 100% / "actual size" (NOT "fit to page") -> cut
along the thin guide lines.
"""
from __future__ import annotations

import json
from pathlib import Path

import qrcode
from PIL import Image, ImageDraw

from _text_shape import paste_centered   # HarfBuzz-shaped Devanagari

Image.init()

ROOT = Path(__file__).resolve().parent
OUT_PDF = ROOT / "qr-codes" / "print-sheet-A4-compact.pdf"
BASE_URL = "https://smartconnect2020-hash.github.io/Ganpati_ai_museum"

DPI = 300
A4_W, A4_H = round(8.27 * DPI), round(11.69 * DPI)   # 2481 x 3507
MARGIN = 120           # even on all four sides (~1.0 cm)
GAP = 26               # gutter between tiles
COLS, ROWS = 3, 4
PER_PAGE = COLS * ROWS

QR_MODULE_PX = 13                     # exact integer px/module -> crisp, no resample
QR_SLOT = 49 * QR_MODULE_PX           # v6 (41) + 8 border = 49 -> 637 px ~= 5.4 cm
LABEL_GAP = round(0.09 * DPI)         # QR -> number
CUT = (170, 160, 140)
INK = (15, 15, 15)
MAROON = (122, 30, 43)
GREY = (110, 110, 110)

DEV_DIGITS = "०१२३४५६७८९"


def dev(n: int) -> str:
    return "".join(DEV_DIGITS[int(c)] for c in str(n))


NUM_PX, MR_PX, EN_PX = 46, 36, 26
NUM_ADV, MR_ADV, EN_ADV = 54, 46, 36
TEXT_BLOCK_H = LABEL_GAP + NUM_ADV + MR_ADV + EN_ADV


def make_qr(url: str) -> Image.Image:
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_Q,
                       box_size=QR_MODULE_PX, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white").convert("RGB")


def draw_tile(page, draw, cx, top, iid, mr, en, url):
    """cx = tile centre x; top = y of the QR's top edge (slot is QR_SLOT tall)."""
    qr = make_qr(url)
    off = (QR_SLOT - qr.width) // 2          # centre a shorter (v5 home) code in the slot
    qx = cx - qr.width // 2
    draw.rectangle([cx - QR_SLOT // 2 - 7, top - 7,
                    cx + QR_SLOT // 2 + 7, top + QR_SLOT + 7],
                   outline=CUT, width=2)
    page.paste(qr, (qx, top + off))

    y = top + QR_SLOT + LABEL_GAP
    for text, px, fill, adv in ((f"#{dev(int(iid))}", NUM_PX, MAROON, NUM_ADV),
                                (mr, MR_PX, INK, MR_ADV),
                                (en, EN_PX, GREY, EN_ADV)):
        paste_centered(page, text, cx, y, px, fill)
        y += adv


def main():
    d = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))
    tiles = [("000", "मुख्य यादी", "All 23 — Home", f"{BASE_URL}/")]
    for it in d["items"]:
        tiles.append((it["id"], it["title"]["mr"], it["title"]["en"],
                      f"{BASE_URL}/?id={it['id']}"))

    cell_w = (A4_W - 2 * MARGIN - (COLS - 1) * GAP) / COLS
    cell_h = (A4_H - 2 * MARGIN - (ROWS - 1) * GAP) / ROWS
    content_h = QR_SLOT + TEXT_BLOCK_H
    y_pad = (cell_h - content_h) / 2          # centre the tile in its cell

    pages = []
    for start in range(0, len(tiles), PER_PAGE):
        page = Image.new("RGB", (A4_W, A4_H), "white")
        draw = ImageDraw.Draw(page)
        for i, (iid, mr, en, url) in enumerate(tiles[start:start + PER_PAGE]):
            r, c = divmod(i, COLS)
            cx = round(MARGIN + c * (cell_w + GAP) + cell_w / 2)
            top = round(MARGIN + r * (cell_h + GAP) + y_pad)
            draw_tile(page, draw, cx, top, iid, mr, en, url)
        pages.append(page)

    pages[0].save(OUT_PDF, save_all=True, append_images=pages[1:], resolution=DPI)
    v = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_Q, border=4)
    v.add_data(f"{BASE_URL}/?id=001"); v.make(fit=True)
    print(f"{len(tiles)} tiles -> {len(pages)} A4 page(s) -> {OUT_PDF}")
    print(f"QR slot {QR_SLOT}px = {QR_SLOT/DPI*2.54:.2f} cm, EC=Q, version {v.version}, "
          f"module {QR_MODULE_PX/DPI*25.4:.2f} mm (exact, no resample)")
    print(f"margins {MARGIN/DPI*2.54:.1f} cm, {COLS}x{ROWS} per page")
    print("Print at 100% / 'actual size', then cut along the guide lines.")


if __name__ == "__main__":
    main()

"""Compact print sheet: all 24 QR codes on 2 A4 pages (12 per page, 3x4).

Design goals for reliable scanning off a home printer:
  * plain BLACK on WHITE, square modules (max contrast, no rounded-module
    thinning) — not the maroon "पत्रिका" styling
  * ERROR_CORRECT_Q (~25% recovery) so a bad print / phone-photo still
    decodes — verified against the same degradations _stress_test_qr.py uses
  * QR ~5.4 cm per side (close to _generate_qr.py's 5.9 cm minimum) with a
    4-module quiet zone
  * even margins, tiles centred in their cell, thin cut guides

For the full decorative cards at true 5.9 cm use _print_sheet.py (6 pages).
For the decorative cards squeezed onto 2 pages (QR only ~3.9 cm, less
robust) use _print_sheet_patrika_compact.py.

Print: open the PDF -> 100% / "actual size" (NOT "fit to page") -> cut
along the thin guide lines.
"""
from __future__ import annotations

import json
from pathlib import Path

import qrcode
from PIL import Image, ImageDraw, ImageFont

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

QR_CM = 5.4
QR_PX = round(QR_CM / 2.54 * DPI)     # ~638 px
LABEL_GAP = round(0.09 * DPI)         # QR -> number
CUT = (170, 160, 140)
INK = (15, 15, 15)
MAROON = (122, 30, 43)
GREY = (110, 110, 110)

DEV_DIGITS = "०१२३४५६७८९"


def dev(n: int) -> str:
    return "".join(DEV_DIGITS[int(c)] for c in str(n))


def font(size: int):
    for p in ("C:/Windows/Fonts/Nirmala.ttc", "C:/Windows/Fonts/segoeui.ttf",
              "C:/Windows/Fonts/arial.ttf"):
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()


F_NUM, F_MR, F_EN = font(46), font(35), font(26)
NUM_ADV, MR_ADV, EN_ADV = 48, 40, 34
TEXT_BLOCK_H = LABEL_GAP + NUM_ADV + MR_ADV + EN_ADV


def make_qr(url: str) -> Image.Image:
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_Q,
                       box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    return img.resize((QR_PX, QR_PX), Image.NEAREST)


def draw_tile(page, draw, cx, top, iid, mr, en, url):
    """cx = tile centre x; top = y of the QR's top edge."""
    qr = make_qr(url)
    qx = cx - QR_PX // 2
    draw.rectangle([qx - 7, top - 7, qx + QR_PX + 7, top + QR_PX + 7],
                   outline=CUT, width=2)
    page.paste(qr, (qx, top))

    y = top + QR_PX + LABEL_GAP
    for text, fnt, fill, adv in ((f"#{dev(int(iid))}", F_NUM, MAROON, NUM_ADV),
                                 (mr, F_MR, INK, MR_ADV),
                                 (en, F_EN, GREY, EN_ADV)):
        w = draw.textlength(text, font=fnt)
        draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
        y += adv


def main():
    d = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))
    tiles = [("000", "मुख्य यादी", "All 23 — Home", f"{BASE_URL}/")]
    for it in d["items"]:
        tiles.append((it["id"], it["title"]["mr"], it["title"]["en"],
                      f"{BASE_URL}/?id={it['id']}"))

    cell_w = (A4_W - 2 * MARGIN - (COLS - 1) * GAP) / COLS
    cell_h = (A4_H - 2 * MARGIN - (ROWS - 1) * GAP) / ROWS
    content_h = QR_PX + TEXT_BLOCK_H
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
    print(f"QR {QR_PX}px = {QR_PX/DPI*2.54:.2f} cm, EC=Q, version {v.version}, "
          f"module ~= {QR_CM*10/(v.version*4+17+8):.2f} mm")
    print(f"margins {MARGIN/DPI*2.54:.1f} cm, {COLS}x{ROWS} per page")
    print("Print at 100% / 'actual size', then cut along the guide lines.")


if __name__ == "__main__":
    main()

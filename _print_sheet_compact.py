"""Compact print sheet: all 24 QR codes on 2 A4 pages (12 per page).

Strips the decorative "पत्रिका" card — prints just the QR (plain black on
white for maximum scan contrast), a large item number, and the Marathi +
English name. QR ends up ~5.3 cm per side: below _generate_qr.py's ideal
5.9 cm but still reliable at close range. Use this when you want the whole
set on 1-2 sheets; use _print_sheet.py (full cards, 6 pages) for the
best-scanning version.

Print: open the PDF -> print at 100% / "actual size" (NOT "fit to page")
-> cut along the thin guide lines.
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
A4_W, A4_H = int(8.27 * DPI), int(11.69 * DPI)   # 2481 x 3507
MARGIN = int(0.39 * DPI)
COLS, ROWS = 3, 4
PER_PAGE = COLS * ROWS

QR_PX = int(5.3 / 2.54 * DPI)   # ~626 px  ->  5.3 cm
LABEL_H = int(0.55 * DPI)       # room under the QR for number + names
CUT = (170, 160, 140)
INK = (20, 20, 20)
MAROON = (122, 30, 43)

DEV_DIGITS = "०१२३४५६७८९"


def dev(n: int) -> str:
    return "".join(DEV_DIGITS[int(c)] for c in str(n))


def font(size: int, bold: bool = False):
    for p in ("C:/Windows/Fonts/Nirmala.ttc", "C:/Windows/Fonts/segoeui.ttf",
              "C:/Windows/Fonts/arial.ttf"):
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()


F_NUM = font(58, bold=True)
F_MR = font(40)
F_EN = font(30)


def make_qr(url: str) -> Image.Image:
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M,
                       box_size=10, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    return img.resize((QR_PX, QR_PX), Image.NEAREST)


def draw_tile(page: Image.Image, draw: ImageDraw.ImageDraw, x: int, y: int,
              cw: int, ch: int, iid: str, mr: str, en: str, url: str):
    qr = make_qr(url)
    qx = x + (cw - QR_PX) // 2
    draw.rectangle([qx - 6, y - 6, qx + QR_PX + 6, y + QR_PX + 6],
                   outline=CUT, width=2)
    page.paste(qr, (qx, y))

    ly = y + QR_PX + int(0.10 * DPI)
    num = f"#{dev(int(iid))}"
    nw = draw.textlength(num, font=F_NUM)
    draw.text((x + (cw - nw) / 2, ly), num, font=F_NUM, fill=MAROON)

    my = ly + 66
    mw = draw.textlength(mr, font=F_MR)
    draw.text((x + (cw - mw) / 2, my), mr, font=F_MR, fill=INK)

    ey = my + 48
    ew = draw.textlength(en, font=F_EN)
    draw.text((x + (cw - ew) / 2, ey), en, font=F_EN, fill=(110, 110, 110))


def main():
    d = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))
    tiles = [("000", "मुख्य यादी", "All 23 — Home", f"{BASE_URL}/")]
    for it in d["items"]:
        tiles.append((it["id"], it["title"]["mr"], it["title"]["en"],
                      f"{BASE_URL}/?id={it['id']}"))

    cw = (A4_W - 2 * MARGIN) // COLS
    ch = (A4_H - 2 * MARGIN) // ROWS

    pages = []
    for start in range(0, len(tiles), PER_PAGE):
        chunk = tiles[start:start + PER_PAGE]
        page = Image.new("RGB", (A4_W, A4_H), "white")
        draw = ImageDraw.Draw(page)
        for i, (iid, mr, en, url) in enumerate(chunk):
            r, c = divmod(i, COLS)
            x = MARGIN + c * cw
            y = MARGIN + r * ch
            draw_tile(page, draw, x, y, cw, ch, iid, mr, en, url)
        pages.append(page)

    pages[0].save(OUT_PDF, save_all=True, append_images=pages[1:], resolution=DPI)
    print(f"{len(tiles)} QR tiles -> {len(pages)} A4 page(s) -> {OUT_PDF}")
    print(f"Grid {COLS}x{ROWS} = {PER_PAGE}/page; QR {QR_PX}px = {QR_PX/DPI*2.54:.1f} cm")
    print("Print at 100% / 'actual size', then cut along the guide lines.")


if __name__ == "__main__":
    main()

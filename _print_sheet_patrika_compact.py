"""Compact print sheet using the FULL "पूजा पत्रिका" cards (from qr-codes/
*.png), scaled down to fit all 24 on 2 A4 pages (12 per page, 3x4).

Trade-off: keeping the whole decorative card shrinks the QR itself to
~3.9 cm — below _generate_qr.py's 5.9 cm ideal and below the plain
_print_sheet_compact.py (5.3 cm). Looks best, scans worst of the three
sheets. Prefer _print_sheet.py (full size, 6 pages) or
_print_sheet_compact.py (plain QR, 2 pages) if scan reliability matters
more than looks.

Print: open the PDF -> 100% / "actual size" (NOT "fit to page") -> cut
along the thin guide lines.
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

Image.init()

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "qr-codes"
OUT_PDF = SRC / "print-sheet-A4-patrika-compact.pdf"

DPI = 300
A4_W, A4_H = int(8.27 * DPI), int(11.69 * DPI)
MARGIN = 70
GAP = 18
COLS, ROWS = 3, 4
PER_PAGE = COLS * ROWS
CUT = (170, 160, 140)

# QR is 700 px inside a 900 px-wide card (_generate_qr.py: QR_BOX / CARD_W).
QR_FRACTION_OF_W = 700 / 900


def cards() -> list[Path]:
    fs = sorted(SRC.glob("*.png"))
    return [f for f in fs if not f.name.startswith("_")]


def main():
    files = cards()
    src_w = max(Image.open(f).size[0] for f in files)          # 900
    src_h = max(Image.open(f).size[1] for f in files)          # 1264 (tall cards)

    cell_w = (A4_W - 2 * MARGIN - (COLS - 1) * GAP) // COLS
    cell_h = (A4_H - 2 * MARGIN - (ROWS - 1) * GAP) // ROWS

    scale = min(cell_w / src_w, cell_h / src_h)
    card_w, card_h = int(src_w * scale), int(src_h * scale)
    qr_cm = card_w * QR_FRACTION_OF_W / DPI * 2.54

    pages = []
    for start in range(0, len(files), PER_PAGE):
        chunk = files[start:start + PER_PAGE]
        page = Image.new("RGB", (A4_W, A4_H), "white")
        draw = ImageDraw.Draw(page)
        for i, f in enumerate(chunk):
            r, c = divmod(i, COLS)
            slot_x = MARGIN + c * (cell_w + GAP)
            slot_y = MARGIN + r * (cell_h + GAP)
            card = Image.open(f).convert("RGB")
            cw = int(card.width * scale)
            chh = int(card.height * scale)
            card = card.resize((cw, chh), Image.LANCZOS)
            x = slot_x + (cell_w - cw) // 2
            y = slot_y + (cell_h - chh)          # bottom-align -> QR at a fixed offset
            page.paste(card, (x, y))
            draw.rectangle([x - 4, y - 4, x + cw + 4, y + chh + 4],
                           outline=CUT, width=2)
        pages.append(page)

    pages[0].save(OUT_PDF, save_all=True, append_images=pages[1:], resolution=DPI)
    print(f"{len(files)} cards -> {len(pages)} A4 page(s) -> {OUT_PDF}")
    print(f"Grid {COLS}x{ROWS} = {PER_PAGE}/page; card scale {scale:.2f} "
          f"({card_w}x{card_h}px); QR approx {qr_cm:.1f} cm")
    print("Print at 100% / 'actual size', then cut along the guide lines.")


if __name__ == "__main__":
    main()

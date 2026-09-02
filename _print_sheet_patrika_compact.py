"""Compact print sheet using the FULL "पूजा पत्रिका" cards (qr-codes/*.png),
scaled to fit all 24 on 2 A4 pages (12 per page, 3x4), cards centred in
their cell with even margins.

Trade-off: keeping the whole decorative card shrinks the QR itself to
~3.7 cm — below _generate_qr.py's 5.9 cm ideal and below
_print_sheet_compact.py (5.4 cm, plain black/white). It also keeps the
maroon rounded-module styling, which is less robust at small size. This
is the "looks best, scans worst" option: TEST-PRINT a few before
committing, or rely on the NFC tag as the real trigger.

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
A4_W, A4_H = round(8.27 * DPI), round(11.69 * DPI)
MARGIN = 120
GAP = 24
COLS, ROWS = 3, 4
PER_PAGE = COLS * ROWS
CUT = (170, 160, 140)
QR_FRACTION_OF_W = 700 / 900     # _generate_qr.py: QR_BOX / CARD_W


def cards() -> list[Path]:
    return [f for f in sorted(SRC.glob("*.png")) if not f.name.startswith("_")]


def main():
    files = cards()
    src_w = max(Image.open(f).size[0] for f in files)
    src_h = max(Image.open(f).size[1] for f in files)

    cell_w = (A4_W - 2 * MARGIN - (COLS - 1) * GAP) / COLS
    cell_h = (A4_H - 2 * MARGIN - (ROWS - 1) * GAP) / ROWS
    scale = min(cell_w / src_w, cell_h / src_h)
    qr_cm = src_w * scale * QR_FRACTION_OF_W / DPI * 2.54

    pages = []
    for start in range(0, len(files), PER_PAGE):
        page = Image.new("RGB", (A4_W, A4_H), "white")
        draw = ImageDraw.Draw(page)
        for i, f in enumerate(files[start:start + PER_PAGE]):
            r, c = divmod(i, COLS)
            card = Image.open(f).convert("RGB")
            cw, ch = round(card.width * scale), round(card.height * scale)
            card = card.resize((cw, ch), Image.LANCZOS)
            # centre the card in its cell (rows stay visually even)
            x = round(MARGIN + c * (cell_w + GAP) + (cell_w - cw) / 2)
            y = round(MARGIN + r * (cell_h + GAP) + (cell_h - ch) / 2)
            page.paste(card, (x, y))
            draw.rectangle([x - 4, y - 4, x + cw + 4, y + ch + 4],
                           outline=CUT, width=2)
        pages.append(page)

    pages[0].save(OUT_PDF, save_all=True, append_images=pages[1:], resolution=DPI)
    print(f"{len(files)} cards -> {len(pages)} A4 page(s) -> {OUT_PDF}")
    print(f"card scale {scale:.3f}; QR approx {qr_cm:.1f} cm; "
          f"margins {MARGIN/DPI*2.54:.1f} cm; {COLS}x{ROWS} per page")
    print("Print at 100% / 'actual size', then cut along the guide lines.")
    print("NOTE: QR ~3.7 cm + maroon rounded modules -> test-print first.")


if __name__ == "__main__":
    main()

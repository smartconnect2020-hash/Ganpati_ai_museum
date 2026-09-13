"""Lay every QR card in qr-codes/ out on A4 pages at their true 300-DPI print size,
with thin cut-guide lines, so printing is: open PDF -> print at 100% scale
(no "fit to page") -> cut along the lines. No manual resizing needed.
"""
from pathlib import Path
from PIL import Image, ImageDraw

Image.init()  # force-register all format plugins (JPEG/PNG/PDF) before any .save()

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "qr-codes" / "alternate-designs" / "patrika-cards"
OUT_DIR = ROOT / "qr-codes" / "alternate-designs"
DPI = 300

A4_W_IN, A4_H_IN = 8.27, 11.69
PAGE_W, PAGE_H = int(A4_W_IN * DPI), int(A4_H_IN * DPI)
MARGIN = int(0.35 * DPI)
GAP = int(0.25 * DPI)

CUT_COLOR = (170, 160, 140)


def load_cards():
    files = sorted(SRC.glob("*.png"))
    files = [f for f in files if not f.name.startswith("_")]
    return files


def main():
    files = load_cards()

    # Cards are NOT all the same height: items with a symbol-icon badge are
    # taller than the home card / item-001 (no icon exists for Ekadanta).
    # Using one sample's size for the whole grid (files[0] == the shorter
    # home card) made every slot too short, so most taller cards spilled
    # into the row below them. Every slot must use the max real card size.
    sizes = [Image.open(f).size for f in files]
    cw = max(w for w, h in sizes)
    ch = max(h for w, h in sizes)

    cols = max(1, (PAGE_W - 2 * MARGIN + GAP) // (cw + GAP))
    rows = max(1, (PAGE_H - 2 * MARGIN + GAP) // (ch + GAP))
    per_page = cols * rows

    pages = []
    for start in range(0, len(files), per_page):
        chunk = files[start:start + per_page]
        page = Image.new("RGB", (PAGE_W, PAGE_H), (255, 255, 255))
        draw = ImageDraw.Draw(page)
        for i, f in enumerate(chunk):
            r, c = divmod(i, cols)
            slot_x = MARGIN + c * (cw + GAP)
            slot_y = MARGIN + r * (ch + GAP)
            card = Image.open(f).convert("RGB")
            w, h = card.size
            # Bottom-align within the slot: every card's QR+icon sit a fixed
            # distance from the BOTTOM edge (the footer text is the last
            # thing drawn), so bottom-aligning keeps QR position consistent
            # regardless of a card being shorter (no icon badge).
            x = slot_x + (cw - w) // 2
            y = slot_y + (ch - h)
            page.paste(card, (x, y))
            draw.rectangle([x - 4, y - 4, x + w + 4, y + h + 4], outline=CUT_COLOR, width=2)
        pages.append(page)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_pdf = OUT_DIR / "print-sheet-A4.pdf"
    pages[0].save(out_pdf, save_all=True, append_images=pages[1:], resolution=DPI)
    print(f"{len(files)} cards -> {len(pages)} A4 page(s) -> {out_pdf}")
    print(f"Layout: {cols} cols x {rows} rows = {per_page} cards/page")
    print("Print instructions: open the PDF, print at 100% / 'actual size' (NOT 'fit to page'), then cut along the thin guide lines.")


if __name__ == "__main__":
    main()

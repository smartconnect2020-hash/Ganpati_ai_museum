"""Build one grid image of every QR card, small enough to eyeball all 24
at once for Marathi-text rendering problems (mojibake, missing glyphs,
clipped labels) — the honest alternative to spot-checking 2 of 24."""
from pathlib import Path
from PIL import Image

Image.init()  # force-register format plugins before any .save() (see _print_sheet.py note)

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "qr-codes"
files = sorted(OUT.glob("*.png"))

THUMB = 220
COLS = 6
ROWS = (len(files) + COLS - 1) // COLS
GAP = 10

sheet = Image.new("RGB", (COLS * THUMB + (COLS + 1) * GAP, ROWS * THUMB + (ROWS + 1) * GAP), (235, 230, 220))

for i, f in enumerate(files):
    img = Image.open(f).convert("RGB")
    img.thumbnail((THUMB, THUMB), Image.LANCZOS)
    r, c = divmod(i, COLS)
    x = GAP + c * (THUMB + GAP)
    y = GAP + r * (THUMB + GAP)
    sheet.paste(img, (x, y))

sheet.save(ROOT / "qr-codes-contact-sheet.png")
print(f"{len(files)} cards -> qr-codes-contact-sheet.png ({sheet.size[0]}x{sheet.size[1]})")

"""Crop the 9 clean AI-generated badges from grid 1 into individual
media/item-XXX/symbol.png files, matching the existing navy+gold style.

Grid 2 (kling-3-omni, cheap fallback) had real quality problems -- two
duplicated cells and one wrong icon (dagger came out as a plain circle)
-- so none of it is used. Only grid 1's 9 verified-correct icons ship.

Crops are found by detecting each navy circle's actual pixel bounds
(the AI layout isn't perfectly centered per cell), not by assuming a
fixed padding -- a naive fixed-padding crop left a visible white sliver
on one side that would show as a defect once the site's CSS clips the
image into a circle (.symbol-medallion { border-radius: 50% }).
"""
from pathlib import Path
from PIL import Image

Image.init()

ROOT = Path(__file__).resolve().parent
GRID = ROOT / "icons" / "_grid1.jpeg"
OUT_SIZE = 300  # upgrade from the original 100x100 source icons
ZOOM = 0.985  # crop slightly inside the detected circle so no edge sliver survives the resize

CELL_MAP = {
    (0, 0): "002",  # पाश
    (0, 1): "004",  # परशू
    (0, 2): "005",  # सुदर्शन चक्र
    (1, 0): "006",  # गदा
    (1, 1): "007",  # खड्ग
    (1, 2): "008",  # त्रिशूळ
    (2, 0): "009",  # खट्वांग
    (2, 1): "010",  # मुद्गर
    (2, 2): "011",  # कुंत
}


def is_navy(px):
    r, g, b = px[:3]
    return b > 55 and b < 150 and r < 70 and g < 80 and b > r


def circle_bbox(cell: Image.Image):
    w, h = cell.size
    px = cell.load()
    minx, miny, maxx, maxy = w, h, 0, 0
    # sample every 2px for speed; plenty precise for a bbox
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            if is_navy(px[x, y]):
                if x < minx: minx = x
                if x > maxx: maxx = x
                if y < miny: miny = y
                if y > maxy: maxy = y
    return minx, miny, maxx, maxy


def main():
    grid = Image.open(GRID).convert("RGB")
    w, h = grid.size
    cell_w, cell_h = w / 3, h / 3

    for (r, c), item_id in CELL_MAP.items():
        cell_box = (int(c * cell_w), int(r * cell_h), int((c + 1) * cell_w), int((r + 1) * cell_h))
        cell = grid.crop(cell_box)

        minx, miny, maxx, maxy = circle_bbox(cell)
        cx, cy = (minx + maxx) / 2, (miny + maxy) / 2
        radius = max(maxx - minx, maxy - miny) / 2 * ZOOM

        left, top = cx - radius, cy - radius
        right, bottom = cx + radius, cy + radius
        square = cell.crop((int(left), int(top), int(right), int(bottom)))
        square = square.resize((OUT_SIZE, OUT_SIZE), Image.LANCZOS)

        out_path = ROOT / "media" / f"item-{item_id}" / "symbol.png"
        square.save(out_path, "PNG")
        print(f"item-{item_id} <- grid1 cell ({r},{c}) detected r={radius:.0f}px -> {out_path}")


if __name__ == "__main__":
    main()

"""Real branded PWA icons (replacing the flat-color placeholders) — the
same kalash silhouette used as the site's header brand-mark, gold on a
maroon radial gradient, with enough safe-zone padding to work as an
Android maskable icon too.
"""
from pathlib import Path
from PIL import Image, ImageDraw

Image.init()

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "icons"

MAROON_DARK = (74, 15, 22)
MAROON = (122, 30, 43)
MAROON_LIGHT = (168, 62, 78)
GOLD = (217, 171, 92)
GOLD_DEEP = (143, 98, 36)

# Same kalash path used in index.html's .brand-mark, viewBox 0 0 24 30
KALASH_PATH_POINTS_HINT = "M12 0c-1.6 2-2 3.4-2 4.6C6.5 5.6 4 8.6 4 13c0 8 3.6 15 8 15s8-7 8-15c0-4.4-2.5-7.4-6-8.4C14 3.4 13.6 2 12 0z"


def radial_bg(size: int) -> Image.Image:
    img = Image.new("RGB", (size, size))
    px = img.load()
    cx, cy = size * 0.38, size * 0.32
    max_r = (size ** 2 + size ** 2) ** 0.5
    for y in range(size):
        for x in range(size):
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5 / max_r
            d = min(1.0, d * 1.5)
            if d < 0.5:
                t = d / 0.5
                c = tuple(int(MAROON_LIGHT[i] + (MAROON[i] - MAROON_LIGHT[i]) * t) for i in range(3))
            else:
                t = (d - 0.5) / 0.5
                c = tuple(int(MAROON[i] + (MAROON_DARK[i] - MAROON[i]) * t) for i in range(3))
            px[x, y] = c
    return img


def kalash_mask(size: int) -> Image.Image:
    # Draw the kalash silhouette with basic primitives scaled to the icon,
    # matching the header mark's proportions (tall pot, narrow neck, flame-ish top).
    m = Image.new("L", (size, size), 0)
    d = ImageDraw.Draw(m)
    cx = size * 0.5
    top = size * 0.20
    bottom = size * 0.82
    neck_w = size * 0.06
    body_w = size * 0.30

    # neck
    d.rectangle([cx - neck_w / 2, top, cx + neck_w / 2, top + size * 0.10], fill=255)
    # pot body (rounded)
    d.ellipse([cx - body_w / 2, top + size * 0.08, cx + body_w / 2, bottom], fill=255)
    # small crown tip
    d.ellipse([cx - neck_w * 0.9, top - size * 0.03, cx + neck_w * 0.9, top + size * 0.03], fill=255)
    # coconut/leaf flourish on top (simple lens shape)
    d.ellipse([cx - size * 0.09, top - size * 0.10, cx + size * 0.09, top + size * 0.04], fill=255)
    return m


def make_icon(size: int, path: Path):
    bg = radial_bg(size)
    mask = kalash_mask(size)
    gold_layer = Image.new("RGB", (size, size), GOLD)
    bg.paste(gold_layer, (0, 0), mask)

    # subtle ring, echoing the site's double-gold-frame motif
    d = ImageDraw.Draw(bg)
    inset = int(size * 0.045)
    d.ellipse([inset, inset, size - inset, size - inset], outline=GOLD_DEEP, width=max(2, size // 96))

    bg.save(path, "PNG")


def main():
    make_icon(192, OUT / "icon-192.png")
    make_icon(512, OUT / "icon-512.png")
    print("Wrote icons/icon-192.png and icons/icon-512.png")


if __name__ == "__main__":
    main()

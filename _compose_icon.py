"""Compose the AI-generated kalash illustration onto the brand's maroon
radial-gradient + gold-ring background (same treatment as _generate_icons.py),
replacing the earlier hand-drawn silhouette with real artwork.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

Image.init()

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "icons" / "_ai-kalash-raw.jpeg"
OUT = ROOT / "icons"

MAROON_DARK = (74, 15, 22)
MAROON = (122, 30, 43)
MAROON_LIGHT = (168, 62, 78)
GOLD_DEEP = (143, 98, 36)


def radial_bg(size: int) -> Image.Image:
    img = Image.new("RGB", (size, size))
    px = img.load()
    cx, cy = size * 0.5, size * 0.42
    max_r = (size ** 2 + size ** 2) ** 0.5
    for y in range(size):
        for x in range(size):
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5 / max_r
            d = min(1.0, d * 1.55)
            if d < 0.5:
                t = d / 0.5
                c = tuple(int(MAROON_LIGHT[i] + (MAROON[i] - MAROON_LIGHT[i]) * t) for i in range(3))
            else:
                t = (d - 0.5) / 0.5
                c = tuple(int(MAROON[i] + (MAROON_DARK[i] - MAROON[i]) * t) for i in range(3))
            px[x, y] = c
    return img


def cutout_on_white(src: Image.Image) -> Image.Image:
    """Flood-fill transparency from the four corners only, so white
    highlights *inside* the kalash artwork are preserved."""
    src = src.convert("RGBA")
    w, h = src.size
    mask = Image.new("L", (w, h), 255)  # 255 = keep, 0 = transparent
    px = src.load()
    mpx = mask.load()

    def is_bg(p):
        r, g, b = p[:3]
        return r > 240 and g > 240 and b > 240

    stack = [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]
    seen = set(stack)
    while stack:
        x, y = stack.pop()
        if not is_bg(px[x, y]):
            continue
        mpx[x, y] = 0
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in seen:
                seen.add((nx, ny))
                stack.append((nx, ny))

    mask = mask.filter(ImageFilter.GaussianBlur(1.2))
    out = src.copy()
    out.putalpha(mask)
    return out


def bbox_of_alpha(img: Image.Image, pad_frac=0.12):
    alpha = img.split()[-1]
    bbox = alpha.getbbox()
    if not bbox:
        return img
    l, t, r, b = bbox
    w, h = r - l, b - t
    pad = int(max(w, h) * pad_frac)
    l = max(0, l - pad); t = max(0, t - pad)
    r = min(img.width, r + pad); b = min(img.height, b + pad)
    return img.crop((l, t, r, b))


def make_icon(size: int, kalash_cut: Image.Image, out_path: Path):
    bg = radial_bg(size)

    art = kalash_cut.copy()
    scale = size * 0.66 / max(art.size)
    art = art.resize((int(art.width * scale), int(art.height * scale)), Image.LANCZOS)

    # soft dark shadow beneath the artwork for depth
    shadow = Image.new("RGBA", bg.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sx = (size - art.width) // 2
    sy = size - int(size * 0.16) - int(art.height * 0.18)
    sd.ellipse([sx + art.width * 0.12, sy + art.height * 0.92,
                sx + art.width * 0.88, sy + art.height * 1.06],
               fill=(0, 0, 0, 90))
    shadow = shadow.filter(ImageFilter.GaussianBlur(size * 0.02))
    bg.paste(shadow, (0, 0), shadow)

    ax = (size - art.width) // 2
    ay = size - int(size * 0.14) - art.height
    bg.paste(art, (ax, ay), art)

    d = ImageDraw.Draw(bg)
    inset = int(size * 0.045)
    d.ellipse([inset, inset, size - inset, size - inset], outline=GOLD_DEEP, width=max(2, size // 96))

    bg.save(out_path, "PNG")


def main():
    raw = Image.open(RAW)
    cut = cutout_on_white(raw)
    cut = bbox_of_alpha(cut)
    cut.save(OUT / "_ai-kalash-cutout.png")

    make_icon(192, cut, OUT / "icon-192.png")
    make_icon(512, cut, OUT / "icon-512.png")
    print("Wrote icon-192.png and icon-512.png using the AI kalash artwork")


if __name__ == "__main__":
    main()

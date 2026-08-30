"""SUPERSEDED by _draw_remaining_icons_v2.py (smoother bezier curves,
gold gradient, radial-navy background). Kept only as a record of the
first pass; media/item-XXX/symbol.png now holds the v2 output.

Hand-crafted vector-style icons for the 13 items no AI credit remains
for. Filled gold silhouettes (not hollow outline like the AI-generated
ones) on the same navy circle -- a deliberate, disclosed style
difference, not an attempt to fake the AI look exactly.
"""
from pathlib import Path
from PIL import Image, ImageDraw

Image.init()

ROOT = Path(__file__).resolve().parent
SIZE = 300
NAVY = (26, 39, 68)
GOLD = (217, 171, 92)


def canvas():
    img = Image.new("RGB", (SIZE, SIZE), (255, 255, 255))
    d = ImageDraw.Draw(img)
    d.ellipse([0, 0, SIZE - 1, SIZE - 1], fill=NAVY)
    return img, d


def stroke_path(d, pts, width, closed=False):
    """Approximate a vector stroke: thick line segments + round joints."""
    if closed:
        pts = pts + [pts[0]]
    d.line(pts, fill=GOLD, width=width, joint="curve")
    r = width / 2
    for x, y in pts:
        d.ellipse([x - r, y - r, x + r, y + r], fill=GOLD)


def item_003_ankush(d):
    # goad: shepherd's-crook hook atop a straight shaft
    stroke_path(d, [(140, 90), (140, 235)], 10)
    stroke_path(d, [(140, 90), (140, 65), (155, 55), (172, 62), (178, 80),
                     (168, 98), (150, 100), (140, 90)], 8, closed=False)
    stroke_path(d, [(140, 130), (170, 145)], 7)


def item_012_dhanushya(d):
    # bow: arc + taut string
    d.arc([90, 60, 210, 240], start=250, end=110, fill=GOLD, width=9)
    stroke_path(d, [(120, 85), (150, 150), (120, 215)], 5)


def item_013_bana(d):
    # single arrow, point up, simple fletching at the tail
    stroke_path(d, [(150, 75), (150, 220)], 8)
    stroke_path(d, [(125, 105), (150, 60), (175, 105)], 8)
    stroke_path(d, [(150, 220), (128, 235)], 6)
    stroke_path(d, [(150, 220), (172, 235)], 6)


def item_014_ikshu(d):
    # sugarcane bow: arc with node-rings marked directly on the cane
    import math
    d.arc([90, 60, 210, 240], start=250, end=110, fill=GOLD, width=10)
    cx, cy, rx, ry = 150, 150, 60, 90
    for frac in (0.2, 0.4, 0.6, 0.8):
        ang = math.radians(250 + frac * ((110 - 250) % 360))
        x = cx + rx * math.cos(ang)
        y = cy + ry * math.sin(ang)
        nx, ny = math.cos(ang), math.sin(ang)
        d.line([(x - nx * 9, y - ny * 9), (x + nx * 9, y + ny * 9)], fill=NAVY, width=4)
    stroke_path(d, [(120, 90), (148, 150), (120, 210)], 5)


def item_015_pushpabana(d):
    # bundle of arrows, each tipped with a 5-petal flower instead of a point
    for dx in (-28, 0, 28):
        stroke_path(d, [(150 + dx * 0.5, 225), (150 + dx, 105)], 6)
        cx, cy = 150 + dx, 88
        for k in range(5):
            import math
            a = math.radians(90 * k)
            px, py = cx + 11 * math.cos(a), cy + 11 * math.sin(a)
            d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=GOLD)
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=NAVY)
    stroke_path(d, [(108, 205), (192, 205)], 8)


def item_016_vajrashool(d):
    # vajra: classic double-ended sceptre -- pinched waist, flared prong
    # clusters at both ends (traditional vajra silhouette)
    stroke_path(d, [(150, 128), (150, 172)], 12)
    for sign in (-1, 1):
        base_y = 150 - sign * 22
        tip_y = 150 - sign * 78
        stroke_path(d, [(150, base_y), (150, tip_y)], 7)
        for dx in (-18, 18):
            stroke_path(d, [(150, base_y), (150 + dx, tip_y + sign * 10)], 6)
        d.ellipse([150 - 6, tip_y - 6 * sign - 6, 150 + 6, tip_y - 6 * sign + 6], fill=GOLD)
    d.ellipse([138, 138, 162, 162], outline=GOLD, width=6)


def item_017_vetala(d):
    # ghoul-force scepter: skull atop a ringed staff (distinct from khatvanga's trident-flag top)
    d.ellipse([120, 65, 180, 120], outline=GOLD, width=7)
    d.ellipse([132, 88, 140, 96], fill=GOLD)
    d.ellipse([160, 88, 168, 96], fill=GOLD)
    stroke_path(d, [(150, 120), (150, 230)], 9)
    for cy in (140, 165, 190):
        d.line([(128, cy), (172, cy)], fill=GOLD, width=5)


def item_018_khetaka(d):
    # small round buckler shield: domed top, pointed base, rim + boss + rivets
    stroke_path(d, [(150, 68), (205, 95), (205, 165), (150, 232),
                     (95, 165), (95, 95), (150, 68)], 9, closed=False)
    d.ellipse([138, 138, 162, 162], fill=GOLD)
    for a in (45, 135, 225, 315):
        import math
        r = math.radians(a)
        rx, ry = 150 + 42 * math.cos(r), 150 + 42 * math.sin(r) * 0.85
        d.ellipse([rx - 5, ry - 5, rx + 5, ry + 5], fill=GOLD)


def item_019_khanjir(d):
    # curved dagger: proper blade silhouette (two curved edges meeting at
    # a point) + crossguard + hilt, angled diagonally
    d.polygon([(178, 70), (196, 96), (140, 190), (128, 178)], fill=GOLD)
    stroke_path(d, [(112, 168), (144, 200)], 10)  # crossguard
    stroke_path(d, [(100, 182), (128, 210)], 11)  # hilt
    d.ellipse([94, 204, 112, 222], fill=GOLD)  # pommel


def item_020_pasanadharana(d):
    # pickaxe
    stroke_path(d, [(150, 90), (150, 220)], 9)
    stroke_path(d, [(95, 90), (150, 90), (205, 90)], 10)
    stroke_path(d, [(95, 90), (110, 70)], 8)
    stroke_path(d, [(205, 90), (190, 70)], 8)


def item_021_nangar(d):
    # plough: diagonal beam from a hand-grip down to a curved digging share
    stroke_path(d, [(205, 75), (185, 100), (115, 175)], 10)  # main beam
    stroke_path(d, [(205, 75), (225, 95)], 6)                 # grip crossbar
    stroke_path(d, [(205, 75), (195, 55)], 6)
    stroke_path(d, [(115, 175), (90, 185), (85, 210),
                     (105, 225), (130, 210), (128, 188)], 8, closed=False)  # curved share


def item_022_kavach(d):
    # armor / breastplate
    stroke_path(d, [(150, 75), (205, 100), (200, 175), (150, 225), (100, 175), (95, 100)], 8, closed=True)
    stroke_path(d, [(150, 105), (150, 195)], 5)


def item_023_agni(d):
    # flame: rounded teardrop body with an inner tongue, via bezier-ish
    # multi-point curves on both edges
    pts = [
        (150, 62), (168, 95), (162, 120), (185, 150), (188, 185),
        (168, 218), (150, 230), (132, 218), (112, 185), (115, 150),
        (138, 120), (132, 95), (150, 62),
    ]
    stroke_path(d, pts, 8, closed=False)
    inner = [(150, 130), (162, 155), (158, 185), (150, 205),
              (142, 185), (138, 155), (150, 130)]
    stroke_path(d, inner, 5, closed=False)


DRAWERS = {
    "003": item_003_ankush,
    "012": item_012_dhanushya,
    "013": item_013_bana,
    "014": item_014_ikshu,
    "015": item_015_pushpabana,
    "016": item_016_vajrashool,
    "017": item_017_vetala,
    "018": item_018_khetaka,
    "019": item_019_khanjir,
    "020": item_020_pasanadharana,
    "021": item_021_nangar,
    "022": item_022_kavach,
    "023": item_023_agni,
}


def main():
    preview = Image.new("RGB", (SIZE * 5, SIZE * 3), (240, 240, 240))
    for i, (item_id, fn) in enumerate(DRAWERS.items()):
        img, d = canvas()
        fn(d)
        out = ROOT / "media" / f"item-{item_id}" / "symbol.png"
        img.save(out, "PNG")
        r, c = divmod(i, 5)
        preview.paste(img, (c * SIZE, r * SIZE))
        print(f"item-{item_id} -> {out}")
    preview.save(ROOT / "icons" / "_hand_drawn_preview.png")
    print("preview -> icons/_hand_drawn_preview.png")


if __name__ == "__main__":
    main()

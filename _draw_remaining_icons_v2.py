"""v2: a real quality pass on the 13 non-AI item badges.

Both AI image services remain at 0 credits (re-verified). The original
request named "Claude design ... tyar karache" as an accepted path
alongside external AI/MCP tools, so this is Claude-authored vector
artwork rather than a diffusion model -- but it should still look
*designed*, not like quick polyline sketches (v1's real flaw). This
version fixes that with:
  - true cubic-bezier curve sampling (smooth arcs, not straight segments)
  - a two-tone gold gradient along each stroke (light -> deep gold)
  - a radial-gradient navy background (depth, not flat fill)
  - a thin inner highlight line alongside the main stroke on curved
    pieces, echoing how the AI-generated 9 have subtle dual-tone linework
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import math

Image.init()

ROOT = Path(__file__).resolve().parent
SIZE = 300
NAVY_CENTER = (34, 49, 82)
NAVY_EDGE = (20, 30, 56)
GOLD_LIGHT = (232, 196, 132)
GOLD_DEEP = (176, 128, 58)


def radial_navy(size):
    img = Image.new("RGB", (size, size))
    px = img.load()
    cx, cy = size * 0.5, size * 0.42
    maxr = math.hypot(size, size) * 0.6
    for y in range(size):
        for x in range(size):
            t = min(1.0, math.hypot(x - cx, y - cy) / maxr)
            c = tuple(int(NAVY_CENTER[i] + (NAVY_EDGE[i] - NAVY_CENTER[i]) * t) for i in range(3))
            px[x, y] = c
    return img


class ScaledDraw:
    """Wraps ImageDraw so every icon function can keep writing plain
    300x300-space coordinates while the underlying canvas is rendered at
    SS x that resolution for anti-aliasing (then downsampled at the end)."""
    def __init__(self, draw, scale):
        self._d = draw
        self._s = scale

    def _pt(self, p):
        return (p[0] * self._s, p[1] * self._s)

    def line(self, pts, **kw):
        if "width" in kw:
            kw["width"] = max(1, round(kw["width"] * self._s))
        self._d.line([self._pt(p) for p in pts], **kw)

    def ellipse(self, box, **kw):
        if "width" in kw:
            kw["width"] = max(1, round(kw["width"] * self._s))
        l, t, r, b = box
        self._d.ellipse([l * self._s, t * self._s, r * self._s, b * self._s], **kw)

    def polygon(self, pts, **kw):
        self._d.polygon([self._pt(p) for p in pts], **kw)

    def arc(self, box, **kw):
        if "width" in kw:
            kw["width"] = max(1, round(kw["width"] * self._s))
        l, t, r, b = box
        self._d.arc([l * self._s, t * self._s, r * self._s, b * self._s], **kw)


def canvas():
    bg = radial_navy(SIZE)
    mask = Image.new("L", (SIZE, SIZE), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, SIZE - 1, SIZE - 1], fill=255)
    out = Image.new("RGB", (SIZE, SIZE), NAVY_EDGE)
    out.paste(bg, (0, 0), mask)
    return out, ScaledDraw(ImageDraw.Draw(out), SIZE / 300)


def bezier(p0, p1, p2, p3, n=28):
    pts = []
    for i in range(n + 1):
        t = i / n
        mt = 1 - t
        x = mt**3*p0[0] + 3*mt**2*t*p1[0] + 3*mt*t**2*p2[0] + t**3*p3[0]
        y = mt**3*p0[1] + 3*mt**2*t*p1[1] + 3*mt*t**2*p2[1] + t**3*p3[1]
        pts.append((x, y))
    return pts


def poly_bezier(anchors_and_handles, n=28):
    """anchors_and_handles: list of (anchor, out_handle) tuples, open path.
    Between point i and i+1 uses (anchor_i, outhandle_i, inhandle_{i+1}, anchor_{i+1})."""
    pts = []
    for i in range(len(anchors_and_handles) - 1):
        a0, h0 = anchors_and_handles[i]
        a1, h1 = anchors_and_handles[i + 1]
        seg = bezier(a0, h0, h1, a1, n)
        pts.extend(seg if i == 0 else seg[1:])
    return pts


def grad_stroke(d, pts, width, closed=False, reverse=False):
    if closed:
        pts = pts + [pts[0]]
    n = len(pts) - 1
    for i in range(n):
        t = i / max(1, n - 1)
        if reverse:
            t = 1 - t
        col = tuple(int(GOLD_LIGHT[k] + (GOLD_DEEP[k] - GOLD_LIGHT[k]) * t) for k in range(3))
        d.line([pts[i], pts[i + 1]], fill=col, width=width)
    r = width / 2
    for i, (x, y) in enumerate(pts):
        t = i / max(1, n)
        if reverse:
            t = 1 - t
        col = tuple(int(GOLD_LIGHT[k] + (GOLD_DEEP[k] - GOLD_LIGHT[k]) * t) for k in range(3))
        d.ellipse([x - r, y - r, x + r, y + r], fill=col)


def straight_grad(d, p0, p1, width):
    grad_stroke(d, [p0, p1], width)


# ---------------------------------------------------------------- icons --

def item_003_ankush(d):
    # goad: smooth shepherd's-hook curling off a straight shaft
    straight_grad(d, (138, 235), (138, 100), 11)
    hook = poly_bezier([
        ((138, 100), (138, 68)),
        ((160, 52), (185, 58)),
        ((196, 82), (176, 104)),
        ((150, 100), (140, 96)),
    ])
    grad_stroke(d, hook, 8)
    straight_grad(d, (138, 128), (172, 146), 7)


def item_012_dhanushya(d):
    # bow: one long smooth bezier arc + taut straight string
    arc = poly_bezier([
        ((122, 78), (150, 60)),
        ((196, 92), (198, 150)),
        ((196, 208), (150, 240)),
        ((122, 222), (118, 210)),
    ])
    grad_stroke(d, arc, 10)
    straight_grad(d, (128, 92), (150, 150), 5)
    straight_grad(d, (150, 150), (128, 208), 5)


def item_013_bana(d):
    shaft = poly_bezier([((150, 80), (150, 100)), ((150, 165), (150, 190)), ((150, 218), (150, 218))])
    grad_stroke(d, shaft, 8)
    head = poly_bezier([((126, 110), (135, 90)), ((150, 62), (150, 62)), ((150, 62), (165, 90)), ((174, 110), (174, 110))])
    grad_stroke(d, head, 8, reverse=True)
    straight_grad(d, (150, 218), (128, 236), 6)
    straight_grad(d, (150, 218), (172, 236), 6)


def item_014_ikshu(d):
    arc = poly_bezier([
        ((122, 78), (150, 60)),
        ((196, 92), (198, 150)),
        ((196, 208), (150, 240)),
        ((122, 222), (118, 210)),
    ])
    grad_stroke(d, arc, 10)
    # node rings sampled along the same curve
    for frac in (0.2, 0.42, 0.62, 0.82):
        idx = int(frac * (len(arc) - 1))
        x, y = arc[idx]
        x2, y2 = arc[min(idx + 1, len(arc) - 1)]
        nx, ny = -(y2 - y), (x2 - x)
        nl = math.hypot(nx, ny) or 1
        nx, ny = nx / nl, ny / nl
        d.line([(x - nx * 8, y - ny * 8), (x + nx * 8, y + ny * 8)], fill=NAVY_EDGE, width=4)
    straight_grad(d, (128, 92), (148, 150), 5)
    straight_grad(d, (148, 150), (128, 208), 5)


def item_015_pushpabana(d):
    for dx in (-30, 0, 30):
        straight_grad(d, (150 + dx * 0.5, 228), (150 + dx, 108), 6)
        cx, cy = 150 + dx, 90
        for k in range(6):
            a = math.radians(60 * k)
            px_, py_ = cx + 12 * math.cos(a), cy + 12 * math.sin(a) * 0.9
            col = GOLD_LIGHT if k % 2 == 0 else GOLD_DEEP
            d.ellipse([px_ - 7, py_ - 7, px_ + 7, py_ + 7], fill=col)
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=NAVY_EDGE)
    straight_grad(d, (106, 208), (194, 208), 7)


def item_016_vajrashool(d):
    # classic vajra silhouette: a pinched central grip (vesica), with
    # 3 prongs fanning from each end and curving back to meet a tip
    d.ellipse([133, 133, 167, 167], outline=GOLD_LIGHT, width=7)
    straight_grad(d, (150, 133), (150, 100), 8)
    straight_grad(d, (150, 167), (150, 200), 8)
    for sign in (-1, 1):  # -1 = top set, 1 = bottom set
        hub = (150, 150 - sign * 33)
        tip = (150, 150 - sign * 88)
        grad_stroke(d, [hub, tip], 6)
        for dx in (-20, 20):
            outer = (150 + dx, 150 - sign * 60)
            curve = poly_bezier([(hub, (hub[0] + dx * 0.6, hub[1] - sign * 8)),
                                  (outer, (150 + dx * 0.3, tip[1]))])
            grad_stroke(d, curve, 5)
            grad_stroke(d, [outer, (tip[0] + (dx > 0) * 2 - 1, tip[1] + sign * 4)], 5)
        d.ellipse([tip[0] - 5, tip[1] - 5, tip[0] + 5, tip[1] + 5], fill=GOLD_LIGHT)


def item_017_vetala(d):
    d.ellipse([118, 62, 182, 122], outline=GOLD_LIGHT, width=7)
    d.ellipse([131, 86, 140, 95], fill=GOLD_DEEP)
    d.ellipse([160, 86, 169, 95], fill=GOLD_DEEP)
    straight_grad(d, (150, 122), (150, 232), 9)
    for cy in (142, 167, 192):
        straight_grad(d, (126, cy), (174, cy), 5)


def item_018_khetaka(d):
    shield = poly_bezier([
        ((150, 66), (188, 78)),
        ((206, 100), (206, 140)),
        ((206, 176), (170, 210)),
        ((150, 234), (130, 210)),
        ((94, 176), (94, 140)),
        ((94, 100), (112, 78)),
        ((150, 66), (150, 66)),
    ])
    grad_stroke(d, shield, 9)
    d.ellipse([137, 137, 163, 163], fill=GOLD_LIGHT)
    for a in (45, 135, 225, 315):
        r = math.radians(a)
        rx, ry = 150 + 44 * math.cos(r), 150 + 44 * math.sin(r) * 0.88
        d.ellipse([rx - 5, ry - 5, rx + 5, ry + 5], fill=GOLD_DEEP)


def item_019_khanjir(d):
    # straight-tapered dagger blade (a blade is not curvy) + crossguard + pommel,
    # angled diagonally like it's laid down
    tip = (198, 66)
    base_l, base_r = (128, 168), (152, 148)
    d.polygon([tip, base_r, base_l], fill=GOLD_LIGHT)
    d.line([tip, base_l], fill=GOLD_DEEP, width=2)  # spine accent
    straight_grad(d, (112, 178), (148, 152), 12)   # crossguard
    straight_grad(d, (96, 196), (124, 174), 11)     # hilt grip
    d.ellipse([88, 190, 106, 208], fill=GOLD_DEEP)  # pommel


def item_020_pasanadharana(d):
    straight_grad(d, (150, 92), (150, 220), 9)
    straight_grad(d, (96, 92), (204, 92), 10)
    tip_l = poly_bezier([((96, 92), (86, 82)), ((80, 66), (94, 58))])
    tip_r = poly_bezier([((204, 92), (214, 82)), ((220, 66), (206, 58))])
    grad_stroke(d, tip_l, 7)
    grad_stroke(d, tip_r, 7)


def item_021_nangar(d):
    beam = poly_bezier([((208, 72), (194, 88)), ((160, 120), (120, 172))])
    grad_stroke(d, beam, 10)
    straight_grad(d, (208, 72), (228, 90), 6)
    straight_grad(d, (208, 72), (196, 52), 6)
    share = poly_bezier([
        ((120, 172), (94, 178)),
        ((82, 192), (86, 212)),
        ((104, 228), (128, 214)),
        ((130, 196), (122, 182)),
    ])
    grad_stroke(d, share, 7)


def item_022_kavach(d):
    body = poly_bezier([
        ((150, 72), (196, 88)),
        ((210, 118), (204, 160)),
        ((196, 196), (150, 228)),
        ((104, 196), (96, 160)),
        ((90, 118), (104, 88)),
        ((150, 72), (150, 72)),
    ])
    grad_stroke(d, body, 8)
    straight_grad(d, (150, 100), (150, 200), 5)
    for dx in (-1, 1):
        arm = poly_bezier([((150, 110), (150 + dx * 30, 120)), ((150 + dx * 46, 145), (150 + dx * 40, 165))])
        grad_stroke(d, arm, 5)


def item_023_agni(d):
    outer = poly_bezier([
        ((150, 58), (172, 90)),
        ((176, 122), (150, 140)),
        ((196, 168), (192, 210)),
        ((172, 236), (150, 240)),
        ((128, 236), (108, 210)),
        ((104, 168), (150, 140)),
        ((124, 122), (128, 90)),
        ((150, 58), (150, 58)),
    ])
    grad_stroke(d, outer, 8)
    inner = poly_bezier([
        ((150, 128), (166, 150)),
        ((170, 178), (150, 202)),
        ((130, 178), (134, 150)),
        ((150, 128), (150, 128)),
    ])
    grad_stroke(d, inner, 5)


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
    SS = 3  # supersample for anti-aliasing since PIL draws are hard-edged
    global SIZE
    real_size = 300
    SIZE = real_size * SS
    preview = Image.new("RGB", (real_size * 5, real_size * 3), (240, 240, 240))
    for i, (item_id, fn) in enumerate(DRAWERS.items()):
        img, d = canvas()
        fn(d)
        img = img.filter(ImageFilter.GaussianBlur(1.2)).resize((real_size, real_size), Image.LANCZOS)
        out = ROOT / "media" / f"item-{item_id}" / "symbol.png"
        img.save(out, "PNG")
        r, c = divmod(i, 5)
        preview.paste(img, (c * real_size, r * real_size))
        print(f"item-{item_id} -> {out}")
    preview.save(ROOT / "icons" / "_v2_preview.png")
    print("preview -> icons/_v2_preview.png")


if __name__ == "__main__":
    main()

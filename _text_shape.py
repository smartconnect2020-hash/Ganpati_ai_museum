"""Shaped-text rendering for Devanagari (Marathi).

Pillow's ImageDraw.text() does NOT do complex-script shaping unless it was
built with libraqm — and the Windows wheels are not. Without shaping,
Marathi conjuncts (जोडाक्षरे), the reph (र्), matras and half-forms render
wrong: "सुदर्शन" comes out as "सुद‌र्‌शन", "अस्त्र" as "अस्‌त्‌र", etc.

This module shapes with HarfBuzz (uharfbuzz) and rasterises each glyph
with FreeType (freetype-py), returning a transparent RGBA PIL image that
callers paste onto their canvas. Both are self-contained binary wheels
(bundled HarfBuzz / FreeType) — `pip install` needs no separate system
library.

Conjuncts render in Nirmala's tight ligature form: त्र / क्र / स्त्र come
out as the base consonant plus a small subscript र-curl. That is correct
Marathi typography — at low preview resolution the curl can look like a
dropped letter, but it is not; check a full-resolution render.
"""
from __future__ import annotations

from functools import lru_cache

import freetype
import uharfbuzz as hb
from PIL import Image

NIRMALA = "C:/Windows/Fonts/Nirmala.ttc"
NIRMALA_BOLD_INDEX = 1          # Nirmala.ttc: 0 = regular, 1 = bold


@lru_cache(maxsize=8)
def _faces(path: str, index: int, variations: tuple = ()):
    with open(path, "rb") as fh:
        data = fh.read()
    hb_face = hb.Face(data, index)
    hb_font = hb.Font(hb_face)
    ft_face = freetype.Face(path, index=index)
    if variations:
        var = dict(variations)
        hb_font.set_variations(var)
        # FreeType wants design-space coords in declared axis order, keyed
        # by 4-letter axis TAG ("wght"), not the human-readable axis name.
        axes = ft_face.get_variation_info().axes
        coords = [var.get(ax.tag, ax.default) for ax in axes]
        ft_face.set_var_design_coords(coords)
    return hb_font, ft_face


def render_text(text: str, px: int, color=(0, 0, 0), *,
                path: str = NIRMALA, index: int = 0,
                variations: dict | None = None) -> Image.Image:
    """Return an RGBA image of `text` shaped + rasterised at `px` pixels.

    `variations`: for variable fonts, e.g. {"wght": 800} to pick a weight
    that has no static instance file (see fonts/NotoSansDevanagari.ttf,
    which ships weight 100-900 as a single variable font, no separate
    Bold/ExtraBold .ttf).
    """
    hb_font, ft_face = _faces(path, index, tuple(sorted((variations or {}).items())))
    hb_font.scale = (px * 64, px * 64)
    hb.ot_font_set_funcs(hb_font)

    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()          # script = Devanagari, dir = LTR
    hb.shape(hb_font, buf, {"kern": True, "liga": True})

    ft_face.set_pixel_sizes(0, px)
    ascender = ft_face.size.ascender / 64.0
    descender = ft_face.size.descender / 64.0

    pen = 0.0
    placed = []
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        ft_face.load_glyph(info.codepoint,
                           freetype.FT_LOAD_RENDER | freetype.FT_LOAD_TARGET_NORMAL)
        bmp = ft_face.glyph.bitmap
        w, h = bmp.width, bmp.rows
        if w and h:
            gi = Image.frombytes("L", (w, h), bytes(bmp.buffer))
            x = pen + pos.x_offset / 64.0 + ft_face.glyph.bitmap_left
            y = -(pos.y_offset / 64.0) - ft_face.glyph.bitmap_top
            placed.append((gi, x, y))
        pen += pos.x_advance / 64.0

    pad = 2
    width = max(1, int(round(pen)) + pad * 2)
    height = max(1, int(round(ascender - descender)) + pad * 2)
    baseline = ascender + pad

    canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    tint = tuple(color[:3])
    for gi, x, y in placed:
        solid = Image.new("RGBA", gi.size, tint + (0,))
        solid.putalpha(gi)
        canvas.alpha_composite(solid, (int(round(x)) + pad,
                                       int(round(baseline + y))))
    return canvas


def text_width(text: str, px: int, *, path: str = NIRMALA, index: int = 0,
              variations: dict | None = None) -> int:
    hb_font, _ = _faces(path, index, tuple(sorted((variations or {}).items())))
    hb_font.scale = (px * 64, px * 64)
    hb.ot_font_set_funcs(hb_font)
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(hb_font, buf, {"kern": True, "liga": True})
    return int(round(sum(p.x_advance for p in buf.glyph_positions) / 64.0))


def paste_centered(page: Image.Image, text: str, cx: int, top: int, px: int,
                   color=(0, 0, 0), *, path: str = NIRMALA, index: int = 0,
                   variations: dict | None = None):
    """Paste `text` horizontally centred on cx, its top edge at `top`."""
    img = render_text(text, px, color, path=path, index=index, variations=variations)
    page.paste(img, (int(cx - img.width / 2), int(top)), img)
    return img.height


if __name__ == "__main__":   # quick visual smoke test
    samples = ["सुदर्शन चक्र", "वेताळ अस्त्र", "त्रिशूळ", "वज्रशूळ",
               "इक्षुकार्मुक", "खड्ग", "वस्तू क्र. ५", "श्री गणेश आयुधे"]
    y = 20
    out = Image.new("RGB", (900, 60 * len(samples) + 40), "white")
    for s in samples:
        img = render_text(s, 44, (20, 20, 20))
        out.paste(img, (30, y), img)
        y += 60
    out.save("_text_shape_sample.png")
    print("wrote _text_shape_sample.png")

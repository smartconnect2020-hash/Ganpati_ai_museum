"""Shared QR+side-name tile renderer — used by both the multi-up A4 sheet
(_print_sheet_side_label.py) and the per-item Canva-editable tile exporter
(_export_side_label_tiles.py), so the two never drift apart.

Block = 8.63 x 5.0 cm @ 300 DPI at scale=1 (grew from the original fixed
7x5cm — QR +1cm and the text column proportionally bigger both needed real
width). `render_tile(..., scale=N)` renders the same design bigger without
ever upscaling a bitmap: the QR is regenerated with a bigger module size
(still crisp, integer pixels) and the title font size scales too — used for
the home tile's double-size treatment on its own dedicated last page (see
_print_sheet_side_label.py). No border around the tile (removed per
feedback — looked cleaner without it). No serial-number badge (removed per
feedback — was print-sheet-only scaffolding, not wanted on the final tiles).

Font history (why Noto Sans Devanagari, not Nirmala or Mukta):

  1. Nirmala Text Bold's ी (dependent-II) glyph is a closed loop that reads
     as ो (o-matra) at a glance — "खंजीर" could misread as "खंजोर". Nirmala
     UI Bold avoids this (plain vertical stroke).
  2. Item 023 अग्नी: Nirmala (all 6 faces, pixel-diff verified), Tiro
     Devanagari Marathi, Hind Bold, and Mukta Bold/ExtraBold (also
     pixel-diff verified) ALL render the ग्न conjunct identically to ग्र —
     none ships a ग्न ligature distinct from रफला (्र). Mukta was shipped
     anyway with a ZWNJ (U+200C) inserted between the halant and न to force
     an explicit, visibly-halant ग् + न — technically unambiguous, but it
     reads as a broken/stray mark to an actual reader (confirmed: flagged
     on sight). That workaround is gone now that a font was found that
     doesn't need it.
  3. Noto Sans Devanagari (Google/Noto, variable font, OFL) DOES carry a
     distinct ग्न ligature — pixel-diff confirmed different glyph widths
     for gna vs gra, at every weight tested including 800. It also keeps
     ी distinct from ो. It ships as ONE variable .ttf (wght 100-900, no
     separate Bold/ExtraBold file) — see _text_shape.py's `variations`
     param, which sets the wght axis on both the HarfBuzz shaper and the
     FreeType rasteriser. Titles render at wght=800 (~ExtraBold).
"""
from __future__ import annotations

from pathlib import Path

import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import SolidFillColorMask
from PIL import Image

from _text_shape import paste_centered, text_width

Image.init()

ROOT = Path(__file__).resolve().parent
BASE_URL = "https://smartconnect2020-hash.github.io/Ganpati_ai_museum"
HOME_ID = "000"
HOME_TITLE = "श्री गणेश आयुध माहिती"       # matches data.json meta.site_title "श्री गणेश आयुधे"

# Discontinued items — see backup-removed-items-2026-09-13/ for a full copy
# of data.json + media/ + audio-scripts/ from before removal.
EXCLUDED_IDS = {"015", "019", "022"}       # पुष्पबाण, खंजीर, कवच
FEATURED_FIRST_ID = "020"                  # अग्नी — pinned to the first / top-left tile (renumbered from 023 after sequential 001-020 renumbering)

FONT_DIR = ROOT / "fonts"
NOTO_DEVANAGARI = str(FONT_DIR / "NotoSansDevanagari.ttf")   # variable: wght 100-900
TITLE_WGHT = {"wght": 800}    # ~ExtraBold

DPI = 300
CM = DPI / 2.54

QR_MODULE_PX = 10
QR_SLOT = 49 * QR_MODULE_PX            # v6 + border -> 490px = 4.15cm
PAD_IN = round(0.16 * CM)              # block edge -> QR / text
GAP_QR_TEXT = round(0.16 * CM)
TEXT_COL_W = round(QR_SLOT * (378 / 392))   # same QR:text ratio as the original 7x5cm design

BLOCK_W = 2 * PAD_IN + QR_SLOT + GAP_QR_TEXT + TEXT_COL_W   # 1019px = 8.63cm
BLOCK_H = round(5.0 * CM)              # 591px = 5.00cm

TITLE_MAX_PX = round(QR_SLOT * 0.5)    # "roughly half the QR's height" -> 245px
TITLE_MIN_PX = 42                      # floor — still bold/legible, not shrunk to nothing

MAROON = (122, 30, 43)
IVORY = (255, 249, 236)
INK = (58, 15, 22)
CREAM = (251, 241, 222)


def load_tiles(data_json_path: Path) -> tuple[tuple[str, str, str], list[tuple[str, str, str]]]:
    """Returns (home_tile, weapon_tiles). weapon_tiles has FEATURED_FIRST_ID
    pinned first, the rest in their normal data.json order after it."""
    import json
    d = json.loads(data_json_path.read_text(encoding="utf-8"))
    home = (HOME_ID, HOME_TITLE, f"{BASE_URL}/")
    items = [it for it in d["items"] if it["id"] not in EXCLUDED_IDS]
    items.sort(key=lambda it: (it["id"] != FEATURED_FIRST_ID, it["id"]))
    weapons = [(it["id"], it["title"]["mr"], f"{BASE_URL}/?id={it['id']}") for it in items]
    return home, weapons


def make_qr(url: str, module_px: int) -> Image.Image:
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_Q,
                       box_size=module_px, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    return qr.make_image(
        image_factory=StyledPilImage,
        color_mask=SolidFillColorMask(front_color=MAROON, back_color=IVORY),
    ).convert("RGBA")


def greedy_wrap(words: list[str], px: int, max_w: int) -> list[str]:
    lines, cur = [], ""
    for w in words:
        cand = f"{cur} {w}".strip()
        if cur and text_width(cand, px, path=NOTO_DEVANAGARI, variations=TITLE_WGHT) > max_w:
            lines.append(cur)
            cur = w
        else:
            cur = cand
    if cur:
        lines.append(cur)
    return lines


def fit_title(title: str, max_w: int, max_lines: int, start_px: int, min_px: int) -> tuple[int, list[str]]:
    words = title.split(" ")
    for px in range(start_px, min_px - 1, -2):
        lines = greedy_wrap(words, px, max_w)
        if len(lines) <= max_lines and all(
            text_width(ln, px, path=NOTO_DEVANAGARI, variations=TITLE_WGHT) <= max_w for ln in lines
        ):
            return px, lines
    return min_px, greedy_wrap(words, min_px, max_w)


def render_tile(iid: str, title_mr: str, url: str, *, scale: float = 1.0) -> Image.Image:
    """Return an RGBA image, transparent background, (BLOCK_W*scale) x
    (BLOCK_H*scale). scale=1 is the standard grid tile; a bigger scale
    regenerates the QR at a bigger module size (stays crisp) and renders
    the title bigger too — used for the home tile's poster-size last page."""
    qr_module = max(1, round(QR_MODULE_PX * scale))
    qr_slot = 49 * qr_module
    pad_in = round(PAD_IN * scale)
    gap = round(GAP_QR_TEXT * scale)
    text_col_w = round(TEXT_COL_W * scale)
    block_w = 2 * pad_in + qr_slot + gap + text_col_w
    block_h = round(BLOCK_H * scale)
    title_max_px = round(TITLE_MAX_PX * scale)
    title_min_px = round(TITLE_MIN_PX * scale)

    tile = Image.new("RGBA", (block_w, block_h), (0, 0, 0, 0))

    qr = make_qr(url, qr_module)
    qx = pad_in + (qr_slot - qr.width) // 2
    qy = (block_h - qr.height) // 2
    tile.paste(qr, (qx, qy), qr)

    tx0 = pad_in + qr_slot + gap
    tx_c = tx0 + text_col_w // 2

    title_px, lines = fit_title(title_mr, text_col_w, max_lines=2,
                                start_px=title_max_px, min_px=title_min_px)
    line_h = round(title_px * 1.2)
    content_h = len(lines) * line_h
    ty = (block_h - content_h) // 2

    for ln in lines:
        paste_centered(tile, ln, tx_c, ty, title_px, INK, path=NOTO_DEVANAGARI, variations=TITLE_WGHT)
        ty += line_h

    return tile

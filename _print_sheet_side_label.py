"""A4 print sheet: QR code + Marathi name printed SIDE-BY-SIDE inside a
fixed-height block per item.

Layout / font rationale lives in _tile_common.py (shared with
_export_side_label_tiles.py, which exports the same tiles as individual
Canva-ready PNGs). This file only arranges those tiles onto A4 pages:

  Page 1-2: the 20 weapon tiles, 2 columns x 5 rows = 10/page -> exactly 2
  full pages (अग्नी pinned first/top-left — see _tile_common.FEATURED_FIRST_ID
  — the rest in normal order after it). No odd leftover partial page.

  Page 3: the home tile ("श्री गणेश आयुध माहिती" + its QR) ALONE, at roughly
  double size, scaled to fill the full page width with nothing beside it —
  it's meant for the main आरास (shrine) display, so it needs to read from
  further away than a pocket-size item tile. `HOME_SCALE` is computed from
  "fill the page width minus a safe margin" rather than a hardcoded 2.0, so
  it lands wherever that width happens to put it (works out to ~2.1x —
  "double size" and "full width" are actually the same constraint here).

Print: open the PDF -> 100% / "actual size" (NOT "fit to page") -> cut
along the tile edges (no border is drawn — see _tile_common.py).
"""
from __future__ import annotations

from PIL import Image

from _tile_common import ROOT, BLOCK_W, BLOCK_H, CM, CREAM, DPI, load_tiles, render_tile

OUT_PDF = ROOT / "qr-codes" / "print-sheet-A4-side-label.pdf"

A4_W, A4_H = round(8.27 * DPI), round(11.69 * DPI)
GAP = round(0.3 * CM)
COLS, ROWS = 2, 5
PER_PAGE = COLS * ROWS

HOME_PAGE_MARGIN = round(1.5 * CM)     # safe print margin either side of the big home tile
HOME_SCALE = (A4_W - 2 * HOME_PAGE_MARGIN) / BLOCK_W


def weapon_page(tiles: list[tuple[str, str, str]]) -> Image.Image:
    grid_w = COLS * BLOCK_W + (COLS - 1) * GAP
    grid_h = ROWS * BLOCK_H + (ROWS - 1) * GAP
    origin_x = (A4_W - grid_w) // 2
    origin_y = (A4_H - grid_h) // 2

    page = Image.new("RGB", (A4_W, A4_H), CREAM)
    for i, (iid, title_mr, url) in enumerate(tiles):
        r, c = divmod(i, COLS)
        x = origin_x + c * (BLOCK_W + GAP)
        y = origin_y + r * (BLOCK_H + GAP)
        tile = render_tile(iid, title_mr, url)
        page.paste(tile, (x, y), tile)
    return page


def home_page(home: tuple[str, str, str]) -> Image.Image:
    iid, title_mr, url = home
    tile = render_tile(iid, title_mr, url, scale=HOME_SCALE)
    page = Image.new("RGB", (A4_W, A4_H), CREAM)
    x = (A4_W - tile.width) // 2
    y = (A4_H - tile.height) // 2
    page.paste(tile, (x, y), tile)
    return page


def main():
    home, weapons = load_tiles(ROOT / "data.json")
    assert len(weapons) == PER_PAGE * 2, (
        f"expected exactly {PER_PAGE * 2} weapon tiles for 2 clean full pages, got {len(weapons)}")

    pages = [
        weapon_page(weapons[0:PER_PAGE]),
        weapon_page(weapons[PER_PAGE:PER_PAGE * 2]),
        home_page(home),
    ]

    pages[0].save(OUT_PDF, save_all=True, append_images=pages[1:], resolution=DPI)
    print(f"{len(weapons)} weapon tiles -> 2 full pages + 1 home page -> {OUT_PDF}")
    print(f"Weapon block {BLOCK_W}x{BLOCK_H}px = {BLOCK_W/CM:.2f} x {BLOCK_H/CM:.2f} cm, {COLS}x{ROWS}={PER_PAGE}/page")
    print(f"Home tile scale {HOME_SCALE:.2f}x -> {round(BLOCK_W*HOME_SCALE)/CM:.2f} x {round(BLOCK_H*HOME_SCALE)/CM:.2f} cm, "
          f"page margin {HOME_PAGE_MARGIN/CM:.2f}cm each side")


if __name__ == "__main__":
    main()

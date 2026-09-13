"""Per-item Canva-editable tiles: the same QR-plus-side-name design as
print-sheet-A4-side-label.pdf, but ONE PNG per item instead of a fixed
10-per-page grid — so each can be dropped into its own Canva canvas,
resized, or rearranged freely, independent of the print sheet's layout.

Each file is exactly BLOCK_W x BLOCK_H (8.63 x 5.0 cm @ 300 DPI), fully
transparent outside the QR/text, so it drops cleanly onto any Canva
background. All tiles here — including the home tile — are exported at the
standard scale=1; the home tile's double-size/full-width treatment is a
print-sheet-only concern (see _print_sheet_side_label.py's home_page()),
since a Canva user can resize a single PNG themselves.

Output: qr-codes/side-label-tiles/<id>-<title_mr>.png (21 files).
"""
from __future__ import annotations

from _tile_common import ROOT, BLOCK_W, BLOCK_H, DPI, CM, load_tiles, render_tile

OUT = ROOT / "qr-codes" / "side-label-tiles"
OUT.mkdir(parents=True, exist_ok=True)


def main():
    home, weapons = load_tiles(ROOT / "data.json")
    tiles = [home] + weapons
    for iid, title_mr, url in tiles:
        img = render_tile(iid, title_mr, url)
        img.save(OUT / f"{iid}-{title_mr}.png", "PNG", dpi=(DPI, DPI))

    print(f"Generated {len(tiles)} Canva-ready QR+name tiles -> {OUT}")
    print(f"Each file: {BLOCK_W}x{BLOCK_H}px @ {DPI} DPI = "
          f"{BLOCK_W/CM:.2f} x {BLOCK_H/CM:.2f} cm, transparent background.")


if __name__ == "__main__":
    main()

"""Generate print-ready, brand-styled QR tags for every item + home page.

Uses only local libraries (qrcode + Pillow) — no external QR service,
no watermark, no upload, no signup. Palette matches the "पूजा पत्रिका"
theme already defined in styles.css.
"""
from __future__ import annotations

import json
from pathlib import Path

import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import SolidFillColorMask
from PIL import Image, ImageDraw

# Devanagari needs HarfBuzz shaping — Pillow's draw.text() mangles conjuncts.
from _text_shape import paste_centered, NIRMALA, NIRMALA_BOLD_INDEX

Image.init()  # force-register format plugins before any .save() (see _print_sheet.py note)

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "qr-codes"
OUT.mkdir(exist_ok=True)

BASE_URL = "https://smartconnect2020-hash.github.io/Ganpati_ai_museum"

DEVANAGARI_DIGITS = "०१२३४५६७८९"


def to_devanagari(n: int) -> str:
    """Mirrors app.js's displayNum() so printed tags match on-site numerals."""
    return "".join(DEVANAGARI_DIGITS[int(c)] for c in str(n))

MAROON = (122, 30, 43)      # --color-primary
GOLD = (143, 98, 36)        # --color-gold (text-safe, verified 4.76:1 earlier)
CREAM = (251, 241, 222)     # --color-bg
IVORY = (255, 249, 236)     # --color-surface
INK = (58, 15, 22)          # --color-text

CARD_W = 900
QR_MODULE_PX = 14           # exact integer px per module -> perfectly crisp, no resample
PAD = 60
LOGO_FRACTION = 0.22        # decorative seal, sits ABOVE the QR — never overlaps it
PRINT_DPI = 300             # embedded in the PNG so print dialogs show the true physical size


def make_qr(url: str) -> Image.Image:
    # Square modules + ERROR_CORRECT_Q + a 4-module quiet zone, rendered at
    # an exact integer module size (no resampling — a resized QR aliases and
    # fails under JPEG). An earlier version used RoundedModuleDrawer + EC-M;
    # a stress sweep (rotation / blur / JPEG-q45 / distance, all 24 codes)
    # showed rounded+M losing 5-12 codes under JPEG recompression at every
    # size, while square+Q cleared everything. Looks are not worth an
    # unscannable tag. No centre logo either — that broke ~half the codes;
    # the item icon is a separate seal on the card (see make_card).
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=QR_MODULE_PX,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    return qr.make_image(
        image_factory=StyledPilImage,
        color_mask=SolidFillColorMask(front_color=MAROON, back_color=IVORY),
    ).convert("RGBA")


def make_card(title_mr: str, subtitle: str, url: str, logo_path: Path | None, out_path: Path):
    qr_img = make_qr(url)
    qr_box = qr_img.width           # exact, integer — varies slightly with URL length

    badge_d = int(qr_box * LOGO_FRACTION) if logo_path and logo_path.exists() else 0
    top_zone = (badge_d + 30) if badge_d else 0
    extra_h = 260 + top_zone
    card = Image.new("RGB", (CARD_W, qr_box + PAD * 2 + extra_h), CREAM)
    draw = ImageDraw.Draw(card)

    # Double gold ring frame, matching .main's box-shadow motif on the site
    inset = 22
    draw.rounded_rectangle(
        [inset, inset, CARD_W - inset, card.height - inset],
        radius=28, outline=GOLD, width=4,
    )
    draw.rounded_rectangle(
        [inset + 10, inset + 10, CARD_W - inset - 10, card.height - inset - 10],
        radius=22, outline=GOLD, width=1,
    )

    # Item icon as a seal above the QR — never overlaps the code, so the QR
    # itself stays untouched and 100% scannable (verified per-file, see
    # _verify_qr.py). This is the actual customization: every weapon's tag
    # carries its own icon, the code underneath is identical in structure.
    if badge_d:
        logo = Image.open(logo_path).convert("RGBA")
        inner = int(badge_d * 0.68)
        logo.thumbnail((inner, inner), Image.LANCZOS)
        plate = Image.new("RGBA", (badge_d, badge_d), (0, 0, 0, 0))
        pd = ImageDraw.Draw(plate)
        pd.ellipse([0, 0, badge_d, badge_d], fill=IVORY + (255,), outline=GOLD + (255,), width=5)
        px = (badge_d - logo.width) // 2
        py = (badge_d - logo.height) // 2
        plate.paste(logo, (px, py), logo)
        bx = (CARD_W - badge_d) // 2
        by = PAD
        card.paste(plate, (bx, by), plate)

    qr_x = (CARD_W - qr_box) // 2
    qr_y = PAD + top_zone + 20
    card.paste(qr_img, (qr_x, qr_y), qr_img)

    ty = qr_y + qr_box + 30
    paste_centered(card, title_mr, CARD_W // 2, ty, 52, MAROON,
                   path=NIRMALA, index=NIRMALA_BOLD_INDEX)

    sy = ty + 78
    paste_centered(card, subtitle, CARD_W // 2, sy, 30, INK)

    foot = "श्री गणेश आयुधे · स्कॅन करून ऐका"
    paste_centered(card, foot, CARD_W // 2, sy + 52, 22, GOLD)

    card.save(out_path, "PNG", dpi=(PRINT_DPI, PRINT_DPI))


def main():
    d = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))

    # Home / index QR
    make_card(
        "आमचं घर संग्रहालय",
        "सर्व २३ आयुधे — मुख्य यादी",
        f"{BASE_URL}/",
        None,
        OUT / "000-home.png",
    )

    count = 0
    for item in d["items"]:
        iid = item["id"]
        title = item["title"]["mr"]
        url = f"{BASE_URL}/?id={iid}"
        symbol = ROOT / "media" / f"item-{iid}" / "symbol.png"
        logo = symbol if symbol.exists() else None
        make_card(title, f"वस्तू क्र. {to_devanagari(int(iid))}", url, logo, OUT / f"{iid}-{title}.png")
        count += 1

    sample = Image.open(OUT / f"005-{d['items'][4]['title']['mr']}.png")
    qr_cm = QR_MODULE_PX * (6 * 4 + 17 + 8) / PRINT_DPI * 2.54   # v6 = 41 modules + 8 border
    print(f"Generated {count + 1} QR cards in {OUT}")
    print(f"Embedded print DPI: {PRINT_DPI}  (square modules, EC-Q)")
    print(f"Item card ~= {sample.width / PRINT_DPI * 2.54:.1f} x "
          f"{sample.height / PRINT_DPI * 2.54:.1f} cm; QR square ~= {qr_cm:.1f} cm "
          f"(module {QR_MODULE_PX / PRINT_DPI * 25.4:.2f} mm)")
    print("Stress-verified: all 24 codes survive rotation / blur / JPEG-q45 / "
          "distance. Fine to print smaller than the full card if space is tight.")


if __name__ == "__main__":
    main()

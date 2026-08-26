"""
Landing hero.

The sheet is 6167 x 3135 — a 1.97 landscape. A browser window is rarely
that shape, so a full-bleed `cover` fit would crop something off every
edge: on a laptop it takes the Eyes of Wakanda logo off the left and the
©MARVEL mark off the right; on a phone it takes almost everything.

The sheet's field is one flat grey, so the fix is to sit it on more of
that same grey until the file is shaped like a window. `cover` then eats
the grey instead of the artwork.

The padding was black under the bar at first, carried out from the
sheet's own edge, which put slabs of black in the bottom corners. Grey
everywhere reads as the sheet's own margin instead, so the padding is
kept as small as the range of window shapes allows.

Two files come out of it:

  wide  — the whole sheet, padded to 1.68. Safe from 1.50 to 2.20,
          which covers every ordinary browser window.
  tall  — the left column only: Shakoo, her shape note and the Eyes of
          Wakanda logo, padded to 0.44. Safe from 0.44 to 0.53, which
          is every phone held upright.
"""

import os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "Uzoma Website Images", "Uzoma Website", "Eyes of Wakanda",
                   "StyleExploration_Dora_Concept_080321_UDunkwu _v001.png")
OUT = os.path.join(ROOT, "assets", "hero")

GREY = (108, 108, 108)   # the sheet's field, and so the page behind it

WIDE_MIN, WIDE_MAX = 1.60, 2.05      # window ratios the wide file must survive
TALL_MIN = 0.50                      # below this a phone trims the right edge instead
TALL_CUT = 0.27                      # how much of the sheet the phone keeps

WIDE_WIDTHS = (2560, 1600)
TALL_WIDTHS = (1080, 720)


def bar_top(im):
    """First row of the black ©MARVEL bar. It is a hard edge, not a fade."""
    px = im.load()
    x = im.width // 2
    for y in range(im.height - 1, -1, -1):
        if px[x, y][0] > 70:
            return y + 1
    raise SystemExit("no bar found")


def pad(sheet, w, h, x, y):
    """The sheet on a canvas of the given size, the rest left flat grey."""
    canvas = Image.new("RGB", (w, h), GREY)
    canvas.paste(sheet, (x, y))
    return canvas


def save(canvas, stem, widths):
    for w in widths:
        h = round(w * canvas.height / canvas.width)
        out = os.path.join(OUT, f"{stem}-{w}.jpg")
        canvas.resize((w, h), Image.LANCZOS).save(
            out, "JPEG", quality=84, optimize=True, progressive=True)
        print(f"  {os.path.basename(out):24} {w}x{h}  {os.path.getsize(out)//1024} KB")


def main():
    os.makedirs(OUT, exist_ok=True)
    sheet = Image.open(SRC).convert("RGB")
    sw, sh = sheet.size
    print(f"sheet {sw}x{sh}  bar starts at {bar_top(sheet)}")

    w = round(sh * WIDE_MAX)
    h = round(sw / WIDE_MIN)
    x, y = (w - sw) // 2, (h - sh) // 2
    print(f"wide  {w}x{h} ratio {w/h:.3f}  pad {x} x {y}")
    save(pad(sheet, w, h, x, y), "dora-wide", WIDE_WIDTHS)

    cut = round(sw * TALL_CUT)
    left = sheet.crop((0, 0, cut, sh))
    h = round(cut / TALL_MIN)
    y = (h - sh) // 2
    print(f"tall  {cut}x{h} ratio {cut/h:.3f}  pad 0 x {y}  (keeps {cut} of {sw})")
    save(pad(left, cut, h, 0, y), "dora-tall", TALL_WIDTHS)


main()

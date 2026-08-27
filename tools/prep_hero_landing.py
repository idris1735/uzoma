"""
Landing hero.

One file. The window's shape crops it, and because there is only one
file the crop moves with the window instead of switching between fixed
versions — drag the edge and the sheet slides, it never cuts.

That rules out framing each device separately. What it needs instead is
a single frame that degrades in the right direction, which is what the
left edge gives: the sheet is anchored there, so a wide window holds the
whole line-up and a narrow one closes in on Shakoo and the Eyes of
Wakanda logo beside her. Nothing pops.

The sheet is 6167 x 3135 — a 1.97 landscape, wider than most windows —
so a bare `cover` would eat the top and bottom of it. It is sat on a
band of its own colour instead, top and bottom, until the file is 1.60.
Above that ratio the artwork spans the window edge to edge with the
©MARVEL mark still in frame; below it, the band holds the full height of
the sheet and the trim comes off the right.

The band above is the grey of the field. The band below is the black of
the ©MARVEL bar, carried down from the sheet's own last row so the logo
plate comes with it — on a phone that band is on screen, and grey there
would read as a strip of empty page under the artwork rather than as
part of it.
"""

import os

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "Uzoma Website Images", "Uzoma Website", "Eyes of Wakanda",
                   "StyleExploration_Dora_Concept_080321_UDunkwu _v001.png")
OUT = os.path.join(ROOT, "assets", "hero")

GREY = (108, 108, 108)   # the sheet's field, and so the page behind it
RATIO = 1.60             # above this the whole sheet is in frame
WIDTHS = (2560, 1600, 1100)


def main():
    os.makedirs(OUT, exist_ok=True)
    sheet = Image.open(SRC).convert("RGB")
    sw, sh = sheet.size

    h = round(sw / RATIO)
    y = (h - sh) // 2
    canvas = Image.new("RGB", (sw, h), GREY)
    canvas.paste(sheet, (0, y))
    canvas.paste(sheet.crop((0, sh - 1, sw, sh)).resize((sw, h - (y + sh))), (0, y + sh))
    print(f"sheet {sw}x{sh} -> canvas {sw}x{h} ratio {sw / h:.3f}  "
          f"grey above {y}, bar carried down {h - (y + sh)}")

    for w in WIDTHS:
        out = os.path.join(OUT, f"dora-{w}.jpg")
        canvas.resize((w, round(w * h / sw)), Image.LANCZOS).save(
            out, "JPEG", quality=84, optimize=True, progressive=True)
        print(f"  {os.path.basename(out):18} {w}x{round(w * h / sw)}  "
              f"{os.path.getsize(out) // 1024} KB")


main()

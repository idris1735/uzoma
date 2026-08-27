"""
Landing hero.

One file. The window's shape crops it, and because there is only one
file the crop moves with the window instead of switching between fixed
versions — drag the edge and the sheet slides, it never cuts.

No padding: the file is the sheet and nothing else, so there is no band
of anything above or below it at any size. The sheet's own top and
bottom edge are the frame's.

That has a price. The sheet is a 1.97 landscape and most windows are
narrower than that, so on most windows the height fills and the trim
comes off the width. It is anchored left, which is the direction it
should give way in: a wide window holds the whole line-up, a narrow one
closes in on Shakoo and the Eyes of Wakanda logo beside her. What goes
first, on anything narrower than 1.97, is the ©MARVEL mark at the far
right — the whole sheet including that mark is on the Eyes of Wakanda
page, uncropped.
"""

import os

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "Uzoma Website Images", "Uzoma Website", "Eyes of Wakanda",
                   "StyleExploration_Dora_Concept_080321_UDunkwu _v001.png")
OUT = os.path.join(ROOT, "assets", "hero")

WIDTHS = (2560, 1600, 1100)


def main():
    os.makedirs(OUT, exist_ok=True)
    sheet = Image.open(SRC).convert("RGB")
    sw, sh = sheet.size
    print(f"sheet {sw}x{sh} ratio {sw / sh:.3f}")

    for w in WIDTHS:
        h = round(w * sh / sw)
        out = os.path.join(OUT, f"dora-{w}.jpg")
        sheet.resize((w, h), Image.LANCZOS).save(
            out, "JPEG", quality=84, optimize=True, progressive=True)
        print(f"  {os.path.basename(out):18} {w}x{h}  {os.path.getsize(out) // 1024} KB")


main()

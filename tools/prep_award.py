"""
The two pictures on the about page.

The Emmy card is a flat 1080 square and needs nothing but resizing.

The award photograph is the awkward one. Its source is a raw cut-out: a
hand and trophy lifted off a violet background with a loose lasso, so a
violet blob still surrounds the subject and the outline itself is
contaminated where the two blended.

Keying the violet is only half of it — the ring of half-violet pixels
along the edge is what shows up as a purple halo on a white page. So the
mask is eroded a couple of pixels past the boundary, then feathered, and
the result is flattened onto white and saved as JPEG. The about page is
white, so a flattened cut-out reads exactly like a floating one at a
twentieth of the weight.
"""

import os
import numpy as np
from PIL import Image, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "CAA_Award.png")
EMMY = os.path.join(ROOT, "EOW_1080x1080-SOCIAL-EMMY-KAGLASS-EMW+COS.jpg")
OUT = os.path.join(ROOT, "assets", "misc")
WIDTHS = (1180, 780)
EMMY_WIDTHS = (1080, 720)


def mask(im):
    """Subject only: no violet fill, and none of the edge it bled into."""
    a = np.asarray(im).astype(np.int16)
    r, g, b, al = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
    violet = (b > 120) & (r > 60) & (g < 90) & (b - g > 70) & (r - g > 20)
    keep = ((al > 128) & ~violet).astype(np.uint8) * 255
    m = Image.fromarray(keep, "L")
    m = m.filter(ImageFilter.MinFilter(5))        # past the contaminated ring
    return m.filter(ImageFilter.GaussianBlur(1.2))


def save(im, stem, widths):
    for w in widths:
        h = round(w * im.height / im.width)
        out = os.path.join(OUT, f"{stem}-{w}.jpg")
        im.resize((w, h), Image.LANCZOS).save(
            out, "JPEG", quality=86, optimize=True, progressive=True)
        print(f"  {os.path.basename(out):22} {w}x{h}  {os.path.getsize(out)//1024} KB")


def main():
    emmy = Image.open(EMMY).convert("RGB")
    print(f"emmy card {emmy.size}")
    save(emmy, "eow-emmy", EMMY_WIDTHS)

    im = Image.open(SRC).convert("RGBA")
    m = mask(im)
    box = m.point(lambda v: 255 if v > 8 else 0).getbbox()
    im, m = im.crop(box), m.crop(box)
    print(f"trimmed to {im.size} (ratio {im.width / im.height:.4f}) from {box}")

    flat = Image.new("RGB", im.size, (255, 255, 255))
    flat.paste(im.convert("RGB"), mask=m)
    save(flat, "caa-award", WIDTHS)


main()

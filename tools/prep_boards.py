"""
The storyboards, page by page.

The three PDFs are the full boards — 529, 575 and 631 pages, about
200 MB between them. Handing a visitor a 74 MB file to flip through is
not a website, so every page is rendered here instead and served one at
a time. There is then nothing to download: the PDF never leaves this
machine.

Each page is rendered whole rather than lifting the drawing out of it,
because the scene and panel numbers along the top are part of what the
client wants read — but the white margin around that is trimmed off, so
the board fills the screen instead of a box of paper it sits inside.
WebP because these are flat colour and hard line: it lands around a
tenth of the PDF page's weight and a third of JPEG's.
"""

import os
from io import BytesIO

import fitz
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "boards")

DPI = 150
QUALITY = 76

BOARDS = [
    ("coma-toes", "Comatoes_Storyboard.pdf"),
    ("cash-trapped-1", "Cashtrapped1_Storyboard.pdf"),
    ("cash-trapped-2", "Cashtrapped2_Storyboard.pdf"),
]


def trim(im):
    """Drop the white paper margin so the board itself fills the frame."""
    a = np.asarray(im).astype(np.int16)
    ink = a.min(axis=2) < 245
    rows = np.where(ink.any(axis=1))[0]
    cols = np.where(ink.any(axis=0))[0]
    if not len(rows) or not len(cols):
        return im
    return im.crop((cols[0], rows[0], cols[-1] + 1, rows[-1] + 1))


def render(slug, pdf):
    src = os.path.join(ROOT, "Storyboards", pdf)
    out = os.path.join(OUT, slug)
    os.makedirs(out, exist_ok=True)

    doc = fitz.open(src)
    total = 0
    for n, page in enumerate(doc, 1):
        pix = page.get_pixmap(dpi=DPI)
        im = trim(Image.frombytes("RGB", (pix.width, pix.height), pix.samples))
        buf = BytesIO()
        im.save(buf, format="WEBP", quality=QUALITY, method=6)
        path = os.path.join(out, f"{n:04d}.webp")
        with open(path, "wb") as fh:
            fh.write(buf.getvalue())
        total += buf.tell()
        if n % 100 == 0:
            print(f"    {slug} {n}/{len(doc)}", flush=True)

    print(f"  {slug:16} {len(doc)} pages  {total // 1024 // 1024} MB  "
          f"({im.width}x{im.height})", flush=True)
    return len(doc)


def main():
    os.makedirs(OUT, exist_ok=True)
    counts = {slug: render(slug, pdf) for slug, pdf in BOARDS}
    print("counts:", counts)


main()

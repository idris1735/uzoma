#!/usr/bin/env python3

# SUPERSEDED by tools/prep_v2.py, which splits at the gutters between
# figures rather than at equal ink mass, and keys the paper away first.
"""Split the lineup silhouette into 5 balanced character crops.

Even columns can bisect a character, so we split by alpha mass:
greedy boundaries where cumulative silhouette ink hits k/5.
Saves assets/hero-sil-{1..5}.png (binary silhouettes).
"""
import os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "assets", "hero-eow-lineup-sil.png")
OUT = os.path.join(ROOT, "assets", "hero-sil-{i}.png")


def main():
    img = Image.open(SRC).convert("RGBA")
    w, h = img.size
    px = img.load()

    # ink mass per column
    col_mass = []
    for x in range(w):
        m = 0
        for y in range(0, h, 2):  # sample every 2nd row
            if px[x, y][3] > 24:
                m += 1
        col_mass.append(m)

    total = sum(col_mass)
    if total == 0:
        raise SystemExit("silhouette has no ink — aborting")

    # find 5 boundaries at k/5 of mass
    bounds = [0]
    target = total / 5.0
    acc = 0.0
    k = 1
    for x in range(w):
        acc += col_mass[x]
        if k < 5 and acc >= target * k:
            bounds.append(x)
            k += 1
    bounds.append(w)
    bounds[-2] = max(bounds[-2], bounds[-3] + 8)  # sanity: non-empty

    print(f"src {w}x{h}, total ink {total}")
    for i in range(5):
        x0, x1 = bounds[i], bounds[i + 1]
        crop = img.crop((x0, 0, x1, h))
        out = OUT.format(i=i + 1)
        crop.save(out)
        print(f"  hero-sil-{i + 1}.png  x {x0:>4}–{x1:<4}  ({x1 - x0}px)")


if __name__ == "__main__":
    main()

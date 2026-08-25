# -*- coding: utf-8 -*-

# SUPERSEDED by tools/prep_v2.py. This version derived the hero silhouette
# from the source PNG's alpha channel, which is fully opaque — every
# silhouette it produced was a solid black rectangle.
"""
Dev tooling. Builds the hero layer stack from the EoW lineup source:
  hero-eow-lineup-sil.png    alpha -> solid black silhouette (transparent bg)
  hero-eow-lineup-flat.jpg   posterised flats pass
  hero-eow-lineup-final.jpg  the render (optimised JPEG copy)
Also derives sketch/line passes for consistency with the site layer names.
Run once with:  python tools/prep_hero.py
"""
import os
from PIL import Image, ImageOps, ImageFilter, ImageEnhance

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "assets", "eow", "eow-01-lineup.png")
OUT = os.path.join(ROOT, "assets", "hero-eow-lineup-")

im = Image.open(SRC).convert("RGBA")
MAXW = 2560
if im.width > MAXW:
    im = im.resize((MAXW, round(im.height * MAXW / im.width)), Image.LANCZOS)

# 1. silhouette: alpha -> black, transparent background
alpha = im.getchannel("A")
sil = Image.new("RGBA", im.size, (0, 0, 0, 0))
sil.putalpha(alpha)
sil.save(OUT + "sil.png", "PNG", optimize=True)
print("sil    ", sil.size)

base = im.convert("RGB")

# 2. flats: posterised colour pass
flat = ImageOps.posterize(base, 3)
flat = ImageEnhance.Color(flat).enhance(1.25)
flat.save(OUT + "flat.jpg", "JPEG", quality=84, optimize=True, progressive=True)
print("flat   ", flat.size)

# 3. final render
base.save(OUT + "final.jpg", "JPEG", quality=82, optimize=True, progressive=True)
print("final  ", base.size)

# 4/5. sketch + line passes (green construction is added in CSS; these are the paper passes)
g = ImageOps.autocontrast(base.convert("L"), cutoff=1)
sketch = ImageOps.invert(g).point(lambda v: 255 - ((255 - v) ** 2) / 255)
sketch.convert("RGB").save(OUT + "sketch.jpg", "JPEG", quality=84, optimize=True)
edges = base.convert("L").filter(ImageFilter.FIND_EDGES)
line = ImageOps.invert(edges)
line.convert("RGB").save(OUT + "line.jpg", "JPEG", quality=84, optimize=True)
print("layers sketch / line done")
print("== DONE ==")

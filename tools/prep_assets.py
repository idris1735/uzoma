# -*- coding: utf-8 -*-

# SUPERSEDED for the derived passes: the -sketch pass here is inverted
# (white figures on black). tools/prep_v2.py rebuilds sketch/line/flat
# correctly. This file remains the record of how /assets was first
# named and optimised from the client's source folder.
"""
Dev tooling (NOT part of the site, the site needs no build step).
Optimises source art from "Uzoma Website Images/" into /assets with canonical
names, and derives the layered passes every scrollytelling effect needs:
  -sketch  : inverted construction-line pass (grayscale, invert, contrast)
  -line    : edge-detected line art pass
  -flat    : posterised flat-colour pass
  -final   : the render (optimised copy)
Run once with:  python tools/prep_assets.py
"""
import os, sys
from PIL import Image, ImageOps, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC  = os.path.join(ROOT, "Uzoma Website Images", "Uzoma Website")
OUT  = os.path.join(ROOT, "assets")
EOW, IYA, PER = "Eyes of Wakanda", "Iyanu", "Personal Works"

def makedir(p):
    os.makedirs(p, exist_ok=True)

def save_final(im, dst, maxw, q=84):
    im = im.convert("RGB")
    if im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    im.save(dst, "JPEG", quality=q, optimize=True, progressive=True)
    print(f"  final {os.path.basename(dst)}  {im.width}x{im.height}")

def save_alpha_png(im, dst, maxw):
    if im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    im.save(dst, "PNG", optimize=True)
    print(f"  png   {os.path.basename(dst)}  {im.width}x{im.height} (alpha)")

def derivations(im, stem, maxw, q=84):
    """Write -sketch, -line, -flat passes at the same aspect ratio."""
    if im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    base = im.convert("RGB")
    # sketch: pencil-on-paper inversion
    g = ImageOps.autocontrast(base.convert("L"), cutoff=1)
    sketch = ImageOps.invert(g).point(lambda v: 255 - ((255 - v) ** 2) / 255)
    sketch.convert("RGB").save(stem + "-sketch.jpg", "JPEG", quality=q, optimize=True)
    # line: edge pass, dark lines on light sheet
    edges = base.convert("L").filter(ImageFilter.FIND_EDGES)
    line = ImageOps.invert(edges)
    line.convert("RGB").save(stem + "-line.jpg", "JPEG", quality=q, optimize=True)
    # flat: posterised colour pass
    flat = ImageOps.posterize(base, 3)
    flat = ImageEnhanceColor(flat)
    flat.save(stem + "-flat.jpg", "JPEG", quality=q, optimize=True)
    print(f"  layers {os.path.basename(stem)}-{{sketch,line,flat}}.jpg")

def ImageEnhanceColor(im):
    from PIL import ImageEnhance
    return ImageEnhance.Color(im).enhance(1.25)

def process(src_path, dst_path, maxw=1800, layers=False, q=84):
    im = Image.open(src_path)
    has_alpha = im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info)
    if has_alpha:
        save_alpha_png(im, dst_path + ".png", maxw)
        if layers:
            derivations(im.convert("RGB"), dst_path, maxw, q)
    else:
        save_final(im, dst_path + ".jpg", maxw, q)
        if layers:
            derivations(im, dst_path, maxw, q)

makedir(OUT)

print("== EYES OF WAKANDA ==")
e = os.path.join(SRC, EOW); d = os.path.join(OUT, "eow"); makedir(d)
eow = [
    ("LionTeam_Lineup_Concept_UDunkwu_0809_v001.png",      "eow-01-lineup",            2560, True),
    ("Noni_Concept_UDunkwu_1.png",                         "eow-02-noni",              1800, True),
    ("Noni_Concept_UDunkwu1.png",                          "eow-03-noni-keys",         1800, False),
    ("OldNoni_Concept_UDunkwu_2.png",                      "eow-04-old-noni",          1800, False),
    ("NoniTraveller_Concept_UDunkwu_0705_v001.png",        "eow-05-traveller",         1800, False),
    ("HighCouncilman_Concept_UDunkwu_1.png",               "eow-06-councilman",        1800, False),
    ("Kuda_Concept_UDunkwu_3.png",                         "eow-07-kuda",              1800, False),
    ("TafariKuda_Concept_UDunkwu_0608_v001.png",           "eow-08-tafari",            1800, False),
    ("LionGuardFaces_Concept_UDunkwu_1103_v001.png",       "eow-09-lion-guard",        1800, False),
    ("LionChainMakers_Concept_UDunkwu_0824_v001.png",      "eow-10-chainmakers",       1800, False),
    ("HaremCaptives_Concept_UDunkwu_0928_v001.png",        "eow-11-harem",             1800, False),
    ("Seamstresses_Concept_UDunkwu_0928_v001.png",         "eow-12-seamstresses",      1800, False),
    ("EthiopianSoldiers_Concept_UDunkwu_1108_v001.png",    "eow-13-ethiopian",         1800, False),
    ("WakandanCrowd_Concept_UDunkwu_0608_v001.png",        "eow-14-crowd",             1800, False),
    ("StyleExploration_Dora_Concept_080321_UDunkwu _v001.png", "eow-15-dora",         1800, False),
    ("StyleExploration_Flashback_110921_UDunkwu_v001.png", "eow-16-flashback",         1800, False),
    ("StyleExploration_Dora_Concept_082521_UDunkwu_v001.png", "eow-17-dora-02",       1800, False),
    ("WakandanCrowd_Concept_UDunkwu_0606_v002.png",        "eow-18-crowd-02",          1800, False),
    ("WakandanCrowd_Concept_UDunkwu_0511_v001.png",        "eow-19-crowd-03",          1800, False),
]
for src, name, maxw, layers in eow:
    process(os.path.join(e, src), os.path.join(d, name), maxw, layers)

print("== IYANU ==")
i = os.path.join(SRC, IYA); d = os.path.join(OUT, "iyanu"); makedir(d)
iya = [
    ("Iyanu_Ideation.jpg",                "iyanu-01-ideation",    1800, True),
    ("Iyanu_Exploration_0711.jpg",        "iyanu-02-exploration", 1800, False),
    ("Iyanu_Exploration_0704.jpg",        "iyanu-03-exploration", 1800, False),
    ("Iyanu_Exploration_Biyi3.jpg",       "iyanu-04-biyi",        1800, False),
    ("Iyanu_Exploration_Biyi1.jpg",       "iyanu-05-biyi-02",     1800, False),
    ("Iyanu_Exploration_0621_003.jpg",    "iyanu-06-0621",        1800, False),
    ("Iyanu_Exploration_0621_001.jpg",    "iyanu-07-0621-02",     1800, False),
]
for src, name, maxw, layers in iya:
    process(os.path.join(i, src), os.path.join(d, name), maxw, layers)

print("== PERSONAL WORKS ==")
p = os.path.join(SRC, PER); d = os.path.join(OUT, "personal"); makedir(d)
per = [
    ("Afro_Ninja1.png",                 "personal-01-afro-ninja",  1600, True),
    ("Pirate_boy_action_poses.png",     "personal-02-pirate",      1600, False),
    ("vampire.png",                     "personal-03-vampire",     1600, False),
    ("femme_fatale1.png",               "personal-04-femme",       1600, False),
    ("hands.png",                       "personal-05-hands",       1600, False),
    ("People1.png",                     "personal-06-people",      1600, False),
    ("mammal_college.png",              "personal-07-mammal",      1600, False),
    ("female_gangster_dev2_1.png",      "personal-08-gangster",    1600, False),
    ("black_characters_sketches_24_1.jpg", "personal-09-sketches", 1600, False),
    ("style_dump1_1.jpg",               "personal-10-dump",        1600, False),
    ("futuristic_guy1.png",             "personal-11-futuristic",  1600, False),
    ("Sketch2_11.png",                  "personal-12-sketch",      1600, False),
]
for src, name, maxw, layers in per:
    process(os.path.join(p, src), os.path.join(d, name), maxw, layers)

print("== CAA TROPHY ==")
t = Image.open(os.path.join(ROOT, "CAA_Award.png"))
print("  mode:", t.mode, "size:", t.size)
d = os.path.join(OUT, "misc"); makedir(d)
if t.mode in ("RGBA", "LA") or (t.mode == "P" and "transparency" in t.info):
    save_alpha_png(t, os.path.join(d, "caa-award"), 1500)
else:
    save_final(t, os.path.join(d, "caa-award"), 1500, 90)

print("== DONE ==")

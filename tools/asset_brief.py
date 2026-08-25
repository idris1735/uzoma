# -*- coding: utf-8 -*-
"""
asset_brief.py — writes ASSET-BRIEF.md.

A description of every media file on the site, accurate enough that another
person (or model) can lay the site out without ever seeing the images.
Dimensions, aspect, background type, footer bar, alpha and dominant colours
are all measured from the files; the one-line subject descriptions are
authored in DESCRIPTIONS below.

Run:  python tools/asset_brief.py
"""
import os
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# Subject descriptions. Same source as the alt text in build_pages.py, kept
# short here because this file is read for layout decisions, not for a11y.
# ---------------------------------------------------------------------------
DESCRIPTIONS = {
    "hero-eow-lineup-final": "The five Lion team warriors standing in a row, full length, gold lion masks and layered violet/teal wraps. The site's opening image. Cropped to the art, no footer bar.",
    "eow-01-lineup": "The same five-warrior lineup, uncropped, with the black EYES OF WAKANDA / ©MARVEL bar across the bottom.",
    "eow-02-noni": "Noni. Portrait bust at left, a fighting stance in a blue wrap, then three grey action studies. The character that won the CAA award.",
    "eow-03-noni-keys": "Five full-length costume passes on the same figure: teal wrap, hooded cloak, mask and collar, pale robe, layered skirt.",
    "eow-04-old-noni": "An older woman in an ochre cloak and violet skirt at left, then four white line/construction turnarounds of the same garment.",
    "eow-05-traveller": "Five layered travelling costumes, labelled A-D, built up on pale grey mannequins. Fur collars, beads, wraps.",
    "eow-06-councilman": "A dark bodysuit figure, a small mask study, then three olive-and-violet draped robe variants.",
    "eow-07-kuda": "A broad heavy-set man in a red and blue panelled tunic, drawn twice, plus a slim youth in violet at right.",
    "eow-08-tafari": "Two figures. A muscular man in violet armour with a metal vambrace, and a younger figure with folded arms. Tall portrait format.",
    "eow-09-lion-guard": "Six head-and-shoulders studies in a 3x2 grid, labelled A-F. Lots of white space around them.",
    "eow-10-chainmakers": "Five armoured guards in helmets and studded leather, shown front and back. Very wide, short format.",
    "eow-11-harem": "Four figures in pale blue robes and gold headdresses. Two have arms stretched wide to show the garment shape.",
    "eow-12-seamstresses": "Three women, labelled A-C, in teal and gold wraps. Different ages and builds.",
    "eow-13-ethiopian": "Three soldiers: a shield bearer, a spearman in a grey robe, a commander with a large gold disc shield.",
    "eow-14-crowd": "Four civilians in striped and beaded wraps, one in a wide woven hat. Headed 'RIVER TRIBE'.",
    "eow-15-dora": "IMPORTANT: the shape-language sheet. Five torsos on a mid-grey field, named Shakoo, B'Risa, Koi'Fay, Y'Fett, Le'illa, each with a pale geometric primitive drawn beside it and handwritten notes underneath. This is the only artwork with a grey (not white) background, which is why the site uses it as a full-bleed background image.",
    "eow-16-flashback": "A rendered bald male bust in warm light on a grey field, with a small line drawing of the same head. Darker and more painterly than the rest.",
    "eow-17-dora-02": "Four loose vignettes of the team interacting, with red handwritten notes underneath.",
    "eow-18-crowd-02": "Four figures in red checked cloth and heavy sandals. Headed 'MINING TRIBE'.",
    "eow-19-crowd-03": "Four robed merchants in deep blue and plum, one veiled. Headed 'WAKANDAN CARAVAN'.",

    "iyanu-01-ideation": "Three young Yoruba characters full length, plus a photograph of a carved wooden figure at right captioned 'LAMIDI FAKEYE' in red handwriting.",
    "iyanu-02-exploration": "The same three characters, each paired with its line drawing, so six figures across. Wide, short format.",
    "iyanu-03-exploration": "A second pass, colour figure next to line figure, four across.",
    "iyanu-04-biyi": "Four loose line studies of one character in motion. Pure line, no colour, lots of white.",
    "iyanu-05-biyi-02": "Model sheet. Colour front view and line profile on ruled height guides, a forearm detail, and the Lamidi Fakeye reference photo at top left.",
    "iyanu-06-0621": "A boy in a red tunic and a bearded man in a green and violet wrapper, against a numbered height chart with red rules.",
    "iyanu-07-0621-02": "A single archer, full length, blue bow and a quiver of arrows, red and orange wrapper. Tall portrait format, one figure only.",

    "personal-01-afro-ninja": "A hooded warrior in a blue cape at left, a grey action study at right, and a forked blade with a tooled sheath below. Square format.",
    "personal-02-pirate": "A blond-braided boy in seven action poses with a bow. Scattered across the sheet, not a row.",
    "personal-03-vampire": "One woman in two lives: white lab coat scientist, then crimson-caped vampire with a bat form. Five figures, wide format.",
    "personal-04-femme": "A woman in a green patterned kimono with hair sticks and red ribbons, drawn four times with different expressions.",
    "personal-05-hands": "Nineteen hand studies scattered across the page in flat warm greys. No figures.",
    "personal-06-people": "Three body-type studies: sumo wrestler in a green yukata, heavyset man in a blue polo, muscular red-toned figure from behind.",
    "personal-07-mammal": "Five anthropomorphic animals in school uniforms (rhino, antelope, cheetah, gorilla, bush baby) with handwritten trait notes beside each. Titled 'MAMMAL COLLEGE'.",
    "personal-08-gangster": "A woman in leopard print and armour between two large bears with gold arrows in their backs. Flat mid-grey background, not white. Square format.",
    "personal-09-sketches": "Six head-and-shoulders expression studies of one woman in plaid and violet, arranged 2x3. Square format.",
    "personal-10-dump": "A page of loose pencil heads and figures, mostly uncoloured. Square format.",
    "personal-11-futuristic": "Three tall figures labelled A, B, C in grey armour with gold winged shoulders and crested helms. Square format.",
    "personal-12-sketch": "Three stylised women: one in a purple cocktail dress, one smoking, one seated. Square format.",

    "caa-award": "Photograph, cut out with a transparent background. A hand holding a brass-and-maple gear-shaped trophy engraved 'The 2025 Concept Art Awards / UZOMA DUNKWU'. Dark browns, brass, pale maple. Tall portrait.",
    "eow-02-noni-ghost": "Flat silhouette of the Noni sheet, filled solid violet (#7A00FF) on transparency. Used as a large faint background shape.",
    "hero-eow-lineup-sil": "Flat black silhouettes of the five warriors on full transparency. Needs a light or coloured backdrop to be visible at all.",
}

BOARD_NOTE = {
    "coma-toes": "Loose storyboard panels, black line over flat pale washes (mint, grey, skin tones) on white. Two young women in the first panels.",
    "cash-trapped-a": "Loose storyboard panels, black line with flat mint-green and grey washes. A street, a figure falling, banknotes on tarmac, parked cars.",
    "cash-trapped-b": "Second half of the same sequence. Lower camera angles, figures on the ground, more banknotes.",
}


def analyse(path):
    im = Image.open(path)
    w, h = im.size
    has_alpha = im.mode in ("RGBA", "LA") or "transparency" in im.info

    rgba = im.convert("RGBA")
    a = np.array(rgba)
    alpha = a[..., 3]
    rgb = a[..., :3].astype(float)

    transparent = bool(has_alpha and alpha.min() < 8 and (alpha < 8).mean() > 0.05)

    # Find the black bar first: everything else must be measured above it, or
    # the corner samples average white paper with black bar and report grey.
    lum = np.array(im.convert("L"))
    rows = lum.mean(axis=1)
    bar = 0
    for y in range(h - 1, max(0, h - h // 3), -1):
        if rows[y] > 60:
            bar = h - 1 - y
            break
    bar_pct = round(100 * bar / h) if bar > h * 0.03 else 0
    art_h = h - bar if bar_pct else h

    k = max(4, min(w, art_h) // 40)
    corners = np.concatenate([
        rgb[:k, :k].reshape(-1, 3), rgb[:k, -k:].reshape(-1, 3),
        rgb[art_h - k:art_h, :k].reshape(-1, 3), rgb[art_h - k:art_h, -k:].reshape(-1, 3),
    ])
    cmean = corners.mean(axis=0)
    if transparent:
        bg = "transparent"
    elif cmean.min() > 232:
        bg = "white"
    elif cmean.max() < 70:
        bg = "black/very dark"
    else:
        bg = "flat #%02X%02X%02X" % tuple(int(v) for v in cmean)

    # dominant colours, from the artwork only, ignoring paper and near-neutrals
    art = rgba.crop((0, 0, w, art_h))
    tw = 110
    small = np.array(art.resize((tw, max(1, round(tw * art_h / w)))).convert("RGB")).reshape(-1, 3)
    mx, mn = small.max(axis=1), small.min(axis=1)
    keep = small[(mx - mn > 30) & (mx > 55) & (mx < 246)]
    if len(keep) > 12:
        q = (keep // 32 * 32 + 16).astype(int)
        vals, counts = np.unique(q, axis=0, return_counts=True)
        top = vals[np.argsort(-counts)][:4]
        colours = ", ".join("#%02X%02X%02X" % tuple(c) for c in top)
    else:
        colours = "mostly neutral"

    return dict(w=w, h=h, ratio=round(w / h, 2), bg=bg, bar=bar_pct, colours=colours,
                alpha=transparent, kb=os.path.getsize(path) // 1024)


def shape(r):
    if r >= 2.0:
        return "very wide"
    if r >= 1.5:
        return "wide"
    if r >= 1.15:
        return "landscape"
    if r >= 0.95:
        return "square"
    return "portrait"


def row(rel, info, desc):
    bits = [f"{info['w']}x{info['h']}", f"{info['ratio']}:1 {shape(info['ratio'])}", f"bg {info['bg']}"]
    if info["bar"]:
        bits.append(f"black ©MARVEL bar across the bottom ~{info['bar']}% of the height")
    if info["alpha"]:
        bits.append("has real transparency")
    bits.append(f"key colours {info['colours']}")
    return f"- `{rel}` — {'; '.join(bits)}.\n  {desc}\n"


def main():
    out = []
    A = lambda *p: os.path.join(ROOT, "assets", *p)

    def block(title, files, note=""):
        out.append(f"\n### {title}\n")
        if note:
            out.append(note + "\n")
        for rel in files:
            path = os.path.join(ROOT, rel.replace("/", os.sep))
            if not os.path.exists(path):
                continue
            stem = os.path.splitext(os.path.basename(rel))[0]
            out.append(row(rel, analyse(path), DESCRIPTIONS.get(stem, "")))

    def listdir(d, skip=()):
        return sorted(f"assets/{d}/{f}" for f in os.listdir(A(d))
                      if f.lower().endswith((".png", ".jpg"))
                      and not any(s in f for s in skip))

    block("Hero images (home page only)",
          ["assets/hero-eow-lineup-final.jpg", "assets/hero-eow-lineup-sil.png"],
          "These are cropped copies of `eow-01-lineup` with the ©MARVEL bar removed, "
          "so their aspect ratio (2.18:1) differs from every other Eyes of Wakanda file. "
          "`-flat`, `-line` and `-sketch` versions exist at the same size.")

    block("Eyes of Wakanda", listdir("eow", skip=("-flat", "-line", "-sketch", "-ghost")))
    block("Iyanu", listdir("iyanu", skip=("-flat", "-line", "-sketch")))
    block("Personal work", listdir("personal", skip=("-flat", "-line", "-sketch")))
    block("Cutouts with transparency",
          ["assets/misc/caa-award.png", "assets/eow/eow-02-noni-ghost.png"])

    out.append("\n### Storyboard frames\n")
    for prefix, note in BOARD_NOTE.items():
        files = sorted(f for f in os.listdir(A("boards")) if f.startswith(prefix))
        info = analyse(A("boards", files[0]))
        thumb = analyse(os.path.join(ROOT, "assets", "thumbs", "boards",
                                     os.path.splitext(files[0])[0] + ".jpg"))
        out.append(
            f"- `assets/boards/{prefix}-f01..f{len(files):02d}.jpg` — {len(files)} frames, "
            f"{info['w']}x{info['h']} each ({info['ratio']}:1), with the film's black bars "
            f"baked in. The 900px copies in `assets/thumbs/boards/` are letterbox-trimmed to "
            f"{thumb['w']}x{thumb['h']} ({thumb['ratio']}:1) — **use the thumbs**, or you "
            f"will get black bars inside every panel.\n  {note}\n")

    out.append("\n### Video\n")
    for f in sorted(os.listdir(A("video"))):
        kb = os.path.getsize(A("video", f)) // 1024
        out.append(f"- `assets/video/{f}` — {kb} KB, 1280x720, roughly 8 seconds, silent, "
                   f"loops. An animatic of the matching storyboard.\n")

    brief = HEADER + "".join(out) + FOOTER

    with open(os.path.join(ROOT, "ASSET-BRIEF.md"), "w", encoding="utf-8") as fh:
        fh.write(brief)
    # the same brief with the review framing on top, for pasting in one go
    with open(os.path.join(ROOT, "KIMI-PROMPT.md"), "w", encoding="utf-8") as fh:
        fh.write(PROMPT + brief)
    print("wrote ASSET-BRIEF.md and KIMI-PROMPT.md")


PROMPT = """# Review brief — uzomadunkwu.com

## What this is

A portfolio site for Uzoma Dunkwu, a Nigerian visual development artist and
writer/director in animation. He won a 2026 Primetime Creative Arts Emmy for
Outstanding Individual Achievement in Animation, Character Design on Marvel
Animation's *Eyes of Wakanda*, and a 2025 Concept Art Association Award for
the character Noni from the same show. He also did visual development on Lion
Forge Animation's *Iyanu*, runs Scroll Entertainment in Lagos, and is
directing his debut animated short.

Five pages: a home page, three project pages (Eyes of Wakanda, Iyanu,
Personal), and a storyboard page. No build step, no framework. GSAP,
ScrollTrigger, Lenis and SplitType from a CDN; everything else is hand-written
HTML, CSS and vanilla JS.

## What you have and what you do not

You have every HTML, CSS and JS file. **You do not have the images**, and
there are 38 artworks plus 23 storyboard frames driving most of the layout.
The document below describes every one of them: exact path, pixel dimensions,
aspect ratio, background colour, transparency, whether it carries a black
licensing bar, and what is actually depicted. All of it is measured from the
real files.

Work from that description. Do not guess at an image's shape or content, and
do not assume a file exists unless it is listed.

## What I want from you

Your own take on the front-end. Be blunt. In particular:

- Structural and CSS problems: specificity collisions, layout that will break
  at sizes I have not tested, anything fragile in the scroll choreography.
- JavaScript: correctness, event handling, teardown, anything that will
  misbehave on resize or on a slow connection.
- Accessibility and the no-JavaScript fallback, which is meant to render as a
  complete static document.
- Whether the section order and pacing of the home page actually work for a
  studio hiring manager skimming it in sixty seconds.

If you rewrite any markup or CSS, it has to run against the real files:

1. Use the exact `src` paths from the list below. Nothing else exists.
2. Respect each file's aspect ratio. Several are 2.3:1 and several are
   portrait; a grid that assumes uniform tiles will crop faces.
3. Read the seven rules before the file list. They are the mistakes that have
   already been made once on this project.
4. Keep all 38 artworks and 23 frames in use somewhere.

Two things worth saying plainly: you cannot judge the visual composition of
work you cannot see, so weigh in on structure, code and information
architecture rather than art direction. And if something in the brief
contradicts what the code does, say so — that is a real bug worth finding.

---

"""


HEADER = """# Asset brief — uzomadunkwu.com

You have the HTML, CSS and JS for this site but not the images. This file
describes every image and video precisely enough to lay the site out without
seeing them. Dimensions, aspect ratios, background colour, transparency and
dominant colours are measured from the actual files.

**Whatever you change, keep the `src` paths and the aspect ratios below.**

---

## Rules that will break the site if you ignore them

1. **Almost every artwork sits on a pure white background.** They are concept
   sheets, not photographs. If you set one as a full-bleed background, or put
   it directly on the dark page with no frame, you get a white slab. Present
   each one inside a frame with a visible edge.

2. **Never use `object-fit: cover` on an artwork.** These are character
   sheets; cropping one cuts a figure in half. Use `contain`, or give the
   container the artwork's own aspect ratio, which is listed for every file
   below. `cover` is only safe where the container ratio already matches.

3. **Most Eyes of Wakanda files carry a black bar across the bottom** with the
   EYES OF WAKANDA logo and ©MARVEL. It is part of the image and cannot be
   styled away. Its height is given per file. Do not put text over it, and do
   not crop it off — it is the licensing credit.

4. **Silhouette PNGs are solid black on transparency.** On a dark background
   they are invisible. They need a light or coloured surface behind them; the
   site puts a violet radial glow there.

5. **`assets/thumbs/` mirrors the folder structure at 900px wide**, JPEG, with
   any transparency flattened onto white. Use the thumbs for grids, mosaics
   and anything that shows many images at once. Use the full-size original
   only when one image fills the screen.

6. **Four artworks have derived process passes** (`-sketch`, `-line`,
   `-flat`, plus the render with no suffix), all at identical dimensions to
   their render: `eow-01-lineup`, `eow-02-noni`, `iyanu-01-ideation`,
   `personal-01-afro-ninja`, plus the hero crop. `-sketch` is a pale pencil
   under-drawing, `-line` is dark line on white, `-flat` is posterised flat
   colour. No other artwork has them; do not reference passes that do not
   exist.

7. **`assets/sil-map.json`** holds the position of each of the five warriors
   inside the lineup artwork, normalised 0-1, with a head anchor point. That
   is how labels are pinned to the right character. The same numbers are
   inlined in `js/home.js` as `FIGURES`.

---

## Every file
"""

FOOTER = """
---

## Counts

38 finished artworks (19 Eyes of Wakanda, 7 Iyanu, 12 personal), 23 storyboard
frames, 3 clips, 1 award photograph. Every one of them is used somewhere on
the site. If you restructure, keep it that way.

## House rules for copy

Write plain labels only. Use the real names: client names, character names,
project names, and the artist's own titles for each piece, which are the ones
in this file. Do not invent section headings, dates, or descriptions of how
the work was made, and do not add instructional copy. Where a label adds
nothing, leave it out.
"""


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
prep_v2.py — builds every derived asset the site needs.

The source artwork is figures on pure white with a black ©MARVEL footer bar,
and the PNG alpha is fully opaque. prep_hero.py assumed real transparency, so
every silhouette it produced was a solid black rectangle. This keys the white
background away instead.

Produces
  assets/hero-eow-lineup-sil.png   true alpha silhouette of the lineup
  assets/hero-sil-{1..5}.png       one silhouette per character, trimmed
  assets/eow/eow-02-noni-ghost.png Noni silhouette (award section)
  assets/misc/caa-award.png        trophy cutout with the violet blob removed
  assets/thumbs/**                 900px-wide gallery thumbnails

Run:  python tools/prep_v2.py
"""
import os
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = lambda *p: os.path.join(ROOT, "assets", *p)


# ----------------------------------------------------------------- keying ---
def background_mask(lum, white=244, scale_w=720):
    """True where a pixel is background: near-white and reachable from the
    border. Interior whites (a robe, the gap between two arms) stay figure
    because they are not connected to the edge. Computed at low resolution
    and scaled back up; a silhouette needs mass, not pixel accuracy.
    """
    h, w = lum.shape
    sw = min(scale_w, w)
    sh = max(1, round(h * sw / w))
    small = np.array(Image.fromarray(lum).resize((sw, sh), Image.BILINEAR))

    paper = small >= white
    bg = np.zeros_like(paper)
    bg[0, :] |= paper[0, :]
    bg[-1, :] |= paper[-1, :]
    bg[:, 0] |= paper[:, 0]
    bg[:, -1] |= paper[:, -1]

    # flood the paper region outward from the border
    for _ in range(sw + sh):
        grown = bg.copy()
        grown[1:, :] |= bg[:-1, :]
        grown[:-1, :] |= bg[1:, :]
        grown[:, 1:] |= bg[:, :-1]
        grown[:, :-1] |= bg[:, 1:]
        grown &= paper
        if np.array_equal(grown, bg):
            break
        bg = grown

    up = Image.fromarray((bg * 255).astype(np.uint8)).resize((w, h), Image.BILINEAR)
    return np.array(up)  # 0..255, 255 = paper


def footer_top(lum, thresh=60):
    """First row of the solid black ©MARVEL bar, or the image height."""
    rows = lum.mean(axis=1)
    h = len(rows)
    for y in range(h - 1, max(0, h - h // 3), -1):
        if rows[y] > thresh:
            return y + 1
    return h


def silhouette(src, feather=1.5):
    """Black figures on a transparent background, footer bar dropped."""
    im = Image.open(src).convert("RGB")
    lum = np.array(im.convert("L"))
    cut = footer_top(lum)

    bg = background_mask(lum[:cut])
    alpha = np.zeros(lum.shape, dtype=np.uint8)
    alpha[:cut] = 255 - bg

    # The artwork carries ruled guide lines across it. A figure's coverage
    # changes gradually down the image; a ruled line is a one-row spike, so
    # drop rows that jump well above their neighbourhood.
    cover = (alpha[:cut] > 30).sum(axis=1) / alpha.shape[1]
    pad = np.pad(cover, 12, mode="edge")
    local = np.array([np.median(pad[y:y + 25]) for y in range(len(cover))])
    spike = np.where((cover > 0.28) & (cover > 3.0 * np.maximum(local, 1e-3)))[0]
    for y in spike:
        alpha[max(0, y - 2):y + 3] = 0
    # a row that runs edge to edge is a rule, not a figure
    for y in np.where(cover > 0.85)[0]:
        alpha[max(0, y - 2):y + 3] = 0

    out = Image.new("RGBA", im.size, (0, 0, 0, 0))
    out.putalpha(Image.fromarray(alpha))
    if feather:
        from PIL import ImageFilter
        a = out.getchannel("A").filter(ImageFilter.GaussianBlur(feather))
        out.putalpha(a)
    return out


# ----------------------------------------------------------------- passes ---
# Each artwork can be shown at four stages. Only the render is real art; the
# other three are derived. The old pipeline inverted the sketch, producing
# white figures on black instead of pencil on paper.

def _line(gray):
    """Dark line on a white background."""
    from PIL import ImageFilter, ImageOps
    return ImageOps.invert(gray.filter(ImageFilter.FIND_EDGES))


def _sketch(gray):
    """Pale under-drawing: washed-out tone with a soft pencil line over it."""
    from PIL import ImageChops, ImageFilter
    white = Image.new("L", gray.size, 255)
    tone = Image.blend(white, gray, 0.20)                   # very light tone
    pencil = _line(gray).filter(ImageFilter.GaussianBlur(0.7))
    pencil = pencil.point(lambda v: 255 - (255 - v) * 0.6)  # graphite weight, not ink
    return ImageChops.multiply(tone, pencil)


def build_passes(rel, base=None):
    """Write <rel>-sketch / -line / -flat next to <rel>'s render."""
    from PIL import ImageOps, ImageEnhance
    src = base or Image.open(A(rel + (".png" if os.path.exists(A(rel + ".png")) else ".jpg")))
    art = src.convert("RGB") if src.mode != "RGB" else src
    if src.mode == "RGBA":
        bg = Image.new("RGB", src.size, (255, 255, 255))
        bg.paste(src, mask=src.getchannel("A"))
        art = bg

    gray = art.convert("L")
    _sketch(gray).convert("RGB").save(A(rel + "-sketch.jpg"), "JPEG", quality=84, optimize=True)
    _line(gray).convert("RGB").save(A(rel + "-line.jpg"), "JPEG", quality=86, optimize=True)
    flat = ImageEnhance.Color(ImageOps.posterize(art, 3)).enhance(1.25)
    flat.save(A(rel + "-flat.jpg"), "JPEG", quality=84, optimize=True, progressive=True)
    print("passes", rel, art.size)


PASS_SOURCES = [
    "eow/eow-01-lineup",
    "eow/eow-02-noni",
    "iyanu/iyanu-01-ideation",
    "personal/personal-01-afro-ninja",
]


# ------------------------------------------------------------ hero splits ---
def figure_bounds(alpha, n, gap_floor=0.03):
    """Column ranges for n figures, cut at the empty gaps between them."""
    mass = (alpha > 30).sum(axis=0).astype(float)
    mass /= max(mass.max(), 1)
    empty = mass < gap_floor

    # every run of empty columns is a candidate gutter
    gutters, run = [], None
    for x, e in enumerate(empty):
        if e and run is None:
            run = x
        elif not e and run is not None:
            gutters.append((run, x))
            run = None
    if run is not None:
        gutters.append((run, len(empty)))

    inner = [g for g in gutters if g[0] > 0 and g[1] < len(empty)]
    inner.sort(key=lambda g: g[1] - g[0], reverse=True)
    cuts = sorted((g[0] + g[1]) // 2 for g in inner[: n - 1])

    ink = np.where(~empty)[0]
    lo, hi = (int(ink[0]), int(ink[-1]) + 1) if len(ink) else (0, len(empty))
    edges = [lo] + cuts + [hi]
    return [(edges[i], edges[i + 1]) for i in range(len(edges) - 1)]


def build_hero_passes():
    """Hero copies are cropped to the artwork so the wordmark can sit across
    the bottom of the frame. The case-study copies keep the ©MARVEL bar."""
    from PIL import ImageOps, ImageEnhance, ImageFilter

    src = Image.open(A("eow", "eow-01-lineup.png")).convert("RGB")
    cut = footer_top(np.array(src.convert("L")))
    art = src.crop((0, 0, src.width, cut))
    print("hero art", art.size, f"(bar cropped at {cut})")

    art.save(A("hero-eow-lineup-final.jpg"), "JPEG", quality=84, optimize=True, progressive=True)

    flat = ImageEnhance.Color(ImageOps.posterize(art, 3)).enhance(1.25)
    flat.save(A("hero-eow-lineup-flat.jpg"), "JPEG", quality=84, optimize=True, progressive=True)

    _line(art.convert("L")).convert("RGB").save(
        A("hero-eow-lineup-line.jpg"), "JPEG", quality=86, optimize=True, progressive=True)

    _sketch(art.convert("L")).convert("RGB").save(
        A("hero-eow-lineup-sketch.jpg"), "JPEG", quality=84, optimize=True)
    return art.size


def build_hero_silhouettes():
    """Also writes sil-map.json: the position of each character inside the
    artwork, normalised 0-1, shared by the preloader and the hero."""
    import json

    src = A("eow", "eow-01-lineup.png")
    sil = silhouette(src)
    sil = sil.crop((0, 0, sil.width, footer_top(np.array(Image.open(src).convert("L")))))
    sil.save(A("hero-eow-lineup-sil.png"), "PNG", optimize=True)
    W, H = sil.size
    print("sil   ", sil.size, os.path.getsize(A("hero-eow-lineup-sil.png")) // 1024, "KB")

    alpha = np.array(sil.getchannel("A"))
    figures = []
    for i, (x0, x1) in enumerate(figure_bounds(alpha, 5), start=1):
        crop = sil.crop((x0, 0, x1, H))
        box = crop.getbbox() or (0, 0, crop.width, crop.height)
        crop = crop.crop(box)
        crop.save(A(f"hero-sil-{i}.png"), "PNG", optimize=True)

        left, top = x0 + box[0], box[1]
        # head anchor: centre of this figure's topmost band of mass
        sub = alpha[top:top + max(1, crop.height // 16), left:left + crop.width]
        cols = np.where(sub.sum(axis=0) > 0)[0]
        head_x = left + (int(cols.mean()) if len(cols) else crop.width // 2)

        figures.append({
            "src": f"assets/hero-sil-{i}.png",
            "x": round(left / W, 5),
            "y": round(top / H, 5),
            "w": round(crop.width / W, 5),
            "h": round(crop.height / H, 5),
            "headX": round(head_x / W, 5),
            "headY": round(top / H, 5),
        })
        print(f"  hero-sil-{i}.png  x {x0:>5}-{x1:<5}  {crop.size}")

    with open(A("sil-map.json"), "w", encoding="utf-8") as f:
        json.dump({"sheet": [W, H], "ratio": round(W / H, 5), "figures": figures}, f, indent=2)
    print("  sil-map.json — sheet", W, "x", H, "ratio", round(W / H, 4))


def build_noni_silhouette(tint=(122, 0, 255)):
    """Background silhouette for the award section. Written pre-tinted rather
    than coloured with a CSS mask, because a mask is a same-origin request and
    would fail when the site is opened over file://."""
    sil = silhouette(A("eow", "eow-02-noni.png"))
    box = sil.getbbox()
    if box:
        sil = sil.crop(box)
    a = np.array(sil)
    a[..., 0], a[..., 1], a[..., 2] = tint
    out = Image.fromarray(a, "RGBA")
    out.save(A("eow", "eow-02-noni-ghost.png"), "PNG", optimize=True)
    print("noni ghost", out.size)


# ----------------------------------------------------------------- award ----
def build_award():
    """The keyed source has a hard violet fill around the hand. Remove it."""
    im = Image.open(os.path.join(ROOT, "CAA_Award.png")).convert("RGBA")
    a = np.array(im).astype(np.int16)
    r, g, b, al = a[..., 0], a[..., 1], a[..., 2], a[..., 3]

    # the violet fill: strong blue and red, very little green
    violet = (b > 120) & (r > 60) & (g < 90) & (b - g > 70) & (r - g > 20)
    al[violet] = 0

    out = np.dstack([a[..., :3], al]).astype(np.uint8)
    im = Image.fromarray(out, "RGBA")
    box = im.getbbox()
    if box:
        im = im.crop(box)

    w = 860
    im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    im.save(A("misc", "caa-award.png"), "PNG", optimize=True)
    print("award ", im.size, os.path.getsize(A("misc", "caa-award.png")) // 1024, "KB")


# ---------------------------------------------------------------- thumbs ----
GALLERY_DIRS = ["eow", "iyanu", "personal", "boards"]


def trim_letterbox(im, thresh=18):
    """Board frames are exported with the film's black bars baked in. Crop
    them off so the panel fills its tile."""
    g = np.array(im.convert("L"))
    rows = g.max(axis=1)
    keep = np.where(rows > thresh)[0]
    if not len(keep) or (keep[-1] - keep[0] + 1) == len(rows):
        return im
    return im.crop((0, int(keep[0]), im.width, int(keep[-1]) + 1))


def build_thumbs(width=900, quality=76):
    made = 0
    for d in GALLERY_DIRS:
        src_dir = A(d)
        out_dir = A("thumbs", d)
        os.makedirs(out_dir, exist_ok=True)
        for name in sorted(os.listdir(src_dir)):
            if not name.lower().endswith((".png", ".jpg", ".jpeg")):
                continue
            if name.endswith("-sil.png"):
                continue
            im = Image.open(os.path.join(src_dir, name))
            if im.mode in ("RGBA", "LA", "P"):
                bg = Image.new("RGB", im.size, (255, 255, 255))
                im = im.convert("RGBA")
                bg.paste(im, mask=im.getchannel("A"))
                im = bg
            else:
                im = im.convert("RGB")
            if d == "boards":
                im = trim_letterbox(im)
            if im.width > width:
                im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
            out = os.path.join(out_dir, os.path.splitext(name)[0] + ".jpg")
            im.save(out, "JPEG", quality=quality, optimize=True, progressive=True)
            made += 1
    print("thumbs", made, "files")


if __name__ == "__main__":
    for rel in PASS_SOURCES:
        build_passes(rel)
    build_hero_passes()
    build_hero_silhouettes()
    build_noni_silhouette()
    build_award()
    build_thumbs()
    print("== DONE ==")

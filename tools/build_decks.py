"""
The portfolio and storyboard pages, as decks.

The client does not want people scrolling to see the work: one piece is
on screen at a time, filling the window, with the controls in plain
sight. So each of these pages is a deck — every sheet in the document,
one shown, the rest waiting.

Captions and alt text are lifted out of the pages they replace so the
artist's own titles survive the rewrite. Nothing here is invented.
"""

import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PLATE = re.compile(
    r'<figure class="plate"[^>]*>\s*<img src="([^"]+)" alt="([^"]*)"[^>]*>\s*'
    r'<figcaption>([^<]*)</figcaption>', re.S)
FILM = re.compile(
    r'<section class="film"[^>]*>\s*<h2 class="film__title">([^<]+)</h2>\s*'
    r'<video src="([^"]+)"[^>]*?poster="([^"]+)"[^>]*?aria-label="([^"]*)"[^>]*>\s*</video>\s*'
    r'<div class="frames">(.*?)</div>', re.S)
FRAME = re.compile(r'<img src="([^"]+)" alt="([^"]*)"')


def read(name):
    with open(os.path.join(ROOT, name), encoding="utf-8") as fh:
        return fh.read()


def write(name, text):
    with open(os.path.join(ROOT, name), "w", encoding="utf-8") as fh:
        fh.write(text)
    print(f"  {name:34} {len(text) // 1024} KB")


# ------------------------------------------------------------------ chrome --

def nav(current):
    def m(key):
        return ' aria-current="page"' if key == current else ""
    return f'''  <a class="head__name" href="index.html">Uzoma Dunkwu</a>
  <nav class="head__nav" aria-label="Primary">
    <a href="about.html"{m("about")}>About</a>
    <div class="drop">
      <span class="drop__label">Portfolio</span>
      <div class="drop__panel">
        <a href="work-eyes-of-wakanda.html"{m("eow")}>Eyes of Wakanda</a>
        <a href="work-iyanu.html"{m("iyanu")}>Iyanu</a>
        <a href="work-personal.html"{m("personal")}>Personal</a>
      </div>
    </div>
    <div class="drop">
      <span class="drop__label">Storyboards</span>
      <div class="drop__panel">
        <a href="storyboards-coma-toes.html"{m("coma")}>Coma Toes</a>
        <a href="storyboards-cash-trapped.html"{m("cash")}>Cash Trapped</a>
      </div>
    </div>
    <a href="https://uzomadunkwu.gumroad.com/l/ethniccharacterdesign" target="_blank" rel="noopener">Products</a>
    <a href="contact.html"{m("contact")}>Contact</a>
  </nav>
  <input class="nav-toggle" type="checkbox" id="nav-toggle">
  <label class="nav-burger" for="nav-toggle" aria-label="Menu"><span></span><span></span></label>'''


HEAD = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Uzoma Dunkwu</title>
<meta name="description" content="{desc}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' fill='%23fff'/%3E%3Crect x='8' y='8' width='16' height='16' fill='%23111'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://api.fontshare.com" crossorigin>
<link rel="preconnect" href="https://cdn.fontshare.com" crossorigin>
<link href="https://api.fontshare.com/v2/css?f[]=clash-display@500,600&f[]=satoshi@400,500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/site.css">
</head>
<body class="is-deck">
<a class="skip" href="#main">Skip to content</a>

<header class="head">
{nav}
</header>

<main id="main">
<section class="deck" data-deck>
  <h1 class="deck__title">{title}</h1>
  <div class="deck__stage">
{slides}
  </div>
  <div class="deck__bar">
    <button class="deck__btn" type="button" data-deck-prev aria-label="Previous">
      <svg viewBox="0 0 24 24" aria-hidden="true"><polyline points="15,4 7,12 15,20"/></svg>
    </button>
    <div class="deck__dots"></div>
    <button class="deck__btn" type="button" data-deck-next aria-label="Next">
      <svg viewBox="0 0 24 24" aria-hidden="true"><polyline points="9,4 17,12 9,20"/></svg>
    </button>
  </div>
</section>
</main>

<script src="js/site.js"></script>
</body>
</html>
'''


def image_slide(src, alt, caption, first):
    load = ' fetchpriority="high"' if first else ' loading="lazy"'
    return f'''    <figure class="slide">
      <div class="slide__frame"><img src="{src}" alt="{alt}"{load} decoding="async"></div>
      <figcaption>{caption}</figcaption>
    </figure>'''


def video_slide(src, poster, label, caption):
    return f'''    <figure class="slide">
      <div class="slide__frame"><video src="{src}" poster="{poster}" controls muted loop playsinline preload="none" aria-label="{label}"></video></div>
      <figcaption>{caption}</figcaption>
    </figure>'''


def deck(name, title, desc, current, slides):
    write(name, HEAD.format(title=title, desc=desc, nav=nav(current),
                            slides="\n".join(slides)))


# ------------------------------------------------------------------- build --

def work(source, out, title, desc, current):
    plates = PLATE.findall(read(source))
    if not plates:
        raise SystemExit(f"no plates found in {source}")
    slides = [image_slide(src, alt, cap, i == 0)
              for i, (src, alt, cap) in enumerate(plates)]
    deck(out, title, desc, current, slides)


def boards():
    films = FILM.findall(read("storyboards.html"))
    if len(films) != 3:
        raise SystemExit(f"expected 3 films, found {len(films)}")

    by_title = {f[0]: f for f in films}

    def film_slides(title, first_film):
        _, video, poster, label, frames = by_title[title]
        out = [video_slide(video, poster, label, f"{title} — animatic")]
        for i, (src, alt) in enumerate(FRAME.findall(frames)):
            out.append(image_slide(src, alt, title, first_film and i == 0))
        return out

    deck("storyboards-coma-toes.html", "Coma Toes",
         "Coma Toes — storyboards and animatic by Uzoma Dunkwu.", "coma",
         film_slides("Coma Toes", True))

    deck("storyboards-cash-trapped.html", "Cash Trapped",
         "Cash Trapped — storyboards and animatics by Uzoma Dunkwu.", "cash",
         film_slides("Cash Trapped, part 1", True)
         + film_slides("Cash Trapped, part 2", False))


def relink():
    """The pages that are not decks share the same header."""
    for name, current in [("index.html", None), ("about.html", "about"),
                          ("contact.html", "contact")]:
        s = read(name)
        s = re.sub(r'(<header class="head[^"]*">\n).*?(\n</header>)',
                   lambda m: m.group(1) + nav(current) + m.group(2), s, flags=re.S)
        write(name, s)


def main():
    print("decks:")
    work("work-eyes-of-wakanda.html", "work-eyes-of-wakanda.html", "Eyes of Wakanda",
         "Eyes of Wakanda — character design and visual development by Uzoma Dunkwu for Marvel Animation.",
         "eow")
    work("work-iyanu.html", "work-iyanu.html", "Iyanu",
         "Iyanu — visual development by Uzoma Dunkwu for Lion Forge Animation.", "iyanu")
    work("work-personal.html", "work-personal.html", "Personal",
         "Personal work by Uzoma Dunkwu.", "personal")
    boards()
    print("headers:")
    relink()


main()

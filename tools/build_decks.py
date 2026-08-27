"""
The portfolio and storyboard pages, as decks.

The client does not want people scrolling to see the work: one piece is
on screen at a time, filling the window, with the controls in plain
sight. So each portfolio page is a deck — every sheet in the document,
one shown, the rest waiting.

Portfolio captions and alt text are lifted out of the pages they replace
so the artist's own titles survive the rewrite. Nothing here is invented.

The storyboard pages are a different shape: a tab for each thing there
is to look at, which is a board to page through (rendered by
prep_boards.py) or an animatic on YouTube. The players use the plain
youtube.com embed rather than the nocookie one — the privacy-enhanced
host is blocked by filters that leave the ordinary one alone, and the
client needs these to play everywhere.
"""

import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# a deck page as it stands, and the plate page it was built from — this
# script has to be able to run twice
SLIDE = re.compile(
    r'<figure class="slide">\s*<div class="slide__frame">'
    r'<img src="([^"]+)" alt="([^"]*)"[^>]*></div>\s*'
    r'<figcaption>([^<]*)</figcaption>', re.S)
PLATE = re.compile(
    r'<figure class="plate"[^>]*>\s*<img src="([^"]+)" alt="([^"]*)"[^>]*>\s*'
    r'<figcaption>([^<]*)</figcaption>', re.S)



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
    <div class="deck__bar">
      <button class="deck__btn" type="button" data-deck-prev aria-label="Previous">
        <svg viewBox="0 0 24 24" aria-hidden="true"><polyline points="15,4 7,12 15,20"/></svg>
      </button>
      <div class="deck__meta">
        <p class="deck__cap"></p>
        <div class="deck__dots"></div>
      </div>
      <button class="deck__btn" type="button" data-deck-next aria-label="Next">
        <svg viewBox="0 0 24 24" aria-hidden="true"><polyline points="9,4 17,12 9,20"/></svg>
      </button>
    </div>
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
    body = read(source)
    plates = SLIDE.findall(body) or PLATE.findall(body)
    if not plates:
        raise SystemExit(f"no plates found in {source}")
    slides = [image_slide(src, alt, cap, i == 0)
              for i, (src, alt, cap) in enumerate(plates)]
    deck(out, title, desc, current, slides)


SHOWS = {
    "storyboards-coma-toes.html": {
        "title": "Coma Toes",
        "desc": "Coma Toes — storyboards and animatic by Uzoma Dunkwu.",
        "current": "coma",
        "views": [
            ("board", "Storyboard", "coma-toes", 529, "Coma Toes storyboard"),
            ("film", "Animatic", "oGPjcp5Oczc", 0, "Coma-Toes animatic"),
        ],
    },
    "storyboards-cash-trapped.html": {
        "title": "Cash Trapped",
        "desc": "Cash Trapped — storyboards and animatics by Uzoma Dunkwu.",
        "current": "cash",
        "views": [
            ("board", "Part 1 storyboard", "cash-trapped-1", 575, "Cash Trapped, part 1 storyboard"),
            ("film", "Part 1 animatic", "VWYWppKey5c", 0, "Cash-trapped animatic, part 1"),
            ("board", "Part 2 storyboard", "cash-trapped-2", 631, "Cash Trapped, part 2 storyboard"),
            ("film", "Part 2 animatic", "wxuEH9HT5Pc", 0, "Cash-trapped animatic, part 2"),
        ],
    },
}

SHOW = '''<!DOCTYPE html>
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
<section class="show" data-show>
  <div class="show__head">
    <h1 class="show__title">{title}</h1>
    <div class="show__tabs" role="tablist">
{tabs}
    </div>
  </div>
{views}
</section>
</main>

<script src="js/site.js"></script>
</body>
</html>
'''

ARROW_L = '<svg viewBox="0 0 24 24" aria-hidden="true"><polyline points="15,4 7,12 15,20"/></svg>'
ARROW_R = '<svg viewBox="0 0 24 24" aria-hidden="true"><polyline points="9,4 17,12 9,20"/></svg>'


def board_view(slug, count, label):
    return f'''  <div class="view view--board" data-count="{count}" data-path="boards/{slug}/">
    <div class="view__frame">
      <img class="view__page" src="boards/{slug}/0001.webp" alt="{label}" draggable="false" fetchpriority="high" decoding="async">
      <div class="view__bar">
        <button class="deck__btn" type="button" data-page-prev aria-label="Previous page">{ARROW_L}</button>
        <input class="view__scrub" type="range" min="1" max="{count}" value="1" step="1" aria-label="{label} page">
        <button class="deck__btn" type="button" data-page-next aria-label="Next page">{ARROW_R}</button>
      </div>
    </div>
  </div>'''


def film_view(video, label):
    return f'''  <div class="view view--film">
    <div class="view__frame">
      <div class="view__film">
        <iframe data-src="https://www.youtube.com/embed/{video}?rel=0" title="{label}"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
      </div>
    </div>
  </div>'''


def shows():
    for name, spec in SHOWS.items():
        tabs, views = [], []
        for n, (kind, label, ref, count, alt) in enumerate(spec["views"]):
            tabs.append(f'      <button class="show__tab" type="button" role="tab">{label}</button>')
            views.append(board_view(ref, count, alt) if kind == "board" else film_view(ref, alt))
        write(name, SHOW.format(title=spec["title"], desc=spec["desc"],
                                nav=nav(spec["current"]),
                                tabs=chr(10).join(tabs), views=chr(10).join(views)))


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
    print("shows:")
    shows()
    print("headers:")
    relink()


main()

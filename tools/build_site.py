"""
Builds every page on the site from content/*.yaml.

This replaced build_decks.py, which built the portfolio and storyboard
pages by scraping the plates and slides back out of already-generated
HTML. Content now lives in content/*.yaml instead — the CMS (see
admin/) edits those files directly, and this script is what turns an
edit into the actual pages. Run it after any change to content/, or
let Vercel run it as the site's build step (see vercel.json).

Pages fall into two groups:

  - Portfolio decks, storyboard shows, and the press page are fully
    regenerated from a template, the same way build_decks.py always
    did it — the whole file is data-driven, nothing hand-written left
    in them to protect.

  - index.html, about.html and contact.html are hand-built pages with
    far more one-off structure than a template is worth writing. Only
    the specific CMS-controlled fragments (the tagline, the bio
    paragraphs, the address) are patched in place by regex, the same
    way the shared header already was.

A CMS image upload lands in content/uploads/ as the original file the
client gave us; this script is also what turns that into the actual
served asset (the hero crop, the about-page photos), so the pixel work
those already had never has to be redone by hand.
"""

import datetime
import glob
import html
import os
import re

import yaml
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content")
UPLOADS = os.path.join(CONTENT, "uploads")


def load(name):
    with open(os.path.join(CONTENT, name), encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def read(name):
    with open(os.path.join(ROOT, name), encoding="utf-8") as fh:
        return fh.read()


def write(name, text):
    with open(os.path.join(ROOT, name), "w", encoding="utf-8") as fh:
        fh.write(text)
    print(f"  {name:34} {len(text) // 1024} KB")


def md_lite(text):
    """***bold+italic***, **bold** and *italic* — three independent,
    non-nesting spans, which is all the bio's award citations ever need.
    ***x*** exists because "for **X** where X is also *italic*" is what
    the source citations actually look like, and a real nested-emphasis
    parser is a lot of code for two sentences. Escape first so a stray
    < or & in someone's edit can't break the page."""
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*\*(.+?)\*\*\*", r"<strong><em>\1</em></strong>", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    return text


def esc_attr(text):
    """& < > " only — the site's own alt text always leaves a plain
    apostrophe as itself inside a double-quoted attribute, so this does
    too rather than turning every edit into &#x27; noise."""
    return (text.replace("&", "&amp;").replace("<", "&lt;")
                .replace(">", "&gt;").replace('"', "&quot;"))


def uploaded(stem):
    """content/uploads/<stem>.<ext>, whatever extension the CMS saved it
    with, or None if the client has never replaced this image."""
    matches = glob.glob(os.path.join(UPLOADS, stem + ".*"))
    return matches[0] if matches else None


def responsive_image(stem, widths, out_prefix):
    """Resize an uploaded source image to each of `widths`, writing
    {out_prefix}-{w}.jpg, and return the first width's (w, h) for the
    HTML width/height attributes. None if there's no upload to process,
    meaning the checked-in files are left exactly as they are."""
    src = uploaded(stem)
    if not src:
        return None
    im = Image.open(src).convert("RGB")
    sw, sh = im.size
    first = None
    for w in widths:
        h = round(w * sh / sw)
        if first is None:
            first = (w, h)
        out = f"{out_prefix}-{w}.jpg"
        im.resize((w, h), Image.LANCZOS).save(
            os.path.join(ROOT, out), "JPEG", quality=84, optimize=True, progressive=True)
        print(f"    {out:32} {w}x{h}")
    return first


# ------------------------------------------------------------------ chrome --

def nav(current):
    def m(key):
        return ' aria-current="page"' if key == current else ""
    return f'''  <a class="head__name" href="index.html">Uzoma Dunkwu</a>
  <nav class="head__nav" aria-label="Primary">
    <a href="about.html"{m("about")}>About</a>
    <a href="press.html"{m("press")}>Press</a>
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


def relink():
    """The pages that are not decks share the same header."""
    for name, current in [("index.html", None), ("about.html", "about"),
                          ("press.html", "press"), ("contact.html", "contact")]:
        s = read(name)
        s = re.sub(r'(<header class="head[^"]*">\n).*?(\n</header>)',
                   lambda m: m.group(1) + nav(current) + m.group(2), s, flags=re.S)
        write(name, s)


# ------------------------------------------------------------------- decks --

DECK_HEAD = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Uzoma Dunkwu</title>
<meta name="description" content="{desc}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' fill='%23fff'/%3E%3Crect x='8' y='8' width='16' height='16' fill='%23111'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://api.fontshare.com" crossorigin>
<link rel="preconnect" href="https://cdn.fontshare.com" crossorigin>
<link href="https://api.fontshare.com/v2/css?f[]=clash-display@500,600&f[]=satoshi@400,500,700&display=swap" rel="stylesheet">
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
    load_attr = ' fetchpriority="high"' if first else ' loading="lazy"'
    return f'''    <figure class="slide">
      <div class="slide__frame"><img src="{src}" alt="{alt}"{load_attr} decoding="async"></div>
      <figcaption>{caption}</figcaption>
    </figure>'''


WORK_PAGES = {
    "work-eyes-of-wakanda.html": ("content/work/eyes-of-wakanda.yaml", "eow"),
    "work-iyanu.html": ("content/work/iyanu.yaml", "iyanu"),
    "work-personal.html": ("content/work/personal.yaml", "personal"),
}


def decks():
    for name, (data_path, current) in WORK_PAGES.items():
        data = load(data_path.replace("content/", ""))
        slides = [image_slide(s["src"], s["alt"], s["caption"], i == 0)
                  for i, s in enumerate(data["slides"])]
        write(name, DECK_HEAD.format(title=data["title"], desc=data["desc"],
                                     nav=nav(current), slides="\n".join(slides)))


# ------------------------------------------------------------------- shows --

SHOW_HEAD = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Uzoma Dunkwu</title>
<meta name="description" content="{desc}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' fill='%23fff'/%3E%3Crect x='8' y='8' width='16' height='16' fill='%23111'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://api.fontshare.com" crossorigin>
<link rel="preconnect" href="https://cdn.fontshare.com" crossorigin>
<link href="https://api.fontshare.com/v2/css?f[]=clash-display@500,600&f[]=satoshi@400,500,700&display=swap" rel="stylesheet">
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


STORYBOARD_PAGES = {
    "storyboards-coma-toes.html": ("storyboards/coma-toes.yaml", "coma"),
    "storyboards-cash-trapped.html": ("storyboards/cash-trapped.yaml", "cash"),
}


def shows():
    for name, (data_path, current) in STORYBOARD_PAGES.items():
        data = load(data_path)
        tabs, views = [], []
        for v in data["views"]:
            tabs.append(f'      <button class="show__tab" type="button" role="tab">{v["label"]}</button>')
            views.append(board_view(v["ref"], v["count"], v["alt"]) if v["kind"] == "board"
                         else film_view(v["ref"], v["alt"]))
        write(name, SHOW_HEAD.format(title=data["title"], desc=data["desc"], nav=nav(current),
                                     tabs="\n".join(tabs), views="\n".join(views)))


# ------------------------------------------------------------------- press --

PRESS_HEAD = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Press — Uzoma Dunkwu</title>
<meta name="description" content="Press coverage of Uzoma Dunkwu's 2026 Emmy win for Marvel's Eyes of Wakanda.">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' fill='%23fff'/%3E%3Crect x='8' y='8' width='16' height='16' fill='%23111'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://api.fontshare.com" crossorigin>
<link rel="preconnect" href="https://cdn.fontshare.com" crossorigin>
<link href="https://api.fontshare.com/v2/css?f[]=clash-display@500,600&f[]=satoshi@400,500,700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/site.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>

<header class="head">
{nav}
</header>

<main id="main" class="mid">
<section class="intro">
  <h1 class="intro__title">Press</h1>
</section>

<ul class="press">
{items}
</ul>
</main>

<footer class="foot">
  <p class="foot__clients">{clients}</p>
  <p class="credit">Powered by <a href="{credit_url}" target="_blank" rel="noopener">{credit_text}</a></p>
</footer>

<script src="js/site.js"></script>
</body>
</html>
'''


def press_item(item):
    d = item["date"]
    d = d if isinstance(d, datetime.date) else datetime.date.fromisoformat(d)
    date = f"{d:%B} {d.day}, {d:%Y}"
    meta = date if not item.get("note") else f'{date} — {item["note"]}'
    return f'''  <li class="press__item">
    <span class="press__outlet">{item["outlet"]}</span>
    <a class="press__headline" href="{item["url"]}" target="_blank" rel="noopener">{item["headline"]}</a>
    <span class="press__meta">{meta}</span>
  </li>'''


def press(site):
    data = load("press.yaml")
    items = sorted(data["items"], key=lambda i: i["date"], reverse=True)
    write("press.html", PRESS_HEAD.format(
        nav=nav("press"), items="\n".join(press_item(i) for i in items),
        clients=" · ".join(site["footer_clients"]),
        credit_url=site["credit_url"], credit_text=site["credit_text"]))


# ------------------------------------------------------------- patched pages --

def patch(name, pattern, replacement, flags=re.S):
    s = read(name)
    new, n = re.subn(pattern, replacement, s, flags=flags)
    if n == 0:
        raise SystemExit(f"{name}: pattern not found — {pattern[:60]}")
    write(name, new)


def patch_index(site, about):
    responsive_image("hero-source", (2560, 1600, 1100), "assets/hero/dora")
    rest = html.escape(site["hero_rest"], quote=False) + "."
    # the last word pair joins across a non-breaking space rather than the
    # whole tail, matching how the hero line has always broken
    rest = re.sub(r'(\S+) (\S+\.)$', r'\1&nbsp;\2', rest)
    tagline = f'<span class="titlecard__lead">{html.escape(site["hero_lead"], quote=False)}</span> {rest}'
    patch("index.html",
          r'<a class="titlecard__line" href="about\.html">.*?</a>',
          f'<a class="titlecard__line" href="about.html">{tagline}</a>')


def patch_about(site, about):
    paras = "\n".join(f"  <p>{md_lite(p)}</p>" for p in about["bio"])
    patch("about.html", r'<section class="text">\s*.*?\s*</section>',
          f'<section class="text">\n{paras}\n</section>')
    patch("about.html", r'(art--emmy">\s*<img[^>]*alt=")[^"]*(")',
          rf'\g<1>{esc_attr(about["emmy_alt"])}\g<2>')
    patch("about.html", r'(art--award">\s*<img[^>]*alt=")[^"]*(")',
          rf'\g<1>{esc_attr(about["award_alt"])}\g<2>')
    emmy = responsive_image("emmy-source", (1080, 720), "assets/misc/eow-emmy")
    if emmy:
        patch("about.html", r'(art--emmy".*?width=")\d+(" height=")\d+(")',
              rf'\g<1>{emmy[0]}\g<2>{emmy[1]}\g<3>')
    award = responsive_image("award-source", (1180, 780), "assets/misc/caa-award")
    if award:
        patch("about.html", r'(art--award".*?width=")\d+(" height=")\d+(")',
              rf'\g<1>{award[0]}\g<2>{award[1]}\g<3>')
    patch("about.html", r'mailto:[^"]+', f'mailto:{site["email"]}')
    patch("about.html", r'(class="foot__mail"[^>]*>)[^<]+(</a>)', rf'\g<1>{site["email"]}\g<2>')
    patch_footer("about.html", site)


def patch_contact(site):
    patch("contact.html", r'mailto:[^"]+', f'mailto:{site["email"]}')
    patch("contact.html", r'(class="reach__mail"[^>]*>)[^<]+(</a>)', rf'\g<1>{site["email"]}\g<2>')
    patch_footer("contact.html", site)


def patch_footer(name, site):
    clients = " · ".join(site["footer_clients"])
    patch(name, r'(class="foot__clients">)[^<]*(</p>)', rf'\g<1>{clients}\g<2>')
    patch(name, r'(class="credit">Powered by <a href=")[^"]+(")([^>]*>)[^<]+(</a>)',
          rf'\g<1>{site["credit_url"]}\g<2>\g<3>{site["credit_text"]}\g<4>')


def main():
    site = load("site.yaml")
    about = load("about.yaml")

    print("decks:")
    decks()
    print("shows:")
    shows()
    print("press:")
    press(site)
    print("patched pages:")
    patch_index(site, about)
    patch_about(site, about)
    patch_contact(site)
    print("headers:")
    relink()


main()

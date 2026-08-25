# -*- coding: utf-8 -*-
"""
build_simple.py — generates the simple build in simple/.

Five static pages, one stylesheet, no JavaScript. Every image keeps its own
aspect ratio, which is read off the file so a portrait sheet never runs past
the fold. Run:  python tools/build_simple.py
"""
import os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "simple")

MAIL = "hello@uzomadunkwu.com"
SOCIAL = [
    ("Instagram", "https://www.instagram.com/uzomadunkwu"),
    ("LinkedIn", "https://www.linkedin.com/in/uzomadunkwu/"),
    ("YouTube", "https://www.youtube.com/channel/UCU9rpgl7qDSV2p3UXm0jS4g"),
    ("X", "https://x.com/UzomaDunkwu"),
]
CLIENTS = ("Marvel Animation · Lion Forge · Netflix Animation · Disney · Laika · "
           "Triggerfish · Psyop · Stoopid Buddy Stoodios · Scroll Entertainment")

NAV = [("Work", "index.html#work"), ("Storyboards", "storyboards.html"),
       ("About", "index.html#about"), ("Contact", "index.html#contact")]


def ratio(rel):
    with Image.open(os.path.join(ROOT, rel.replace("/", os.sep))) as im:
        return round(im.width / im.height, 4)


def head(title, desc, current=None):
    nav = "\n".join(
        '        <a href="{}"{}>{}</a>'.format(
            href, ' aria-current="page"' if label == current else "", label)
        for label, href in NAV)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' fill='%23fff'/%3E%3Crect x='8' y='8' width='16' height='16' fill='%23111'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://api.fontshare.com" crossorigin>
<link rel="preconnect" href="https://cdn.fontshare.com" crossorigin>
<link href="https://api.fontshare.com/v2/css?f[]=clash-display@500,600&f[]=satoshi@400,500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/site.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>

<header class="head">
  <a class="head__name" href="index.html">Uzoma Dunkwu</a>
  <nav class="head__nav" aria-label="Primary">
{nav}
  </nav>
</header>

<main id="main">
"""


FOOT = f"""</main>

<footer class="foot" id="contact">
  <a class="foot__mail" href="mailto:{MAIL}">{MAIL}</a>
  <div class="foot__links">
""" + "\n".join(
    f'    <a href="{url}" target="_blank" rel="noopener">{name}</a>' for name, url in SOCIAL
) + f"""
  </div>
  <p class="foot__clients">{CLIENTS}</p>
</footer>

</body>
</html>
"""


def plate(src, alt, caption="", lazy=True):
    r = ratio(src)
    lz = ' loading="lazy" decoding="async"' if lazy else ""
    cap = f"\n    <figcaption>{caption}</figcaption>" if caption else ""
    return (f'  <figure class="plate" style="--r: {r}">\n'
            f'    <img src="{src}" alt="{alt}"{lz}>{cap}\n'
            f'  </figure>\n')


# ------------------------------------------------------------------ work ---
# stem, title, alt
EOW = [
    ("eow-01-lineup.png", "Lion team lineup", "Five Lion team warriors in gold lion masks and layered violet wraps, standing in a row."),
    ("eow-02-noni.png", "Noni", "Noni: a portrait bust, a fighting stance in a blue wrap, and three grey action studies."),
    ("eow-03-noni-keys.png", "Noni", "Five costume passes on Noni: teal wrap, hooded cloak, mask and collar, pale robe, layered skirt."),
    ("eow-04-old-noni.png", "Old Noni", "An older Noni in an ochre cloak and violet skirt, with four white construction turnarounds."),
    ("eow-05-traveller.png", "Noni traveller", "Five travelling-costume variants built on grey mannequins with fur collars, beads and wraps."),
    ("eow-06-councilman.png", "High councilman", "A high councilman: base bodysuit, a mask study, three olive and violet draping variants."),
    ("eow-07-kuda.png", "Kuda", "Kuda, a broad man in a red and blue panelled tunic, drawn twice, with a slimmer youth in violet."),
    ("eow-08-tafari.png", "Tafari and Kuda", "Tafari in violet armour with a metal vambrace, standing with a younger figure."),
    ("eow-09-lion-guard.png", "Lion guard faces", "Six lion guard head studies with different hairlines, scars and headbands."),
    ("eow-10-chainmakers.png", "Lion chain makers", "Five armoured chain makers in helmets and studded leather, front and back."),
    ("eow-11-harem.png", "Harem captives", "Four figures in pale blue robes and gold headdresses."),
    ("eow-12-seamstresses.png", "Seamstresses", "Three seamstresses in teal and gold wraps, of different ages and builds."),
    ("eow-13-ethiopian.png", "Ethiopian soldiers", "A shield bearer, a spearman in a grey robe, and a commander with a gold disc shield."),
    ("eow-14-crowd.png", "Wakandan crowd, river tribe", "Four river tribe civilians in striped and beaded wraps, one in a wide woven hat."),
    ("eow-15-dora.png", "Style exploration, Dora", "Five torsos labelled Shakoo, B'Risa, Koi'Fay, Y'Fett and Le'illa, each with a geometric primitive and handwritten design notes."),
    ("eow-16-flashback.png", "Style exploration, flashback", "A rendered bald warrior bust in warm light, with the line drawing it came from."),
    ("eow-17-dora-02.png", "Style exploration, Dora", "Four vignettes of the Lion team together, annotated in red handwriting."),
    ("eow-18-crowd-02.png", "Wakandan crowd, mining tribe", "Four mining tribe figures in red checked cloth, beads and heavy sandals."),
    ("eow-19-crowd-03.png", "Wakandan crowd, merchant tribe", "Four merchants in deep blue and plum robes, one veiled."),
]

IYANU = [
    ("iyanu-01-ideation.jpg", "Ideation", "Three young Yoruba characters beside a photograph of a carved Lamidi Fakeye figure."),
    ("iyanu-02-exploration.jpg", "Exploration", "The three leads beside their line drawings."),
    ("iyanu-03-exploration.jpg", "Exploration", "A second pass on the same three characters, colour beside line."),
    ("iyanu-04-biyi.jpg", "Biyi", "Four line studies of Biyi in motion: a high kick, a leap, a low lunge, a running turn."),
    ("iyanu-05-biyi-02.jpg", "Biyi", "Biyi's model sheet: colour front view and line profile on height guides, with a forearm detail."),
    ("iyanu-06-0621.jpg", "Exploration", "A boy in a red tunic and a bearded man in a green and violet wrapper, against a height chart."),
    ("iyanu-07-0621-02.jpg", "Exploration", "The archer drawn full length with a blue bow and a quiver."),
]

PERSONAL = [
    ("personal-01-afro-ninja.png", "Afro ninja", "A hooded warrior in a blue cape, a grey action study, a forked blade and a tooled sheath."),
    ("personal-02-pirate.png", "Pirate boy, action poses", "A blond-braided pirate boy in seven action poses with a bow."),
    ("personal-03-vampire.png", "Vampire", "A scientist in a white lab coat, and the same woman as a crimson-caped vampire with a bat form."),
    ("personal-04-femme.png", "Femme fatale", "A woman in a green patterned kimono with hair sticks and a red ribbon, in four expressions."),
    ("personal-05-hands.png", "Hands", "Nineteen hand studies in flat warm greys."),
    ("personal-06-people.png", "People", "A sumo wrestler in a green yukata, a heavyset man in a blue polo, and a muscular figure from behind."),
    ("personal-07-mammal.png", "Mammal college", "A rhino, antelope, cheetah, gorilla and bush baby in school uniforms, with handwritten notes."),
    ("personal-08-gangster.png", "Female gangster", "A woman in leopard print and armour between two bears with gold arrows in their backs."),
    ("personal-09-sketches.jpg", "Character sketches", "Six expression studies of a woman in plaid and violet."),
    ("personal-10-dump.jpg", "Style dump", "A page of pencil heads and figures."),
    ("personal-11-futuristic.png", "Futuristic guy", "Three variants of a tall figure in grey armour with gold winged shoulders and a crested helm."),
    ("personal-12-sketch.png", "Sketches", "Three stylised women: one in a purple dress, one smoking, one seated."),
]

PROJECTS = {
    "eow": dict(file="work-eyes-of-wakanda.html", name="Eyes of Wakanda", dir="eow",
                meta="Marvel Animation · Character design", plates=EOW,
                title="Eyes of Wakanda — Uzoma Dunkwu",
                desc="Character design for Marvel Animation's Eyes of Wakanda by Uzoma Dunkwu."),
    "iyanu": dict(file="work-iyanu.html", name="Iyanu", dir="iyanu",
                  meta="Lion Forge Animation · Visual development", plates=IYANU,
                  title="Iyanu — Uzoma Dunkwu",
                  desc="Visual development for Lion Forge Animation's Iyanu by Uzoma Dunkwu."),
    "personal": dict(file="work-personal.html", name="Personal", dir="personal",
                     meta="Personal work", plates=PERSONAL,
                     title="Personal work — Uzoma Dunkwu",
                     desc="Personal character design work by Uzoma Dunkwu."),
}

FILMS = [
    ("Coma Toes", "coma-toes", 8, 4, "assets/video/coma-toes.mp4", "Coma Toes"),
    ("Cash Trapped, part 1", "cash-trapped-a", 8, 7, "assets/video/cash-trapped-a.mp4", "Cash Trapped, part 1"),
    ("Cash Trapped, part 2", "cash-trapped-b", 7, 5, "assets/video/cash-trapped-b.mp4", "Cash Trapped, part 2"),
]

ABOUT = [
    'I am a "self-taught" Nigerian Writer/Director and Visual Development Artist in Animation with over 10 years of experience. My works portraying authentic representation of African characters have gained local and international acclaim.',
    'Some of my accolades include a 2026 Primetime Creative Arts Emmy: Outstanding Individual Achievement In Animation, Character Design for <em>Eyes of Wakanda</em> and a 2025 Concept Art Association Award for Animated Series Character Concept – Noni, <em>Eyes of Wakanda</em> at LightBox Expo.',
    "The notable mainstream projects in my visual development portfolio are Marvel Animation's <em>Eyes of Wakanda</em> and Lion Forge's <em>Iyanu</em>. Other past studio clients include Netflix Animation, Disney, Laika, Triggerfish, Psyop and Stoopid Buddy Stoodios.",
    "In the course of my career, I've trained and mentored about 150 artists of various nationalities around the world. Passing on knowledge from my years of expertise is paramount to me. I hope to impact 1 million artists by 2036.",
    'In 2015, I founded Scroll Entertainment—an animation studio based in Lagos, Nigeria. I am currently directing my debut animated short with an Academy Award Winning Producer. The film is inspired by the daily struggle of an artist to create or conform.',
    'I love to draw and I do so everyday. So much so that I see my drawing skills atrophy after two weeks of hiatus. Some of the artworks I create are shared on my social media occasionally.',
]


def write(name, body):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(body)
    print("wrote simple/" + name)


def build_home():
    out = [head("Uzoma Dunkwu — Visual Development Artist",
                "Emmy and CAA Award-winning Visual Development Artist and Writer/Director in Animation.")]

    # Specified in Website Layout.pdf: "Landing Page Image (From eyes of
    # Wakanda)" is the five-head sheet, not the full-body lineup.
    hero = "assets/eow/eow-15-dora.png"
    out.append(f"""<section class="run" style="padding-top: var(--gap)">
  <figure class="plate" style="--r: {ratio(hero)}">
    <img src="{hero}" alt="Eyes of Wakanda: head-and-shoulders portraits of Shakoo, B'Risa, Koi'Fay, Y'Fett and Le'illa, each with the geometric shape that governs the design drawn beside it." fetchpriority="high">
  </figure>
</section>

<section class="intro">
  <h1 class="intro__title">Uzoma Dunkwu</h1>
  <p class="intro__line">Emmy &amp; CAA Award-winning Visual Development Artist and Writer/Director in Animation.</p>
</section>

<section class="work" id="work">
""")

    covers = [
        ("eow", "assets/eow/eow-02-noni.png",
         "Noni: a portrait bust, a fighting stance in a blue wrap, and three grey action studies."),
        ("iyanu", "assets/iyanu/iyanu-01-ideation.jpg",
         "Iyanu: three young Yoruba characters beside a carved Lamidi Fakeye reference."),
        ("personal", "assets/personal/personal-01-afro-ninja.png",
         "A hooded warrior in a blue cape with a forked blade, beside a grey action study."),
    ]
    for key, src, alt in covers:
        p = PROJECTS[key]
        out.append(f"""  <a class="work__item" style="--r: {ratio(src)}" href="{p['file']}">
    <img src="{src}" alt="{alt}" loading="lazy" decoding="async">
    <span class="work__label">
      <span class="work__title">{p['name']}</span>
      <span class="work__meta">{p['meta']}</span>
    </span>
  </a>
""")

    board = "assets/thumbs/boards/cash-trapped-a-f07.jpg"
    out.append(f"""  <a class="work__item" style="--r: {ratio(board)}" href="storyboards.html">
    <img src="{board}" alt="Cash Trapped: a storyboard panel, black line over flat washes." loading="lazy" decoding="async">
    <span class="work__label">
      <span class="work__title">Storyboards</span>
      <span class="work__meta">Two films · 23 panels</span>
    </span>
  </a>
</section>

<section class="text" id="about">
  <h2>About</h2>
""")
    for para in ABOUT:
        out.append(f"  <p>{para}</p>\n")
    out.append("</section>\n")
    out.append(FOOT)
    write("index.html", "".join(out))


def build_project(key):
    p = PROJECTS[key]
    out = [head(p["title"], p["desc"])]
    out.append(f"""<section class="intro">
  <h1 class="intro__title">{p['name']}</h1>
  <p class="facts"><span>{p['meta']}</span><span>{len(p['plates'])} sheets</span></p>
</section>

<section class="run">
""")
    for i, (stem, title, alt) in enumerate(p["plates"]):
        out.append(plate(f"assets/{p['dir']}/{stem}", alt, title, lazy=i > 0))
    out.append("</section>\n")

    order = ["eow", "iyanu", "personal"]
    nxt = PROJECTS[order[(order.index(key) + 1) % 3]]
    out.append(f"""<section class="intro">
  <p class="facts">Next</p>
  <h2 class="intro__title"><a href="{nxt['file']}">{nxt['name']}</a></h2>
</section>
""")
    out.append(FOOT)
    write(p["file"], "".join(out))


def build_boards():
    out = [head("Storyboards — Uzoma Dunkwu",
                "Storyboards and animatics for Coma Toes and Cash Trapped by Uzoma Dunkwu.",
                current="Storyboards")]
    out.append("""<section class="intro">
  <h1 class="intro__title">Storyboards</h1>
  <p class="facts"><span>Two films</span><span>23 panels</span></p>
</section>
""")
    for name, prefix, count, poster, video, label in FILMS:
        out.append(f"""
<section class="film">
  <h2 class="film__title">{name}</h2>
  <video src="{video}" controls muted loop playsinline preload="none"
         poster="assets/thumbs/boards/{prefix}-f{poster:02d}.jpg" aria-label="{label} animatic"></video>
  <div class="frames">
""")
        for n in range(1, count + 1):
            out.append(f'    <img src="assets/thumbs/boards/{prefix}-f{n:02d}.jpg" '
                       f'alt="{label}: storyboard panel {n}." loading="lazy" decoding="async">\n')
        out.append("  </div>\n</section>\n")

    out.append("""
<section class="intro">
  <p class="facts">Next</p>
  <h2 class="intro__title"><a href="work-eyes-of-wakanda.html">Eyes of Wakanda</a></h2>
</section>
""")
    out.append(FOOT)
    write("storyboards.html", "".join(out))


if __name__ == "__main__":
    build_home()
    for k in PROJECTS:
        build_project(k)
    build_boards()
    print("== DONE ==")

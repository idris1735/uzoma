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

MAIL = "uzomadunkwu@gmail.com"
ICONS = {
    "instagram": '<svg viewBox="0 0 24 24" width="24" height="24" fill="currentColor" aria-hidden="true" focusable="false"><path d="M12 0C8.74 0 8.333.015 7.053.072 5.775.132 4.905.333 4.14.63c-.789.306-1.459.717-2.126 1.384S.935 3.35.63 4.14C.333 4.905.131 5.775.072 7.053.012 8.333 0 8.74 0 12s.015 3.667.072 4.947c.06 1.277.261 2.148.558 2.913.306.788.717 1.459 1.384 2.126.667.666 1.336 1.079 2.126 1.384.766.296 1.636.499 2.913.558C8.333 23.988 8.74 24 12 24s3.667-.015 4.947-.072c1.277-.06 2.148-.262 2.913-.558.788-.306 1.459-.718 2.126-1.384.666-.667 1.079-1.335 1.384-2.126.296-.765.499-1.636.558-2.913.06-1.28.072-1.687.072-4.947s-.015-3.667-.072-4.947c-.06-1.277-.262-2.149-.558-2.913-.306-.789-.718-1.459-1.384-2.126C21.319 1.347 20.651.935 19.86.63c-.765-.297-1.636-.499-2.913-.558C15.667.012 15.26 0 12 0zm0 2.16c3.203 0 3.585.016 4.85.071 1.17.055 1.805.249 2.227.415.562.217.96.477 1.382.896.419.42.679.819.896 1.381.164.422.36 1.057.413 2.227.057 1.266.07 1.646.07 4.85s-.015 3.585-.074 4.85c-.061 1.17-.256 1.805-.421 2.227-.224.562-.479.96-.899 1.382-.419.419-.824.679-1.38.896-.42.164-1.065.36-2.235.413-1.274.057-1.649.07-4.859.07-3.211 0-3.586-.015-4.859-.074-1.171-.061-1.816-.256-2.236-.421-.569-.224-.96-.479-1.379-.899-.421-.419-.69-.824-.9-1.38-.165-.42-.359-1.065-.42-2.235-.045-1.26-.061-1.649-.061-4.844 0-3.196.016-3.586.061-4.861.061-1.17.255-1.814.42-2.234.21-.57.479-.96.9-1.381.419-.419.81-.689 1.379-.898.42-.166 1.051-.361 2.221-.421 1.275-.045 1.65-.06 4.859-.06l.045.03zm0 3.678c-3.405 0-6.162 2.76-6.162 6.162 0 3.405 2.76 6.162 6.162 6.162 3.405 0 6.162-2.76 6.162-6.162 0-3.405-2.76-6.162-6.162-6.162zM12 16c-2.21 0-4-1.79-4-4s1.79-4 4-4 4 1.79 4 4-1.79 4-4 4zm7.846-10.405c0 .795-.646 1.44-1.44 1.44-.795 0-1.44-.646-1.44-1.44 0-.794.646-1.439 1.44-1.439.793-.001 1.44.645 1.44 1.439z"/></svg>',
    "linkedin": '<svg viewBox="0 0 24 24" width="24" height="24" fill="currentColor" aria-hidden="true" focusable="false"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.225 0z"/></svg>',
    "youtube": '<svg viewBox="0 0 24 24" width="24" height="24" fill="currentColor" aria-hidden="true" focusable="false"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>',
    "x": '<svg viewBox="0 0 24 24" width="24" height="24" fill="currentColor" aria-hidden="true" focusable="false"><path d="M18.901 1.153h3.68l-8.04 9.19L24 22.846h-7.406l-5.8-7.584-6.638 7.584H.474l8.6-9.83L0 1.154h7.594l5.243 6.932ZM17.61 20.644h2.039L6.486 3.24H4.298Z"/></svg>',
}

SOCIAL = [
    ("Instagram", "instagram", "https://www.instagram.com/uzomadunkwu"),
    ("LinkedIn", "linkedin", "https://www.linkedin.com/in/uzomadunkwu/"),
    ("YouTube", "youtube", "https://www.youtube.com/channel/UCU9rpgl7qDSV2p3UXm0jS4g"),
    ("X", "x", "https://x.com/UzomaDunkwu"),
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
    f'    <a class="social social--{key}" href="{url}" target="_blank" rel="noopener" aria-label="{name}">{ICONS[key]}</a>'
    for name, key, url in SOCIAL
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

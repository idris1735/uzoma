# -*- coding: utf-8 -*-
"""
build_pages.py — generates the case-study pages and the storyboard page.

Captions and alt text are authored here, next to the data they describe.
Run after adding artwork:  python tools/build_pages.py
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">

  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' fill='%230B0A0D'/%3E%3Crect x='7.5' y='7.5' width='17' height='17' fill='none' stroke='%23A3FF12' stroke-width='2.5'/%3E%3C/svg%3E">

  <link rel="preconnect" href="https://api.fontshare.com" crossorigin>
  <link rel="preconnect" href="https://cdn.fontshare.com" crossorigin>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

  <link href="https://api.fontshare.com/v2/css?f[]=clash-display@200,300,400,500,600,700&f[]=satoshi@300,400,500,700&display=swap" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">

  <link rel="stylesheet" href="css/base.css">
  <link rel="stylesheet" href="css/type.css">
  <link rel="stylesheet" href="css/work.css">

  <!-- arriving from another sheet? the curtain is already down -->
  <script>try{{if(sessionStorage.getItem("uz-transit"))document.documentElement.classList.add("is-arriving")}}catch(e){{}}</script>
{preload}</head>
<body>
  <a class="u-skip" href="#plates">Skip to content</a>
  <div class="grain" aria-hidden="true"></div>

  <header class="site-head">
    <a class="site-head__mark" href="index.html" aria-label="Uzoma Dunkwu — home">
      <span class="anno anno--bone">UZOMA DUNKWU</span>
      <svg class="site-head__shape" viewBox="0 0 24 24" aria-hidden="true">
        <rect x="5" y="5" width="14" height="14"/>
      </svg>
    </a>

    <input class="nav-toggle" type="checkbox" id="nav-toggle" aria-hidden="true">
    <label class="nav-toggle-btn" for="nav-toggle" aria-label="Menu">
      <span class="nav-toggle-btn__bar"></span>
      <span class="nav-toggle-btn__bar"></span>
    </label>

    <nav class="site-nav" aria-label="Primary">
      <ul class="site-nav__list">
        <li><a class="site-nav__link" href="index.html#about">ABOUT</a></li>
        <li class="site-nav__drop">
          <a class="site-nav__link" href="index.html#portfolio">PORTFOLIO</a>
          <ul class="site-nav__sub">
            <li><a class="site-nav__link"{cur_eow} href="work-eyes-of-wakanda.html">EYES OF WAKANDA</a></li>
            <li><a class="site-nav__link"{cur_iyanu} href="work-iyanu.html">IYANU</a></li>
            <li><a class="site-nav__link"{cur_personal} href="work-personal.html">PERSONAL</a></li>
          </ul>
        </li>
        <li><a class="site-nav__link"{cur_boards} href="storyboards.html">STORYBOARDS</a></li>
        <li><a class="site-nav__link" href="index.html#products">PRODUCTS</a></li>
        <li><a class="site-nav__link" href="index.html#contact">CONTACT</a></li>
      </ul>
    </nav>
  </header>

  <main>
"""

FOOT = """  </main>

  <footer class="footer" id="contact" aria-label="Contact">
    <div class="footer__marquee" aria-hidden="true">
      <div class="footer__marquee-track">
        <span>MARVEL ANIMATION · LION FORGE · NETFLIX ANIMATION · DISNEY · LAIKA · TRIGGERFISH · PSYOP · STOOPID BUDDY STOODIOS · SCROLL ENTERTAINMENT ·&nbsp;</span>
        <span>MARVEL ANIMATION · LION FORGE · NETFLIX ANIMATION · DISNEY · LAIKA · TRIGGERFISH · PSYOP · STOOPID BUDDY STOODIOS · SCROLL ENTERTAINMENT ·&nbsp;</span>
      </div>
    </div>

    <div class="footer__body">
      <div class="footer__socials">
        <a class="footer__social anno" href="https://www.instagram.com/uzomadunkwu" target="_blank" rel="noopener" data-scramble>INSTAGRAM</a>
        <a class="footer__social anno" href="https://www.linkedin.com/in/uzomadunkwu/" target="_blank" rel="noopener" data-scramble>LINKEDIN</a>
        <a class="footer__social anno" href="https://www.youtube.com/channel/UCU9rpgl7qDSV2p3UXm0jS4g" target="_blank" rel="noopener" data-scramble>YOUTUBE</a>
        <a class="footer__social anno" href="https://x.com/UzomaDunkwu" target="_blank" rel="noopener" data-scramble>X</a>
      </div>
      <a class="footer__email display" href="mailto:hello@uzomadunkwu.com" data-scramble>HELLO@UZOMADUNKWU.COM</a>
    </div>

    <div class="footer__name" aria-hidden="true"><span class="display">UZOMA DUNKWU</span></div>
  </footer>

  <script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"
          integrity="sha384-g4NTh/Iv5PPU4xPyhEWqPcwtNXOvdaDI8LLnyYfyNZOjKJeYQyjzQ9X5275eBjpt" crossorigin="anonymous"></script>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/ScrollTrigger.min.js"
          integrity="sha384-Z3REaz79l2IaAZqJsSABtTbhjgOUYyV3p90XNnAPCSHg3EMTz1fouunq9WZRtj3d" crossorigin="anonymous"></script>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/ScrollToPlugin.min.js"
          integrity="sha384-RVPQwTb0fPz9kI8s5GwAq1Qioto9fnEQt1aKGSQSm8xV6+DIdBSgcCShoHqfKnhv" crossorigin="anonymous"></script>
  <script src="https://cdn.jsdelivr.net/npm/lenis@1.1.14/dist/lenis.min.js"
          integrity="sha384-O55L/6rhHr9CFvrxqv5luxOCcmVaBmETbZbJDP+Do8T0pztTACsFBD/IXCNkj7DV" crossorigin="anonymous"></script>
  <script src="https://cdn.jsdelivr.net/npm/split-type@0.3.4/umd/index.min.js"
          integrity="sha384-wQImCCD/id1jPTwSloatzKlEpnEAQ5aH8H2Ud27FnNcJ1lf2+hB75ctoWnWxyD8X" crossorigin="anonymous"></script>

  <script src="js/cursor.js"></script>
  <script src="js/transitions.js"></script>
  <script src="js/core.js"></script>
  <script src="js/{page_js}"></script>
</body>
</html>
"""

# ------------------------------------------------------------------- work ---
# (file stem, aspect w/h, title, alt text)
# Titles use the artist's own names for the pieces, taken from the source
# folder rather than invented here.
EOW = [
    ("eow-02-noni", 1800 / 990, "Noni",
     "Noni: portrait bust, a fighting stance in a blue wrap, and three grey action studies."),
    ("eow-03-noni-keys", 1800 / 1020, "Noni",
     "Five costume passes on Noni: teal wrap, hooded travelling cloak, mask and collar, pale robe, layered skirt."),
    ("eow-04-old-noni", 1800 / 1011, "Old Noni",
     "An older Noni in an ochre cloak and violet skirt, with four white construction turnarounds of the same garment."),
    ("eow-05-traveller", 1800 / 1321, "Noni traveller",
     "Five travelling-costume variants, A to D, built on grey mannequins with fur collars, beads and layered wraps."),
    ("eow-06-councilman", 1800 / 1241, "High councilman",
     "A high councilman: base bodysuit, a mask study, and three olive and violet draping variants."),
    ("eow-07-kuda", 1800 / 1383, "Kuda",
     "Kuda, a broad man in a red and blue panelled tunic, drawn twice, with a slimmer youth in violet."),
    ("eow-08-tafari", 1800 / 2027, "Tafari and Kuda",
     "Tafari in violet armour with a metal vambrace, standing with a younger figure in a patterned tunic."),
    ("eow-09-lion-guard", 1800 / 1781, "Lion guard faces",
     "Six lion guard head studies, A to F, with different hairlines, scars and headbands."),
    ("eow-10-chainmakers", 1800 / 798, "Lion chain makers",
     "Five armoured chain makers in helmets and studded leather, drawn front and back."),
    ("eow-11-harem", 1800 / 940, "Harem captives",
     "Four figures in pale blue robes and gold headdresses, two with arms out to show the garment."),
    ("eow-12-seamstresses", 1800 / 1467, "Seamstresses",
     "Three seamstresses, A to C, in teal and gold wraps, of different ages and builds."),
    ("eow-13-ethiopian", 1800 / 1387, "Ethiopian soldiers",
     "Three Ethiopian soldiers: a shield bearer, a spearman in a grey robe, and a commander with a gold disc shield."),
    ("eow-14-crowd", 1800 / 1336, "Wakandan crowd, river tribe",
     "Four river tribe civilians in striped and beaded wraps, one in a wide woven hat, with a hair detail study."),
    ("eow-15-dora", 1800 / 915, "Style exploration, Dora",
     "Five torsos labelled Shakoo, B'Risa, Koi'Fay, Y'Fett and Le'illa, each with a geometric primitive and handwritten design notes beside it."),
    ("eow-16-flashback", 1800 / 1358, "Style exploration, flashback",
     "A rendered bald warrior bust in warm light, with the line drawing it came from."),
    ("eow-17-dora-02", 1800 / 983, "Style exploration, Dora",
     "Four vignettes of the Lion team together, annotated in red handwriting."),
    ("eow-18-crowd-02", 1800 / 1177, "Wakandan crowd, mining tribe",
     "Four mining tribe figures in red checked cloth, beads and heavy sandals."),
    ("eow-19-crowd-03", 1800 / 1108, "Wakandan crowd, merchant tribe",
     "Four merchants in deep blue and plum robes, one veiled, one in an embroidered coat."),
]

IYANU = [
    ("iyanu-02-exploration", 1800 / 787, "Exploration",
     "The three leads beside their line drawings: an archer in red, a figure in a green wrapper, a boy in a magenta tunic."),
    ("iyanu-03-exploration", 1800 / 1095, "Exploration",
     "A second pass on the same three characters, colour beside line."),
    ("iyanu-04-biyi", 1800 / 1354, "Biyi",
     "Four line studies of Biyi in motion: a high kick, a leap, a low lunge, a running turn."),
    ("iyanu-05-biyi-02", 1800 / 1500, "Biyi",
     "Biyi's model sheet: colour front view and line profile on height guides, with a forearm detail and a carved Lamidi Fakeye figure as reference."),
    ("iyanu-06-0621", 1800 / 1693, "Exploration",
     "A boy in a red tunic and a bearded man in a green and violet wrapper, against a numbered height chart."),
    ("iyanu-07-0621-02", 1800 / 2045, "Exploration",
     "The archer drawn full length with a blue bow and a quiver, in a red and orange wrapper."),
]

PERSONAL = [
    ("personal-02-pirate", 1600 / 900, "Pirate boy, action poses",
     "A blond-braided pirate boy in seven action poses, with a bow, a broken arrow and a tumbling fall."),
    ("personal-03-vampire", 1600 / 900, "Vampire",
     "A scientist in a white lab coat, and the same woman as a crimson-caped vampire with a bat form, holding a vial."),
    ("personal-04-femme", 1600 / 800, "Femme fatale",
     "A woman in a green patterned kimono with hair sticks and a red ribbon, in four expressions."),
    ("personal-05-hands", 1600 / 800, "Hands",
     "Nineteen hand studies, gripping, pointing, relaxed and clawed, in flat warm greys."),
    ("personal-06-people", 1600 / 800, "People",
     "Three figures: a sumo wrestler in a green yukata, a heavyset man in a blue polo, and a muscular figure from behind."),
    ("personal-07-mammal", 1600 / 800, "Mammal college",
     "A rhino, antelope, cheetah, gorilla and bush baby in school uniforms, each with a handwritten note on temperament."),
    ("personal-08-gangster", 1600 / 1597, "Female gangster",
     "A woman in leopard print and armour between two bears with gold arrows in their backs, on a flat grey field."),
    ("personal-09-sketches", 1600 / 1600, "Character sketches",
     "Six expression studies of a woman in plaid and violet."),
    ("personal-10-dump", 1600 / 1602, "Style dump",
     "A page of pencil heads and figures: brides, old men, a grinning face, a woman in a wrapper."),
    ("personal-11-futuristic", 1600 / 1600, "Futuristic guy",
     "Three variants, A to C, of a tall figure in grey armour with gold winged shoulders and a crested helm."),
    ("personal-12-sketch", 1600 / 1600, "Sketches",
     "Three stylised women: one in a purple dress, one smoking, one seated."),
]

PROJECTS = {
    "eow": {
        "slug": "work-eyes-of-wakanda.html",
        "title": "Eyes of Wakanda — Uzoma Dunkwu",
        "desc": "Character design for Marvel Animation's Eyes of Wakanda by Uzoma Dunkwu.",
        "name": "EYES OF<br>WAKANDA",
        "aria": "Eyes of Wakanda",
        "facts": [("CLIENT", "Marvel Animation"), ("ROLE", "Character design"),
                  ("SHEETS", "19")],
        "intro": "Five warriors, a city and everyone in it. The Lion team was built the way every character here is built — a primitive first, a silhouette that reads at ten per cent, then the person. Noni, the design at the centre of it, took the 2025 Concept Art Association award; the series took the 2026 Emmy for character design.",
        "hero": ("eow/eow-01-lineup.png", 2560 / 1348,
                 "Eyes of Wakanda: five Lion team warriors — Shakoo, B'Risa, Koi'Fay, Y'Fett and Le'illa — in gold lion masks and layered violet wraps, on one annotated concept sheet."),
        "scrub": ("eow/eow-02-noni", 1800 / 990, "NONI"),
        "lead": "Lion team lineup",
        "dir": "eow",
        "plates": EOW,
        "next": ("work-iyanu.html", "IYANU", "LION FORGE · VISUAL DEVELOPMENT",
                 "assets/thumbs/iyanu/iyanu-01-ideation.jpg"),
    },
    "iyanu": {
        "slug": "work-iyanu.html",
        "title": "Iyanu — Uzoma Dunkwu",
        "desc": "Visual development for Lion Forge Animation's Iyanu by Uzoma Dunkwu.",
        "name": "IYANU",
        "aria": "Iyanu",
        "facts": [("CLIENT", "Lion Forge Animation"), ("ROLE", "Visual development"),
                  ("SHEETS", "7")],
        "intro": "A Yoruba world, so the reference is Yoruba. The carvings of Lamidi Fakeye sit pinned to these sheets — the proportion of the head, the set of the shoulders, the way pattern wraps a body — and the characters are drawn out of them rather than onto them.",
        "hero": ("iyanu/iyanu-01-ideation.jpg", 1800 / 1095,
                 "Iyanu ideation sheet: three young Yoruba characters — an archer in red, a figure in a green wrapper, a boy in a magenta tunic — beside a photograph of a carved Lamidi Fakeye figure."),
        "scrub": ("iyanu/iyanu-01-ideation", 1800 / 1095, "IDEATION"),
        "lead": "Ideation",
        "dir": "iyanu",
        "plates": IYANU,
        "next": ("work-personal.html", "PERSONAL", "PERSONAL WORK",
                 "assets/thumbs/personal/personal-01-afro-ninja.jpg"),
    },
    "personal": {
        "slug": "work-personal.html",
        "title": "Personal work — Uzoma Dunkwu",
        "desc": "Personal character design work by Uzoma Dunkwu.",
        "name": "PERSONAL",
        "aria": "Personal work",
        "facts": [("ROLE", "Personal work"), ("SHEETS", "12")],
        "intro": "“I love to draw and I do so everyday. So much so that I see my drawing skills atrophy after two weeks of hiatus.” This is what that looks like: no brief, no notes, nineteen hands on one page because the hands were not working that week.",
        "hero": ("personal/personal-01-afro-ninja.png", 1.0,
                 "A hooded warrior in a blue cape and grey wrapped trousers, drawn beside a grey action study, a forked blade and a tooled sheath."),
        "scrub": ("personal/personal-01-afro-ninja", 1.0, "AFRO NINJA"),
        "lead": "Afro ninja",
        "dir": "personal",
        "plates": PERSONAL,
        "next": ("work-eyes-of-wakanda.html", "EYES OF WAKANDA", "MARVEL ANIMATION · CHARACTER DESIGN",
                 "assets/thumbs/eow/eow-01-lineup.jpg"),
    },
}

STAGES = [("sketch", "SKETCH"), ("line", "LINE"), ("flat", "FLATS"), ("final", "RENDER")]


def nav_flags(active):
    f = {k: "" for k in ("cur_eow", "cur_iyanu", "cur_personal", "cur_boards")}
    if active:
        f[f"cur_{active}"] = ' aria-current="page"'
    return f


def build_case(key):
    p = PROJECTS[key]
    hero_src, hero_ratio, hero_alt = p["hero"]
    scrub_stem, scrub_ratio, scrub_label = p["scrub"]

    preload = f'\n  <link rel="preload" as="image" href="assets/{hero_src}" fetchpriority="high">\n'
    out = [HEAD.format(title=p["title"], desc=p["desc"], preload=preload, **nav_flags(key))]

    facts = "\n".join(
        f'          <div class="case__fact"><dt>{t}</dt><dd>{v}</dd></div>'
        for t, v in p["facts"])

    out.append(f"""    <section class="case" aria-label="{p['aria']}">
      <div class="case__lamp" aria-hidden="true"></div>

      <div class="case__head">
        <h1 class="case__title display display--optical" data-reveal="lines">{p['name']}</h1>
        <dl class="case__facts">
{facts}
        </dl>
      </div>

      <figure class="case__sheet sheet" data-reveal="plate">
        <img src="assets/{hero_src}" alt="{hero_alt}" fetchpriority="high">
      </figure>
    </section>

    <section class="scrub" aria-label="Process">
      <div class="scrub__head">
        <h2 class="display" data-reveal="lines">PROCESS</h2>
        <p class="anno anno--dim">{scrub_label}<span class="scrub__hint">. DRAG, OR USE THE ARROW KEYS.</span></p>
      </div>

      <div class="scrub__stage" data-scrub style="--stage-ratio: {scrub_ratio:.4f}">
""")

    for i, (stem, _) in enumerate(STAGES):
        src = f"assets/{scrub_stem}-{stem}.jpg" if stem != "final" else f"assets/{scrub_stem}.{'png' if key != 'iyanu' else 'jpg'}"
        out.append(f'        <img class="scrub__pass scrub__pass--{i + 1}" src="{src}" alt="" aria-hidden="true" loading="lazy">\n')

    out.append(f"""        <span class="scrub__handle" aria-hidden="true">
          <span class="scrub__grip"><svg viewBox="0 0 24 24"><polyline points="10,7 5,12 10,17"/><polyline points="14,7 19,12 14,17"/></svg></span>
        </span>
        <input class="scrub__input" type="range" min="0" max="1000" value="0" step="1"
               aria-label="Drawing stage: sketch to finished render">
      </div>

      <ul class="scrub__stages">
""")
    for i, (_, label) in enumerate(STAGES):
        on = " is-on" if i == 0 else ""
        out.append(f'        <li class="scrub__stage-name{on}" data-stage="{i}">{label}</li>\n')

    out.append(f"""      </ul>
    </section>

    <section class="plates" id="plates" aria-label="Every sheet">
      <div class="plates__head">
        <h2 class="display" data-reveal="lines">SHEETS</h2>
        <p class="anno anno--dim">{len(p['plates']) + 1} IN TOTAL</p>
      </div>

      <div class="plates__grid">
""")

    plates = [(p["hero"][0].split("/")[1].rsplit(".", 1)[0], hero_ratio, p["lead"], hero_alt)] + [
        (stem, ratio, title, alt) for stem, ratio, title, alt in p["plates"]]

    for n, (stem, ratio, title, alt) in enumerate(plates, start=1):
        wide = " plate--wide" if ratio >= 1.75 else ""
        full = f"assets/{p['dir']}/{stem}"
        full += ".png" if os.path.exists(os.path.join(ROOT, "assets", p["dir"], stem + ".png")) else ".jpg"
        thumb = f"assets/thumbs/{p['dir']}/{stem}.jpg"
        out.append(f"""        <figure class="plate{wide}">
          <button class="plate__btn" type="button" data-plate="{full}" data-title="{title}" data-no="{n:02d}" data-reveal="plate">
            <img src="{thumb}" alt="{alt}" loading="lazy" width="900" height="{round(900 / ratio)}">
          </button>
          <figcaption class="plate__cap">
            <span class="anno plate__no">{n:02d}</span>
            <span class="anno plate__title">{title}</span>
          </figcaption>
        </figure>
""")

    nxt_href, nxt_name, nxt_studio, nxt_img = p["next"]
    out.append(f"""      </div>
    </section>

    <section class="next-work" aria-label="Next project">
      <a class="next-work__link" href="{nxt_href}">
        <span class="slug">NEXT PROJECT</span>
        <span class="next-work__title display display--optical">{nxt_name}</span>
        <span class="anno anno--dim">{nxt_studio}</span>
      </a>
      <img class="next-work__peek" src="{nxt_img}" alt="" aria-hidden="true" loading="lazy">
    </section>
""")

    out.append(FOOT.format(page_js="work.js"))
    path = os.path.join(ROOT, p["slug"])
    with open(path, "w", encoding="utf-8") as f:
        f.write("".join(out))
    print("wrote", p["slug"], f"({len(plates)} plates)")


# ------------------------------------------------------------- storyboards ---
FILMS = [
    {
        "id": "coma-toes", "title": "COMA TOES",
        "meta": ["08 PANELS", "INSTAGRAM CUT"],
        "prefix": "coma-toes", "count": 8, "poster": 4, "video": "assets/video/coma-toes.mp4",
        "alt": "Coma Toes: storyboard panel {n}.",
    },
    {
        "id": "cash-trapped", "title": "CASH TRAPPED, PART 1",
        "meta": ["08 PANELS"],
        "prefix": "cash-trapped-a", "count": 8, "poster": 7, "video": "assets/video/cash-trapped-a.mp4",
        "alt": "Cash Trapped, part 1: storyboard panel {n}.",
    },
    {
        "id": "cash-trapped-two", "title": "CASH TRAPPED, PART 2",
        "meta": ["07 PANELS"],
        "prefix": "cash-trapped-b", "count": 7, "poster": 5, "video": "assets/video/cash-trapped-b.mp4",
        "alt": "Cash Trapped, part 2: storyboard panel {n}.",
    },
]


def frame_ratio(prefix):
    """Board frames are letterbox-trimmed by prep_v2, so read it off the file."""
    from PIL import Image
    with Image.open(os.path.join(ROOT, "assets", "thumbs", "boards", f"{prefix}-f01.jpg")) as im:
        return round(im.width / im.height, 4)


def build_boards():
    out = [HEAD.format(
        title="Storyboards — Uzoma Dunkwu",
        desc="Storyboards and animatics for Coma Toes and Cash Trapped, boarded and cut by Uzoma Dunkwu.",
        preload="", **nav_flags("boards"))]

    out.append("""    <section class="case" aria-label="Storyboards">
      <div class="case__lamp" aria-hidden="true"></div>
      <div class="case__head">
        <p class="slug">SEQUENCES</p>
        <h1 class="case__title display display--optical" data-reveal="lines">STORY<br>BOARDS</h1>
        <dl class="case__facts">
          <div class="case__fact"><dt>ROLE</dt><dd>Storyboards, animatic</dd></div>
          <div class="case__fact"><dt>FILMS</dt><dd>Two</dd></div>
          <div class="case__fact"><dt>PANELS</dt><dd>23</dd></div>
        </dl>
      </div>
    </section>
""")

    for i, f in enumerate(FILMS):
        alt = " film--alt" if i % 2 else ""
        ratio = frame_ratio(f["prefix"])
        meta = "\n".join(f'          <span class="anno anno--dim">{m}</span>' for m in f["meta"])
        out.append(f"""
    <section class="film{alt}" id="{f['id']}" aria-label="{f['title']}">
      <div class="film__head">
        <h2 class="film__title display display--optical" data-reveal="lines">{f['title']}</h2>
        <div class="film__meta">
{meta}
        </div>
      </div>

      <div class="film__strip" data-strip>
""")
        for n in range(1, f["count"] + 1):
            out.append(f"""        <figure class="frame" style="--frame-ratio: {ratio}">
          <img src="assets/thumbs/boards/{f['prefix']}-f{n:02d}.jpg" alt="{f['alt'].format(n=n)}" loading="lazy">
          <figcaption class="frame__no">{n:02d}</figcaption>
        </figure>
""")
        out.append(f"""      </div>

      <div class="film__player">
        <video class="film__video" src="{f['video']}" muted loop playsinline preload="none"
               poster="assets/thumbs/boards/{f['prefix']}-f{f['poster']:02d}.jpg"
               aria-label="{f['title']} animatic"></video>
        <button class="film__play anno" type="button" data-play>
          <svg viewBox="0 0 24 24" aria-hidden="true"><polygon points="6,4 20,12 6,20"/></svg>
          <span data-play-label>PLAY THE ANIMATIC</span>
        </button>
      </div>
    </section>
""")

    out.append("""
    <section class="next-work" aria-label="Next">
      <a class="next-work__link" href="work-eyes-of-wakanda.html">
        <span class="slug">NEXT PROJECT</span>
        <span class="next-work__title display display--optical">EYES OF WAKANDA</span>
        <span class="anno anno--dim">MARVEL ANIMATION · CHARACTER DESIGN</span>
      </a>
      <img class="next-work__peek" src="assets/thumbs/eow/eow-01-lineup.jpg" alt="" aria-hidden="true" loading="lazy">
    </section>
""")

    out.append(FOOT.format(page_js="boards.js"))
    with open(os.path.join(ROOT, "storyboards.html"), "w", encoding="utf-8") as fh:
        fh.write("".join(out))
    print("wrote storyboards.html")


if __name__ == "__main__":
    for k in PROJECTS:
        build_case(k)
    build_boards()
    print("== DONE ==")

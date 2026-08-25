# uzomadunkwu.com

No build step. Open `index.html` and it runs. This file covers where the
artwork lives, what is derived from what, and which script rebuilds it.

## Pages

| File | Contents |
|---|---|
| `index.html` | Hero, award, about, wall, portfolio track, storyboard tiles, create/conform, teaching, products. |
| `work-eyes-of-wakanda.html` | 19 Eyes of Wakanda pieces, process scrubber on Noni. |
| `work-iyanu.html` | 7 Iyanu pieces, scrubber on the ideation sheet. |
| `work-personal.html` | 12 personal pieces, scrubber on Afro Ninja. |
| `storyboards.html` | Three filmstrips, 23 panels, three clips. |

The four project pages are **generated**. Edit the titles and alt text in
`tools/build_pages.py` and re-run it; do not hand-edit the HTML.

```
python tools/build_pages.py
```

## Code

| File | Contents |
|---|---|
| `css/base.css` | Tokens, reset, grain, header, footer, cursor, preloader, page-transition panel. |
| `css/type.css` | Clash Display, Satoshi, JetBrains Mono, and the type scale. |
| `css/sections.css` | Home page sections. |
| `css/work.css` | Case studies, storyboards, image viewer. |
| `js/core.js` | Boot, Lenis, `[data-reveal]`, counters, scramble, magnets, viewer, preloader. Exposed as `window.UZ`. |
| `js/home.js` | Home page sections. |
| `js/work.js` | Process scrubber and case-study parallax. |
| `js/boards.js` | Filmstrip travel and the clip players. |
| `js/cursor.js` | Custom cursor. |
| `js/transitions.js` | Page-to-page transition. |

`css/base.css` defines `--sheet-w` and `--sheet-top`. The preloader lays its
silhouettes out in that box and the hero uses the same one, so the hand-off
between them is seamless. Changing either value moves both.

## Derived passes

Each artwork can be shown at four stages. Only the render is real art; the
other three are generated:

`-sketch` pale under-drawing · `-line` ink line · `-flat` posterised flats ·
the render itself, no suffix.

Four pieces carry the full set, because four is all the site scrubs:
`eow-01-lineup`, `eow-02-noni`, `iyanu-01-ideation`,
`personal-01-afro-ninja`. To add another, add its stem to `PASS_SOURCES` in
`tools/prep_v2.py` and re-run.

## Asset pipeline

```
python tools/prep_v2.py      # passes, silhouettes, award cutout, thumbnails
python tools/build_pages.py  # the four generated pages
```

`prep_v2.py` does five things:

1. **Derived passes** for the four scrubber pieces.
2. **Hero plate.** The source artwork has a black ©MARVEL bar at the bottom.
   The hero copies are cropped to the art itself, **2560×1173**, so the
   wordmark can sit across the bottom of the frame. The case-study copies
   keep the bar.
3. **Silhouettes.** The source PNGs are figures on pure white with a fully
   opaque alpha channel, so the background is found by flooding the white in
   from the border. Interior whites (a robe, the gap between two arms) stay
   figure because they are not connected to the edge. Ruled guide lines are
   detected as one-row spikes and dropped. Writes
   `hero-eow-lineup-sil.png`, `hero-sil-{1..5}.png`, `sil-map.json`.
4. **Award cutout.** The source photo was keyed with a hard violet fill
   around the hand; those pixels are dropped and the trophy is trimmed to
   its own bounds. The Noni silhouette behind that section
   (`eow-02-noni-ghost.png`) is written pre-tinted rather than coloured with
   a CSS mask, because a mask is a same-origin request and would fail over
   `file://`.
5. **Thumbnails** at 900px into `assets/thumbs/`, mirroring the folder
   structure. Board frames are letterbox-trimmed on the way through.

`sil-map.json` holds the position of each Lion team figure inside the
artwork, normalised 0–1, plus the head anchor each label's leader line points
at. The same numbers are inlined in `js/home.js` as `FIGURES`, and as static
`--x` / `--b` values in `css/sections.css` so the labels are still placed
correctly with JavaScript disabled. **If the lineup artwork changes, re-run
`prep_v2.py` and copy the new `sil-map.json` figures into both places.**

## Handing the code to someone who cannot see the images

```
python tools/asset_brief.py
```

Writes two files. `ASSET-BRIEF.md` describes every image and clip — measured
path, dimensions, aspect ratio, background colour, transparency, whether it
carries the black licensing bar, and what is depicted — so the site can be
laid out without ever opening the artwork. `KIMI-PROMPT.md` is the same brief
with a review request on top, to paste into another tool in one go alongside
the HTML, CSS and JS.

Re-run it whenever artwork is added, replaced or renamed.

## Replacing artwork

Drop a file with the same name and a similar aspect ratio into the same
folder, then re-run both scripts. Keep sources under about 2.5 MB; the JPEG
quality settings assume that.

`prep_assets.py`, `prep_hero.py` and `prep_silhouettes.py` are kept as a
record of how `/assets` was first built from the client's folder. They are
marked SUPERSEDED at the top and should not be re-run. `prep_hero.py`
derives silhouettes from the alpha channel, which is why every silhouette on
the site used to be a black rectangle.

## Loading

163 files, about 42 MB on disk, but no page loads more than a fraction: the
wall uses 900px thumbnails, full-size images load only when opened in the
viewer, and the clips are `preload="none"`.

Fonts come from Fontshare (Clash Display, Satoshi) and Google (JetBrains
Mono). GSAP, ScrollTrigger, ScrollToPlugin, Lenis and SplitType come from
jsDelivr, pinned with SRI hashes. If any of that is unreachable the site
falls back to a complete, readable static document, the same as under
`prefers-reduced-motion`, and the same opened over `file://`.

**If you bump a CDN version, recompute its `integrity` hash**, or the browser
will refuse the script and the site will drop to that static fallback.

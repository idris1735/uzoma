# uzomadunkwu.com

No build step. Open `index.html` and it runs.

## Pages

| File | What it is |
|---|---|
| `index.html` | The landing: one sheet, edge to edge, the tagline over it. |
| `about.html` | The Emmy card, the writing, the award in his hand. |
| `contact.html` | The address and the four accounts. |
| `work-eyes-of-wakanda.html` | 19 sheets, one at a time. |
| `work-iyanu.html` | 7 sheets. |
| `work-personal.html` | 12 sheets. |
| `storyboards-coma-toes.html` | The board, page by page, and the animatic. |
| `storyboards-cash-trapped.html` | Both parts, board and animatic each. |

Every page carries `css/site.css` and `js/site.js` and nothing else.

The six work and storyboard pages are **generated**. Edit the titles and
alt text in `tools/build_decks.py` and re-run it rather than editing the
HTML by hand — it also rewrites the shared header everywhere, so a nav
change is made in one place.

```
python tools/build_decks.py
```

## Artwork

Sources live outside the repository, in `Uzoma Website Images/` and
`Storyboards/` (both gitignored — hundreds of megabytes).

| Script | Makes |
|---|---|
| `tools/prep_assets.py` | `assets/{eow,iyanu,personal}` — the sheets, named and optimised from the client's folders. |
| `tools/prep_hero_landing.py` | `assets/hero/dora-{wide,mid,tall}-*.jpg` — the landing sheet in three crops. |
| `tools/prep_award.py` | `assets/misc/eow-emmy-*.jpg` and `caa-award-*.jpg` — the about page's two pictures. |
| `tools/prep_boards.py` | `boards/{coma-toes,cash-trapped-1,cash-trapped-2}/NNNN.webp` — 1735 storyboard pages. |

### The landing sheet

`eow-15-dora.png` is a 1.97 landscape and a browser window rarely is. A
single `cover` fit would crop the Eyes of Wakanda logo off one end and
the rights mark off the other, so `prep_hero_landing.py` sits the sheet
on more of its own flat grey until each file is shaped like the windows
it serves. `cover` then eats grey instead of artwork.

Three crops, because one cannot serve every shape: padding the whole
sheet down to a tablet's proportions leaves the artwork a strip in a
field of grey, and cropping it to a phone's leaves a tablet looking at
one shoulder.

| File | Keeps | Window shapes |
|---|---|---|
| `dora-wide` | the whole sheet | 1.15 – 2.05 |
| `dora-mid` | Shakoo, B'Risa, Koi'Fay | 0.62 – 1.15 |
| `dora-tall` | Shakoo and the logo | up to 0.53 |

`index.html` picks between them with `<picture>` on `aspect-ratio`.

### The boards

The client's PDFs run 529, 575 and 631 pages — about 200 MB. Handing a
visitor a 74 MB file to flip through is not a website, so every page is
rendered to WebP and served one at a time. There is then nothing to
download: the PDFs never leave the artist's drive. Pages are rendered
whole (the scene and panel numbers along the top are meant to be read)
with the white paper margin trimmed off, so a board fills its frame
rather than sitting in a box of white.

## Video

The three animatics are YouTube embeds, built only when their tab is
opened and torn down when it is left. They use the plain `youtube.com`
host rather than `youtube-nocookie.com`: the privacy-enhanced host is
blocked by filters that leave the ordinary one alone.

# Asset brief — uzomadunkwu.com

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

### Hero images (home page only)
These are cropped copies of `eow-01-lineup` with the ©MARVEL bar removed, so their aspect ratio (2.18:1) differs from every other Eyes of Wakanda file. `-flat`, `-line` and `-sketch` versions exist at the same size.
- `assets/hero-eow-lineup-final.jpg` — 2560x1173; 2.18:1 very wide; bg white; key colours #303050, #305050, #505090, #705030.
  The five Lion team warriors standing in a row, full length, gold lion masks and layered violet/teal wraps. The site's opening image. Cropped to the art, no footer bar.
- `assets/hero-eow-lineup-sil.png` — 2560x1173; 2.18:1 very wide; bg transparent; has real transparency; key colours mostly neutral.
  Flat black silhouettes of the five warriors on full transparency. Needs a light or coloured backdrop to be visible at all.

### Eyes of Wakanda
- `assets/eow/eow-02-noni.png` — 1800x990; 1.82:1 wide; bg white; black ©MARVEL bar across the bottom ~13% of the height; key colours #705030, #503030, #703030, #305050.
  Noni. Portrait bust at left, a fighting stance in a blue wrap, then three grey action studies. The character that won the CAA award.
- `assets/eow/eow-03-noni-keys.png` — 1800x1020; 1.76:1 wide; bg white; black ©MARVEL bar across the bottom ~11% of the height; key colours #703030, #907070, #503030, #309090.
  Five full-length costume passes on the same figure: teal wrap, hooded cloak, mask and collar, pale robe, layered skirt.
- `assets/eow/eow-04-old-noni.png` — 1800x1011; 1.78:1 wide; bg white; black ©MARVEL bar across the bottom ~14% of the height; key colours #503050, #705030, #503030, #B07050.
  An older woman in an ochre cloak and violet skirt at left, then four white line/construction turnarounds of the same garment.
- `assets/eow/eow-05-traveller.png` — 1800x1321; 1.36:1 landscape; bg white; black ©MARVEL bar across the bottom ~12% of the height; key colours #B09090, #705090, #503030, #705070.
  Five layered travelling costumes, labelled A-D, built up on pale grey mannequins. Fur collars, beads, wraps.
- `assets/eow/eow-06-councilman.png` — 1800x1241; 1.45:1 landscape; bg white; black ©MARVEL bar across the bottom ~12% of the height; key colours #707030, #907030, #705030, #503050.
  A dark bodysuit figure, a small mask study, then three olive-and-violet draped robe variants.
- `assets/eow/eow-07-kuda.png` — 1800x1383; 1.3:1 landscape; bg white; black ©MARVEL bar across the bottom ~11% of the height; key colours #705030, #905050, #503070, #905030.
  A broad heavy-set man in a red and blue panelled tunic, drawn twice, plus a slim youth in violet at right.
- `assets/eow/eow-08-tafari.png` — 1800x2027; 0.89:1 portrait; bg white; black ©MARVEL bar across the bottom ~10% of the height; key colours #303050, #503050, #705030, #705050.
  Two figures. A muscular man in violet armour with a metal vambrace, and a younger figure with folded arms. Tall portrait format.
- `assets/eow/eow-09-lion-guard.png` — 1800x1781; 1.01:1 square; bg white; black ©MARVEL bar across the bottom ~13% of the height; key colours #B07050, #B09050, #D0B090, #D09070.
  Six head-and-shoulders studies in a 3x2 grid, labelled A-F. Lots of white space around them.
- `assets/eow/eow-10-chainmakers.png` — 1800x798; 2.26:1 very wide; bg white; black ©MARVEL bar across the bottom ~15% of the height; key colours #303050, #503030, #503010, #505030.
  Five armoured guards in helmets and studded leather, shown front and back. Very wide, short format.
- `assets/eow/eow-11-harem.png` — 1800x940; 1.91:1 wide; bg white; black ©MARVEL bar across the bottom ~15% of the height; key colours #509090, #507070, #305070, #507090.
  Four figures in pale blue robes and gold headdresses. Two have arms stretched wide to show the garment shape.
- `assets/eow/eow-12-seamstresses.png` — 1800x1467; 1.23:1 landscape; bg white; black ©MARVEL bar across the bottom ~11% of the height; key colours #305070, #305050, #705030, #705050.
  Three women, labelled A-C, in teal and gold wraps. Different ages and builds.
- `assets/eow/eow-13-ethiopian.png` — 1800x1387; 1.3:1 landscape; bg white; black ©MARVEL bar across the bottom ~12% of the height; key colours #705030, #503010, #907050, #503030.
  Three soldiers: a shield bearer, a spearman in a grey robe, a commander with a large gold disc shield.
- `assets/eow/eow-14-crowd.png` — 1800x1336; 1.35:1 landscape; bg white; black ©MARVEL bar across the bottom ~11% of the height; key colours #505030, #705030, #707050, #705050.
  Four civilians in striped and beaded wraps, one in a wide woven hat. Headed 'RIVER TRIBE'.
- `assets/eow/eow-15-dora.png` — 1800x915; 1.97:1 wide; bg flat #6B6B6B; black ©MARVEL bar across the bottom ~15% of the height; key colours #705030, #503030, #703030, #703010.
  IMPORTANT: the shape-language sheet. Five torsos on a mid-grey field, named Shakoo, B'Risa, Koi'Fay, Y'Fett, Le'illa, each with a pale geometric primitive drawn beside it and handwritten notes underneath. This is the only artwork with a grey (not white) background, which is why the site uses it as a full-bleed background image.
- `assets/eow/eow-16-flashback.png` — 1800x1358; 1.33:1 landscape; bg flat #686868; black ©MARVEL bar across the bottom ~13% of the height; key colours #503030, #503010, #501010, #301010.
  A rendered bald male bust in warm light on a grey field, with a small line drawing of the same head. Darker and more painterly than the rest.
- `assets/eow/eow-17-dora-02.png` — 1800x983; 1.83:1 wide; bg white; black ©MARVEL bar across the bottom ~12% of the height; key colours #503030, #705030, #503010, #703030.
  Four loose vignettes of the team interacting, with red handwritten notes underneath.
- `assets/eow/eow-18-crowd-02.png` — 1800x1177; 1.53:1 wide; bg white; black ©MARVEL bar across the bottom ~12% of the height; key colours #703030, #701030, #903030, #705030.
  Four figures in red checked cloth and heavy sandals. Headed 'MINING TRIBE'.
- `assets/eow/eow-19-crowd-03.png` — 1800x1108; 1.62:1 wide; bg white; black ©MARVEL bar across the bottom ~13% of the height; key colours #303050, #503030, #705030, #305090.
  Four robed merchants in deep blue and plum, one veiled. Headed 'WAKANDAN CARAVAN'.

### Iyanu
- `assets/iyanu/iyanu-01-ideation.jpg` — 1800x1095; 1.64:1 wide; bg white; key colours #905070, #907050, #503030, #709070.
  Three young Yoruba characters full length, plus a photograph of a carved wooden figure at right captioned 'LAMIDI FAKEYE' in red handwriting.
- `assets/iyanu/iyanu-02-exploration.jpg` — 1800x787; 2.29:1 very wide; bg white; key colours #905070, #907050, #709070, #B09070.
  The same three characters, each paired with its line drawing, so six figures across. Wide, short format.
- `assets/iyanu/iyanu-03-exploration.jpg` — 1800x1095; 1.64:1 wide; bg white; key colours #905070, #907050, #709070, #905050.
  A second pass, colour figure next to line figure, four across.
- `assets/iyanu/iyanu-04-biyi.jpg` — 1800x1354; 1.33:1 landscape; bg white; key colours mostly neutral.
  Four loose line studies of one character in motion. Pure line, no colour, lots of white.
- `assets/iyanu/iyanu-05-biyi-02.jpg` — 1800x1500; 1.2:1 landscape; bg white; key colours #907050, #709090, #709070, #503030.
  Model sheet. Colour front view and line profile on ruled height guides, a forearm detail, and the Lamidi Fakeye reference photo at top left.
- `assets/iyanu/iyanu-06-0621.jpg` — 1800x1693; 1.06:1 square; bg white; key colours #703030, #705050, #707050, #507050.
  A boy in a red tunic and a bearded man in a green and violet wrapper, against a numbered height chart with red rules.
- `assets/iyanu/iyanu-07-0621-02.jpg` — 1800x2045; 0.88:1 portrait; bg white; key colours #907050, #D05030, #B03030, #705050.
  A single archer, full length, blue bow and a quiver of arrows, red and orange wrapper. Tall portrait format, one figure only.

### Personal work
- `assets/personal/personal-01-afro-ninja.png` — 1600x1600; 1.0:1 square; bg white; key colours #505030, #503030, #705030, #707050.
  A hooded warrior in a blue cape at left, a grey action study at right, and a forked blade with a tooled sheath below. Square format.
- `assets/personal/personal-02-pirate.png` — 1600x900; 1.78:1 wide; bg white; key colours #907050, #705030, #505030, #907030.
  A blond-braided boy in seven action poses with a bow. Scattered across the sheet, not a row.
- `assets/personal/personal-03-vampire.png` — 1600x900; 1.78:1 wide; bg white; key colours #501030, #701030, #503030, #703050.
  One woman in two lives: white lab coat scientist, then crimson-caped vampire with a bat form. Five figures, wide format.
- `assets/personal/personal-04-femme.png` — 1600x800; 2.0:1 very wide; bg white; key colours #709070, #D09070, #507070, #B09070.
  A woman in a green patterned kimono with hair sticks and red ribbons, drawn four times with different expressions.
- `assets/personal/personal-05-hands.png` — 1600x800; 2.0:1 very wide; bg white; key colours #907070, #B07070, #B09070, #B09090.
  Nineteen hand studies scattered across the page in flat warm greys. No figures.
- `assets/personal/personal-06-people.png` — 1600x800; 2.0:1 very wide; bg white; key colours #90D0B0, #903010, #70B090, #509070.
  Three body-type studies: sumo wrestler in a green yukata, heavyset man in a blue polo, muscular red-toned figure from behind.
- `assets/personal/personal-07-mammal.png` — 1600x800; 2.0:1 very wide; bg white; key colours #705090, #703070, #705070, #D0B070.
  Five anthropomorphic animals in school uniforms (rhino, antelope, cheetah, gorilla, bush baby) with handwritten trait notes beside each. Titled 'MAMMAL COLLEGE'.
- `assets/personal/personal-08-gangster.png` — 1600x1597; 1.0:1 square; bg flat #676767; key colours #705050, #503030, #703030, #505030.
  A woman in leopard print and armour between two large bears with gold arrows in their backs. Flat mid-grey background, not white. Square format.
- `assets/personal/personal-10-dump.jpg` — 1600x1602; 1.0:1 square; bg white; key colours mostly neutral.
  A page of loose pencil heads and figures, mostly uncoloured. Square format.
- `assets/personal/personal-11-futuristic.png` — 1600x1600; 1.0:1 square; bg white; key colours #907010, #705010, #707050, #707030.
  Three tall figures labelled A, B, C in grey armour with gold winged shoulders and crested helms. Square format.

### Cutouts with transparency
- `assets/misc/caa-award.png` — 860x1292; 0.67:1 portrait; bg transparent; black ©MARVEL bar across the bottom ~6% of the height; has real transparency; key colours #705030, #503010, #D0B070, #907050.
  Photograph, cut out with a transparent background. A hand holding a brass-and-maple gear-shaped trophy engraved 'The 2025 Concept Art Awards / UZOMA DUNKWU'. Dark browns, brass, pale maple. Tall portrait.
- `assets/eow/eow-02-noni-ghost.png` — 1709x691; 2.47:1 very wide; bg transparent; has real transparency; key colours mostly neutral.
  Flat silhouette of the Noni sheet, filled solid violet (#7A00FF) on transparency. Used as a large faint background shape.

### Storyboard frames
- `assets/boards/coma-toes-f01..f08.jpg` — 8 frames, 1280x960 each (1.33:1), with the film's black bars baked in. The 900px copies in `assets/thumbs/boards/` are letterbox-trimmed to 900x505 (1.78:1) — **use the thumbs**, or you will get black bars inside every panel.
  Loose storyboard panels, black line over flat pale washes (mint, grey, skin tones) on white. Two young women in the first panels.
- `assets/boards/cash-trapped-a-f01..f08.jpg` — 8 frames, 1920x1080 each (1.78:1), with the film's black bars baked in. The 900px copies in `assets/thumbs/boards/` are letterbox-trimmed to 900x385 (2.34:1) — **use the thumbs**, or you will get black bars inside every panel.
  Loose storyboard panels, black line with flat mint-green and grey washes. A street, a figure falling, banknotes on tarmac, parked cars.
- `assets/boards/cash-trapped-b-f01..f07.jpg` — 7 frames, 1920x1080 each (1.78:1), with the film's black bars baked in. The 900px copies in `assets/thumbs/boards/` are letterbox-trimmed to 900x385 (2.34:1) — **use the thumbs**, or you will get black bars inside every panel.
  Second half of the same sequence. Lower camera angles, figures on the ground, more banknotes.

### Video
- `assets/video/cash-trapped-a.mp4` — 250 KB, 1280x720, roughly 8 seconds, silent, loops. An animatic of the matching storyboard.
- `assets/video/cash-trapped-b.mp4` — 324 KB, 1280x720, roughly 8 seconds, silent, loops. An animatic of the matching storyboard.
- `assets/video/coma-toes.mp4` — 154 KB, 1280x720, roughly 8 seconds, silent, loops. An animatic of the matching storyboard.

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

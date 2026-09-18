/**
 * The one place that says what the CMS can edit, and how. Both the
 * admin UI (which fetches this from /api/cms-schema to draw its forms)
 * and cms-save (which enforces it — never trusts a client payload for
 * anything not listed here) read from this file. A field that isn't
 * named here can't be changed through the CMS, full stop.
 *
 * Field types the admin UI knows how to render:
 *   text           single-line
 *   markdown-lite  single-line, supports **bold**, *italic*, ***both***
 *   list-text      a reorderable list of plain strings
 *   list-markdown  a reorderable list of markdown-lite strings (the bio)
 *   date           yyyy-mm-dd
 *   group          a fixed object with its own sub-fields (not a list)
 *   list-group     a reorderable, addable/removable list of objects,
 *                  each with its own sub-fields
 *
 * "locked" sub-fields of a list-group (see storyboard views) are shown
 * for context but never accepted from the client — cms-save always
 * keeps the stored value for those, so a tampered request can't move a
 * storyboard's video or board off what prep_boards.py actually built.
 */

const SLIDE_FIELDS = [
  { key: "src", label: "Image", type: "text", locked: false },
  { key: "alt", label: "Alt text", type: "text" },
  { key: "caption", label: "Caption", type: "text" },
];

const WORK = (file, label, imageDir) => ({
  file,
  label,
  imageDir,
  fields: [
    { key: "title", label: "Title", type: "text" },
    { key: "desc", label: "Description (for search/social)", type: "text" },
    { key: "slides", label: "Slides", type: "list-group", itemFields: SLIDE_FIELDS,
      addable: true, imageField: "src" },
  ],
});

const STORYBOARD = (file, label, imageDir) => ({
  file,
  label,
  fields: [
    { key: "title", label: "Title", type: "text" },
    { key: "desc", label: "Description (for search/social)", type: "text" },
    { key: "views", label: "Tabs", type: "list-group", addable: false, itemFields: [
      { key: "label", label: "Tab label", type: "text" },
      { key: "kind", label: "Kind", type: "text", locked: true },
      { key: "ref", label: "Video ID / board", type: "text", locked: true },
      { key: "count", label: "Page count", type: "text", locked: true },
      { key: "alt", label: "Alt text", type: "text", locked: true },
    ] },
  ],
});

module.exports = {
  site: {
    file: "content/site.yaml",
    label: "Site",
    fields: [
      { key: "hero_lead", label: "Hero tagline — bold lead-in", type: "text" },
      { key: "hero_rest", label: "Hero tagline — rest of the line", type: "text" },
      { key: "email", label: "Contact email", type: "text" },
      { key: "footer_clients", label: "Client list (footer)", type: "list-text", addable: true },
      { key: "credit_text", label: "Credit text", type: "text" },
      { key: "credit_url", label: "Credit link", type: "text" },
    ],
    images: [{ key: "hero_source", label: "Hero image (landing page)", widths: [2560, 1600, 1100] }],
  },
  about: {
    file: "content/about.yaml",
    label: "About",
    fields: [
      { key: "bio", label: "Bio paragraphs", type: "list-markdown", addable: true },
      { key: "emmy_alt", label: "Emmy card image — alt text", type: "text" },
      { key: "award_alt", label: "Award photo — alt text", type: "text" },
    ],
    images: [
      { key: "emmy_source", label: "Emmy card image", widths: [1080, 720] },
      { key: "award_source", label: "Award photo", widths: [1180, 780] },
    ],
  },
  press: {
    file: "content/press.yaml",
    label: "Press",
    fields: [
      { key: "items", label: "Press mentions", type: "list-group", addable: true, itemFields: [
        { key: "outlet", label: "Outlet", type: "text" },
        { key: "headline", label: "Headline", type: "text" },
        { key: "url", label: "Link", type: "text" },
        { key: "date", label: "Date", type: "date" },
        { key: "note", label: "Note (optional)", type: "text" },
      ] },
    ],
  },
  "work-eow": WORK("content/work/eyes-of-wakanda.yaml", "Portfolio — Eyes of Wakanda", "assets/eow"),
  "work-iyanu": WORK("content/work/iyanu.yaml", "Portfolio — Iyanu", "assets/iyanu"),
  "work-personal": WORK("content/work/personal.yaml", "Portfolio — Personal", "assets/personal"),
  "storyboard-coma": STORYBOARD("content/storyboards/coma-toes.yaml", "Storyboards — Coma Toes"),
  "storyboard-cash": STORYBOARD("content/storyboards/cash-trapped.yaml", "Storyboards — Cash Trapped"),
};

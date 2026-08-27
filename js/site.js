/* ============================================================
   site.js — the one script the site carries.
   The menu, and the decks that carry the work: one sheet on
   screen, arrows and marks to step through the rest. No
   libraries, works straight off the disk.
   ============================================================ */

"use strict";

(() => {
  /* file:// never fires loading="lazy" in Chromium — strip it so the
     site works when opened straight off the disk */
  if (location.protocol === "file:") {
    document.querySelectorAll("img[loading]").forEach((im) => im.removeAttribute("loading"));
  }

  /* ---- the menu: closes on a chosen link, on Escape, on an outside
     tap, and keeps its expanded state honest ---- */
  const navToggle = document.getElementById("nav-toggle");
  if (navToggle) {
    const burger = document.querySelector(".nav-burger");
    const head = document.querySelector(".head");
    const sync = () => {
      if (burger) burger.setAttribute("aria-expanded", navToggle.checked ? "true" : "false");
      /* the class (not just :has) opens the panel — older mobile
         browsers don't support :has() and the menu would never open */
      if (head) head.classList.toggle("is-open", navToggle.checked);
    };
    sync();
    navToggle.addEventListener("change", sync);

    document.querySelectorAll(".head__nav a").forEach((a) =>
      a.addEventListener("click", () => { navToggle.checked = false; }));

    document.addEventListener("click", (e) => {
      if (!navToggle.checked) return;
      /* the label forwards a second click whose target is the checkbox
         itself — treat it as part of the header or the menu is
         unchecked again in the same tap */
      if (e.target.closest(".head__nav, .nav-burger, .nav-toggle")) return;
      navToggle.checked = false;
    });

    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && navToggle.checked) navToggle.checked = false;
    });
  }

  /* dropdowns on touch screens: there is no hover, so a tap on the
     label toggles the panel */
  document.querySelectorAll(".drop").forEach((drop) => {
    const label = drop.querySelector(".drop__label");
    if (!label) return;
    label.addEventListener("click", () => {
      const open = !drop.classList.contains("is-open");
      document.querySelectorAll(".drop.is-open").forEach((d) => d.classList.remove("is-open"));
      drop.classList.toggle("is-open", open);
    });
  });

  document.addEventListener("click", (e) => {
    if (e.target.closest(".drop")) return;
    document.querySelectorAll(".drop.is-open").forEach((d) => d.classList.remove("is-open"));
  });

  /* ============================== DECKS ==============================
     The portfolio and storyboard pages show one sheet at a time. The
     controls only appear once this runs, so a browser without JavaScript
     is left with the first sheet rather than a row of dead buttons. */

  document.querySelectorAll("[data-deck]").forEach((deck) => {
    const slides = Array.from(deck.querySelectorAll(".slide"));
    if (!slides.length) return;

    const dots = deck.querySelector(".deck__dots");
    const cap = deck.querySelector(".deck__cap");
    const title = (deck.querySelector(".deck__title") || {}).textContent || "";
    let at = 0;

    /* a mark per sheet: position without putting a number on the page */
    slides.forEach((_, n) => {
      const dot = document.createElement("button");
      dot.className = "deck__dot";
      dot.type = "button";
      dot.setAttribute("aria-label", `${title}, ${n + 1} of ${slides.length}`);
      dot.addEventListener("click", () => go(n));
      dots.appendChild(dot);
    });
    const marks = Array.from(dots.children);

    /* a hidden slide never fetches a lazy image, so the neighbours are
       promoted as we arrive — stepping is then instant */
    const warm = (n) => {
      const im = slides[(n + slides.length) % slides.length].querySelector("img[loading]");
      if (im) im.loading = "eager";
    };

    const go = (n) => {
      at = (n + slides.length) % slides.length;
      slides.forEach((s, k) => {
        s.classList.toggle("is-on", k === at);
        const v = s.querySelector("video");
        if (v && k !== at) v.pause();
      });
      marks.forEach((m, k) => m.setAttribute("aria-current", k === at ? "true" : "false"));
      if (cap) {
        const fc = slides[at].querySelector("figcaption");
        cap.textContent = fc ? fc.textContent : "";
      }
      warm(at - 1);
      warm(at + 1);
    };

    deck.querySelector("[data-deck-prev]").addEventListener("click", () => go(at - 1));
    deck.querySelector("[data-deck-next]").addEventListener("click", () => go(at + 1));

    document.addEventListener("keydown", (e) => {
      if (e.target.closest("input, textarea, video")) return;
      if (e.key === "ArrowLeft") go(at - 1);
      if (e.key === "ArrowRight") go(at + 1);
    });

    /* swipe, but not across a video's own controls */
    let from = null;
    const stage = deck.querySelector(".deck__stage");
    stage.addEventListener("pointerdown", (e) => {
      from = e.target.closest("video") ? null : e.clientX;
    });
    stage.addEventListener("pointerup", (e) => {
      if (from === null) return;
      const dx = e.clientX - from;
      from = null;
      if (Math.abs(dx) > 48) go(at + (dx < 0 ? 1 : -1));
    });

    deck.classList.add("is-live");
    go(0);
  });
  /* ============================== SHOWS ==============================
     A storyboard page is a set of views — a board to page through, or an
     animatic on YouTube — and a tab for each. The players are not built
     until their tab is opened, and switching away rebuilds the iframe so
     nothing carries on playing out of sight. */

  document.querySelectorAll("[data-show]").forEach((show) => {
    const tabs = Array.from(show.querySelectorAll(".show__tab"));
    const views = Array.from(show.querySelectorAll(".view"));
    if (!tabs.length || tabs.length !== views.length) return;

    const open = (n) => {
      tabs.forEach((t, k) => t.setAttribute("aria-selected", k === n ? "true" : "false"));
      views.forEach((v, k) => {
        v.classList.toggle("is-on", k === n);
        const frame = v.querySelector("iframe");
        if (!frame) return;
        if (k === n) {
          if (!frame.src) frame.src = frame.dataset.src;
        } else if (frame.src) {
          /* clearing the source is what actually stops the sound */
          frame.removeAttribute("src");
        }
      });
    };

    tabs.forEach((t, n) => t.addEventListener("click", () => open(n)));
    open(0);

    /* ---- boards: one page on screen, the rest fetched as they are asked
       for. A board runs to six hundred pages, so they are never all in
       the document at once. ---- */
    show.querySelectorAll(".view--board").forEach((board) => {
      const img = board.querySelector(".view__page");
      const scrub = board.querySelector(".view__scrub");
      const count = +board.dataset.count;
      const path = board.dataset.path;
      let page = 1;

      const file = (n) => `${path}${String(n).padStart(4, "0")}.webp`;

      const go = (n) => {
        page = Math.min(count, Math.max(1, n));
        img.src = file(page);
        scrub.value = String(page);
        [page - 1, page + 1].forEach((k) => {
          if (k >= 1 && k <= count) { const pre = new Image(); pre.src = file(k); }
        });
      };

      board.querySelector("[data-page-prev]").addEventListener("click", () => go(page - 1));
      board.querySelector("[data-page-next]").addEventListener("click", () => go(page + 1));
      scrub.addEventListener("input", () => go(+scrub.value));

      document.addEventListener("keydown", (e) => {
        if (!board.classList.contains("is-on")) return;
        if (e.target.closest("input, textarea")) return;
        if (e.key === "ArrowLeft") go(page - 1);
        if (e.key === "ArrowRight") go(page + 1);
      });

      /* a swipe turns the page */
      let from = null;
      const frame = board.querySelector(".view__frame");
      frame.addEventListener("pointerdown", (e) => { from = e.clientX; });
      frame.addEventListener("pointerup", (e) => {
        if (from === null) return;
        const dx = e.clientX - from;
        from = null;
        if (Math.abs(dx) > 48) go(page + (dx < 0 ? 1 : -1));
      });

      /* the board is here to be read, not collected */
      img.addEventListener("contextmenu", (e) => e.preventDefault());

      go(1);
    });
  });
})();

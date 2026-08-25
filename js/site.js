/* ============================================================
   site.js — the one script the simple build carries.
   A dependency-free sheet viewer: click any wall tile, view the
   artwork full size, step through with arrows or the keyboard,
   Escape closes. No libraries, works straight off the disk.
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
    const sync = () => {
      if (burger) burger.setAttribute("aria-expanded", navToggle.checked ? "true" : "false");
    };
    sync();
    navToggle.addEventListener("change", sync);

    document.querySelectorAll(".head__nav a").forEach((a) =>
      a.addEventListener("click", () => { navToggle.checked = false; }));

    document.addEventListener("click", (e) => {
      if (!navToggle.checked) return;
      if (e.target.closest(".head__nav, .nav-burger")) return;
      navToggle.checked = false;
    });

    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && navToggle.checked) navToggle.checked = false;
    });
  }

  const tiles = Array.from(document.querySelectorAll("[data-full]"));
  if (!tiles.length) return;

  const lb = document.createElement("div");
  lb.className = "lb";
  lb.setAttribute("role", "dialog");
  lb.setAttribute("aria-modal", "true");
  lb.setAttribute("aria-label", "Sheet viewer");
  lb.innerHTML = `
    <div class="lb__bar">
      <p class="lb__title"></p>
      <button class="lb__btn" type="button" data-lb-close aria-label="Close viewer">
        <svg viewBox="0 0 24 24"><line x1="5" y1="5" x2="19" y2="19"/><line x1="19" y1="5" x2="5" y2="19"/></svg>
      </button>
    </div>
    <div class="lb__stage"><img class="lb__img" alt=""></div>
    <div class="lb__bar lb__bar--foot">
      <p class="lb__count"></p>
      <div class="lb__nav">
        <button class="lb__btn" type="button" data-lb-prev aria-label="Previous sheet">
          <svg viewBox="0 0 24 24"><polyline points="14,5 7,12 14,19"/></svg>
        </button>
        <button class="lb__btn" type="button" data-lb-next aria-label="Next sheet">
          <svg viewBox="0 0 24 24"><polyline points="10,5 17,12 10,19"/></svg>
        </button>
      </div>
    </div>`;
  document.body.appendChild(lb);

  const img = lb.querySelector(".lb__img");
  const title = lb.querySelector(".lb__title");
  const count = lb.querySelector(".lb__count");
  let i = 0;
  let opener = null;

  const show = (n) => {
    i = (n + tiles.length) % tiles.length;
    const t = tiles[i];
    const thumb = t.querySelector("img");
    title.textContent = t.dataset.title || "";
    count.textContent = `${t.dataset.no || String(i + 1).padStart(2, "0")} / ${tiles.length}`;
    img.alt = (thumb && thumb.alt) || t.dataset.title || "";
    img.src = t.dataset.full;
  };

  const open = (n, from) => {
    opener = from || null;
    show(n);
    lb.classList.add("is-open");
    document.documentElement.classList.add("is-lb");
    lb.querySelector("[data-lb-close]").focus();
  };

  const close = () => {
    lb.classList.remove("is-open");
    document.documentElement.classList.remove("is-lb");
    if (opener) opener.focus();
  };

  tiles.forEach((t, n) => t.addEventListener("click", () => open(n, t)));
  lb.querySelector("[data-lb-close]").addEventListener("click", close);
  lb.querySelector("[data-lb-prev]").addEventListener("click", () => show(i - 1));
  lb.querySelector("[data-lb-next]").addEventListener("click", () => show(i + 1));
  lb.addEventListener("click", (e) => {
    if (e.target === lb || e.target.classList.contains("lb__stage")) close();
  });

  document.addEventListener("keydown", (e) => {
    if (!lb.classList.contains("is-open")) return;
    if (e.key === "Escape") close();
    if (e.key === "ArrowLeft") show(i - 1);
    if (e.key === "ArrowRight") show(i + 1);
  });

  /* ============================== HOME STAGE ============================== */
  /* The home page is one controlled slider: the art fills the viewport,
     arrows and the range scrub through the set, a swipe works on touch,
     and a tap opens the sheet full size. */
  const stage = document.querySelector(".stage");
  if (stage) {
    const img = stage.querySelector(".stage__img");
    const noEl = stage.querySelector(".stage__no");
    const titleEl = stage.querySelector(".stage__title");
    const projEl = stage.querySelector(".stage__project");
    const range = stage.querySelector(".stage__range");
    let cur = -1;
    let pressX = null;

    const go = (n, dir = 0) => {
      cur = (n + tiles.length) % tiles.length;
      const s = tiles[cur];
      const title = s.querySelector(".wall__cap-title")?.textContent || s.dataset.title || "";
      const proj = s.querySelector(".wall__cap-project")?.textContent || "Work";
      noEl.textContent = `${s.dataset.no || String(cur + 1).padStart(2, "0")} / ${tiles.length}`;
      titleEl.textContent = title;
      projEl.textContent = proj;
      range.value = String(cur);

      img.classList.remove("is-in");
      const swap = () => {
        /* the reveal is load-driven with a timer fallback, so the sheet
           can never be left blank by a missed event */
        const reveal = () => img.classList.add("is-in");
        img.onload = reveal;
        img.onerror = reveal;
        setTimeout(reveal, 900);
        /* phones crop the landscape landing sheet onto the first girl */
        const onPhone = window.matchMedia("(max-width: 640px)").matches;
        img.style.objectPosition = onPhone && (s.dataset.full || "").includes("eow-15-dora")
          ? "6% 50%"
          : "50% 50%";
        img.src = s.dataset.full;
        img.alt = (s.querySelector("img") || {}).alt || title;
      };
      if (dir) setTimeout(swap, 300);
      else swap();

      /* warm the neighbours so stepping never waits */
      [cur - 1, cur + 1].forEach((k) => {
        const nb = tiles[(k + tiles.length) % tiles.length];
        if (nb && nb.dataset.full) { const pre = new Image(); pre.src = nb.dataset.full; }
      });
    };

    /* open on the sheet the client asked for, then the set follows */
    const start = Math.max(0, tiles.findIndex((s) => (s.dataset.full || "").includes("eow-15-dora")));
    go(start);

    stage.querySelector("[data-next]").addEventListener("click", () => go(cur + 1, 1));
    stage.querySelector("[data-prev]").addEventListener("click", () => go(cur - 1, -1));
    range.addEventListener("input", () => go(+range.value));

    document.addEventListener("keydown", (e) => {
      if (lb.classList.contains("is-open")) return;
      if (e.key === "ArrowRight") go(cur + 1, 1);
      if (e.key === "ArrowLeft") go(cur - 1, -1);
    });

    /* swipe to step, tap to open full size */
    img.addEventListener("pointerdown", (e) => { pressX = e.clientX; });
    img.addEventListener("pointerup", (e) => {
      if (pressX === null) return;
      const dx = e.clientX - pressX;
      pressX = null;
      if (Math.abs(dx) > 48) go(cur + (dx < 0 ? 1 : -1), dx < 0 ? 1 : -1);
      else open(cur);
    });

    /* ===== mobile autoplay: the landing fills itself ===== */
    /* the set drifts on its own, one sheet every ~20s; a finger on it
       pauses the drift, which resumes after another quiet stretch.
       Manual steps, swipes and taps always win. Never reduced motion. */
    const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const autoEligible = !reduced &&
      (window.matchMedia("(max-width: 640px)").matches ||
       window.matchMedia("(hover: none)").matches);
    if (autoEligible) {
      const AUTO_MS = 20000;
      let auto = 0;
      const arm = () => {
        clearTimeout(auto);
        auto = setTimeout(() => { go(cur + 1, 1); arm(); }, AUTO_MS);
      };
      const pause = (resumeIn = AUTO_MS) => {
        clearTimeout(auto);
        auto = setTimeout(arm, resumeIn);
      };
      arm();
      stage.addEventListener("pointerdown", () => pause(), { passive: true });
      range.addEventListener("input", () => pause());
    }
  }
})();

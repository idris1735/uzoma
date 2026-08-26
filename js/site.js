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

})();

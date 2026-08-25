/* ============================================================
   site.js — the one script the simple build carries.
   A dependency-free sheet viewer: click any wall tile, view the
   artwork full size, step through with arrows or the keyboard,
   Escape closes. No libraries, works straight off the disk.
   ============================================================ */

"use strict";

(() => {
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

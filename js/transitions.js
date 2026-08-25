/* ============================================================
   transitions.js — page-to-page transition.

   On leaving, a violet panel wipes in diagonally showing the
   destination name, then the browser navigates. On arriving,
   the same panel wipes off.

   The incoming half is armed by an inline flag in <head>, so the
   new page is covered on its first paint. See the
   `html.is-arriving` rule in base.css.

   Skipped under prefers-reduced-motion, and for anything that is
   not an internal page link.
   ============================================================ */

"use strict";

(() => {
  const KEY = "uz-transit";
  const root = document.documentElement;
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const NAMES = {
    "index": "HOME",
    "storyboards": "STORYBOARDS",
    "work-eyes-of-wakanda": "EYES OF WAKANDA",
    "work-iyanu": "IYANU",
    "work-personal": "PERSONAL",
  };

  const nameFor = (pathname) => {
    const stem = (pathname.split("/").pop() || "index").replace(/\.html?$/, "");
    return NAMES[stem] || stem.replace(/-/g, " ").toUpperCase();
  };

  /* ---------------------------------------------------- arriving ---- */
  /* the flag was read in <head>; clear it either way, so a reload never
     leaves the page stuck under the panel */
  try { sessionStorage.removeItem(KEY); } catch (e) { /* private mode */ }

  if (root.classList.contains("is-arriving")) {
    const clear = () => root.classList.remove("is-arriving", "is-arrived");
    if (reduced) {
      clear();
    } else {
      requestAnimationFrame(() => {
        root.classList.add("is-arrived");
        setTimeout(clear, 900);
      });
    }
  }

  if (reduced) return;

  /* ---------------------------------------------------- leaving ---- */
  const isInternal = (a) => {
    if (!a || !a.getAttribute("href")) return false;
    if (a.target && a.target !== "_self") return false;
    if (a.hasAttribute("download")) return false;
    const url = new URL(a.href, location.href);
    if (url.origin !== location.origin) return false;
    if (!/\.html?$/i.test(url.pathname)) return false;
    if (url.pathname === location.pathname) return false;   /* same-page anchors */
    return true;
  };

  let leaving = false;

  document.addEventListener("click", (e) => {
    if (e.defaultPrevented || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button !== 0) return;
    const a = e.target.closest("a[href]");
    if (!isInternal(a) || leaving) return;

    e.preventDefault();
    leaving = true;
    const href = a.href;

    let curtain = document.querySelector(".vt-curtain");
    if (!curtain) {
      curtain = document.createElement("div");
      curtain.className = "vt-curtain";
      curtain.setAttribute("aria-hidden", "true");
      curtain.innerHTML = '<span class="vt-curtain__word"></span>';
      document.body.appendChild(curtain);
    }
    curtain.querySelector(".vt-curtain__word").textContent = nameFor(new URL(href).pathname);

    try { sessionStorage.setItem(KEY, "1"); } catch (err) { /* private mode */ }

    requestAnimationFrame(() => curtain.classList.add("is-on"));
    setTimeout(() => { location.href = href; }, 620);
  });

  /* returning through history must not land on a stale panel */
  window.addEventListener("pageshow", (e) => {
    if (!e.persisted) return;
    leaving = false;
    const curtain = document.querySelector(".vt-curtain");
    if (curtain) curtain.classList.remove("is-on");
    root.classList.remove("is-arriving", "is-arrived");
  });
})();

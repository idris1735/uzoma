/* ============================================================
   work.js — case-study pages.

   The process scrubber (cross-fade across sketch, line, flats
   and render) plus a little parallax on the header artwork.
   Reveals, the viewer and the header come from core.js.
   ============================================================ */

"use strict";

(() => {
  const { $, $$, MOTION, TOUCH } = window.UZ;

  /* ============================== PROCESS SCRUBBER ============================== */
  /* Four passes of one artwork, cross-faded by a single value. The range
     input is the real control, so keyboard and screen-reader support come
     free; pointer drags just write into it. */
  const initScrub = () => {
    const stage = $("[data-scrub]");
    if (!stage) return;

    const input = $(".scrub__input", stage);
    const handle = $(".scrub__handle", stage);
    const passes = $$(".scrub__pass", stage);
    const names = $$(".scrub__stage-name");
    if (!input || !passes.length) return;

    const spans = passes.length - 1;   /* three transitions across four passes */

    const paint = () => {
      const p = input.value / input.max;
      const s = p * spans;

      passes.forEach((im, i) => {
        im.style.opacity = Math.max(0, Math.min(1, 1 - Math.abs(s - i))).toFixed(3);
      });

      handle.style.setProperty("--pos", `${(p * 100).toFixed(2)}%`);

      const near = Math.round(s);
      names.forEach((n, i) => n.classList.toggle("is-on", i === near));
    };

    input.addEventListener("input", paint);
    paint();

    /* drag anywhere on the artwork */
    let dragging = false;
    const write = (clientX) => {
      const b = stage.getBoundingClientRect();
      const p = Math.max(0, Math.min(1, (clientX - b.left) / b.width));
      input.value = String(Math.round(p * input.max));
      paint();
    };

    stage.addEventListener("pointerdown", (e) => {
      if (e.target === input) return;
      dragging = true;
      stage.setPointerCapture(e.pointerId);
      write(e.clientX);
    });
    stage.addEventListener("pointermove", (e) => { if (dragging) write(e.clientX); });
    stage.addEventListener("pointerup", () => { dragging = false; });
    stage.addEventListener("pointercancel", () => { dragging = false; });

    /* hovering alone steps through the passes */
    if (!TOUCH) {
      stage.addEventListener("pointermove", (e) => { if (!dragging && e.buttons === 0) write(e.clientX); });
    }

    /* no hover on touch, so scroll position drives it instead */
    if (TOUCH && MOTION) {
      gsap.to(input, {
        value: input.max, ease: "none",
        scrollTrigger: { trigger: stage, start: "top 80%", end: "bottom 40%", scrub: 0.6 },
        onUpdate: paint,
      });
    }
  };

  /* ============================== CASE HEADER ============================== */
  const initCase = () => {
    if (!MOTION) return;
    const sheet = $(".case__sheet");
    if (!sheet) return;

    gsap.to(sheet, {
      yPercent: -6, scale: 1.03, ease: "none",
      scrollTrigger: { trigger: sheet, start: "top bottom", end: "bottom top", scrub: 0.7 },
    });

    gsap.to(".case__lamp", {
      opacity: 0.25, ease: "none",
      scrollTrigger: { trigger: ".case", start: "top top", end: "bottom top", scrub: 0.7 },
    });
  };

  /* ============================== NEXT PROJECT ============================== */
  const initNext = () => {
    if (!MOTION || TOUCH) return;
    const peek = $(".next-work__peek");
    const link = $(".next-work__link");
    if (!peek || !link) return;

    const y = gsap.quickTo(peek, "y", { duration: 0.9, ease: "power3.out" });
    link.addEventListener("pointermove", (e) => {
      const b = link.getBoundingClientRect();
      y((e.clientY - b.top - b.height / 2) * 0.18);
    });
  };

  window.UZ.boot();
  initScrub();
  initCase();
  initNext();
})();

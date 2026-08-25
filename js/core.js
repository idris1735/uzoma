/* ============================================================
   core.js — shared boot and motion helpers.

   Loaded on every page. Owns smooth scroll, the [data-reveal]
   system, the header, counters, the image viewer and the
   preloader. Page-specific code lives in home.js / work.js /
   boards.js and reaches this through window.UZ.

   Nothing here hides content up front. If the CDN is
   unreachable or reduced motion is set, the page renders as a
   complete static document.
   ============================================================ */

"use strict";

window.UZ = (() => {
  const REDUCED = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const TOUCH = window.matchMedia("(hover: none)").matches;
  const IS_FILE = location.protocol === "file:";

  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => Array.from(c.querySelectorAll(s));

  /* loading="lazy" never fires over file:// in Chromium, so strip it and
     let the images load normally when the folder is opened directly */
  if (IS_FILE) $$("img[loading]").forEach((img) => img.removeAttribute("loading"));

  const gsapOK = typeof gsap !== "undefined" && typeof ScrollTrigger !== "undefined";
  const splitOK = typeof SplitType !== "undefined";
  const MOTION = gsapOK && !REDUCED;

  if (!MOTION) document.documentElement.classList.add("no-motion");
  if (gsapOK) gsap.registerPlugin(ScrollTrigger, ScrollToPlugin);

  /* ============================== SMOOTH SCROLL ============================== */
  let lenis = null;
  if (MOTION && typeof Lenis !== "undefined") {
    /* touch gets Lenis too — the client's first look is on a phone and
       every pinned scrub should feel driven by the same film-grade
       inertia as the desktop, not by the OS's default scroll */
    lenis = new Lenis({
      lerp: 0.085,
      wheelMultiplier: 1,
      syncTouch: TOUCH,
      touchMultiplier: 1.4,
    });
    lenis.on("scroll", ScrollTrigger.update);
    gsap.ticker.add((t) => lenis.raf(t * 1000));
    gsap.ticker.lagSmoothing(0);
  }

  const scrollTo = (el) => {
    if (lenis) lenis.scrollTo(el, { offset: 0, duration: 1.4 });
    else el.scrollIntoView({ behavior: REDUCED ? "auto" : "smooth" });
  };

  /* ============================== NAV ============================== */
  const initNav = () => {
    const head = $(".site-head");
    const toggle = $("#nav-toggle");

    $$('a[href*="#"]').forEach((a) => {
      const url = new URL(a.href, location.href);
      if (url.pathname !== location.pathname || !url.hash || url.hash.length < 2) return;
      a.addEventListener("click", (e) => {
        const target = $(url.hash);
        if (!target) return;
        e.preventDefault();
        history.replaceState(null, "", url.hash);
        if (toggle) toggle.checked = false;
        scrollTo(target);
      });
    });

    if (!head || !MOTION) return;

    /* hide the header on scroll down, show it on scroll up */
    let last = window.scrollY;
    ScrollTrigger.create({
      start: 0,
      end: "max",
      onUpdate: (self) => {
        const y = self.scroll();
        if (toggle && toggle.checked) { head.classList.remove("is-hidden"); last = y; return; }
        if (y > 240 && y > last) head.classList.add("is-hidden");
        else head.classList.remove("is-hidden");
        last = y;
      },
    });
  };

  /* ============================== REVEALS ============================== */
  /* [data-reveal] — one attribute, four entrances:
       lines  : masked line-by-line rise (headings, prose)
       plate  : clip-path wipe up, settling out of a slight zoom
       chars  : per-letter stagger, for short display words
       rise   : default, translate up and fade in                        */
  const revealLines = (el, stagger = 0.06) => {
    /* masked line-by-line rise runs at every width — a phone deserves the
       same entrance as the desktop; only the CDN absence falls back */
    if (!splitOK) {
      gsap.from(el, {
        y: 22, opacity: 0, duration: 1, ease: "expo.out",
        scrollTrigger: { trigger: el, start: "top 84%", once: true },
      });
      return;
    }
    const split = new SplitType(el, { types: "lines", lineClass: "line-mask" });
    const inner = (split.lines || []).map((l) => {
      const span = document.createElement("span");
      span.style.display = "block";
      while (l.firstChild) span.appendChild(l.firstChild);
      l.appendChild(span);
      return span;
    });
    gsap.from(inner.length ? inner : [el], {
      yPercent: 108, opacity: 0, duration: 1, ease: "expo.out", stagger,
      scrollTrigger: { trigger: el, start: "top 84%", once: true },
    });
  };

  /* clearProps on complete, or the inline transform GSAP leaves behind
     blocks the CSS hover scale on .plate__btn img */
  const revealPlate = (el) => {
    const img = el.querySelector("img") || el;
    gsap.timeline({
      scrollTrigger: { trigger: el, start: "top 88%", once: true },
      onComplete: () => gsap.set(img, { clearProps: "transform" }),
    })
      .fromTo(el, { clipPath: "inset(100% 0% 0% 0%)" },
                  { clipPath: "inset(0% 0% 0% 0%)", duration: 1.1, ease: "expo.out" }, 0)
      .fromTo(img, { scale: 1.16 }, { scale: 1, duration: 1.4, ease: "expo.out" }, 0);
  };

  const initReveals = (root = document) => {
    if (!MOTION) return;
    $$("[data-reveal]", root).forEach((el) => {
      if (el.dataset.revealed) return;
      el.dataset.revealed = "1";
      const kind = el.dataset.reveal || "rise";
      const delay = parseFloat(el.dataset.revealDelay || 0);

      if (kind === "lines") return revealLines(el, parseFloat(el.dataset.stagger || 0.06));
      if (kind === "plate") return revealPlate(el);

      if (kind === "chars") {
        const letters = $$("span", el);
        gsap.from(letters.length ? letters : [el], {
          yPercent: 110, opacity: 0, duration: 0.9, ease: "expo.out", stagger: 0.035, delay,
          scrollTrigger: { trigger: el, start: "top 88%", once: true },
        });
        return;
      }

      gsap.from(el, {
        y: 30, opacity: 0, duration: 1, ease: "expo.out", delay,
        scrollTrigger: { trigger: el, start: "top 88%", once: true },
      });
    });
  };

  /* ============================== MAGNETIC ============================== */
  const initMagnets = () => {
    if (!MOTION || TOUCH) return;
    $$("[data-magnet]").forEach((el) => {
      const pull = parseFloat(el.dataset.magnet) || 0.32;
      const x = gsap.quickTo(el, "x", { duration: 0.5, ease: "power3.out" });
      const y = gsap.quickTo(el, "y", { duration: 0.5, ease: "power3.out" });
      el.addEventListener("pointermove", (e) => {
        const r = el.getBoundingClientRect();
        x((e.clientX - r.left - r.width / 2) * pull);
        y((e.clientY - r.top - r.height / 2) * pull);
      });
      el.addEventListener("pointerleave", () => { x(0); y(0); });
    });
  };

  /* ============================== COUNTERS ============================== */
  const initCounters = () => {
    if (!MOTION) return;
    const fmt = new Intl.NumberFormat("en-US");
    $$("[data-count]").forEach((el) => {
      const end = parseFloat(el.dataset.count);
      const year = el.hasAttribute("data-year");

      /* a number counting up to 1,000,000 re-wraps the sentence around it
         on every frame, so lock the finished width first */
      const w = el.getBoundingClientRect().width;
      if (w) {
        el.style.display = "inline-block";
        el.style.minWidth = `${w.toFixed(1)}px`;
      }

      const obj = { v: year ? end - 24 : 0 };
      gsap.to(obj, {
        v: end, duration: 1.8, ease: "expo.out",
        scrollTrigger: { trigger: el, start: "top 90%", once: true },
        onUpdate: () => {
          el.textContent = year ? String(Math.round(obj.v)) : fmt.format(Math.round(obj.v));
        },
      });
    });
  };

  /* ============================== SCRAMBLE ============================== */
  const initScramble = () => {
    const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/#@";
    $$("[data-scramble]").forEach((el) => {
      const target = el.textContent.trim();
      let raf = 0;
      const run = () => {
        if (REDUCED) return;
        cancelAnimationFrame(raf);
        let frame = 0;
        const total = 16;
        const tick = () => {
          frame++;
          const p = frame / total;
          el.textContent = target.split("").map((c, i) => {
            if (c === " " || c === "@" || c === ".") return c;
            if (i < p * target.length) return c;
            return chars[(Math.random() * chars.length) | 0];
          }).join("");
          if (frame < total) raf = requestAnimationFrame(tick);
          else el.textContent = target;
        };
        tick();
      };
      el.addEventListener("mouseenter", run);
      el.addEventListener("focus", run);
    });
  };

  /* ============================== IMAGE VIEWER ============================== */
  /* Any [data-plate] button opens that image full size. Arrow keys and
     the on-screen controls step through the set; Escape closes. */
  const initViewer = () => {
    /* plates are collected at open time: the wall tiles on the front page
       are built after boot, so a static list would miss them */
    const readPlates = () =>
      $$("[data-plate]").map((b) => ({
        full: b.dataset.plate,
        title: b.dataset.title || "",
        no: b.dataset.no || "",
        alt: (b.querySelector("img") || {}).alt || b.dataset.title || "",
      }));

    /* nothing will ever open here: no plates and no wall host */
    if (!readPlates().length && !$(".wall__cols")) return;

    let plates = readPlates();

    const el = document.createElement("div");
    el.className = "viewer";
    el.setAttribute("role", "dialog");
    el.setAttribute("aria-modal", "true");
    el.setAttribute("aria-label", "Sheet viewer");
    el.innerHTML = `
      <div class="viewer__bar">
        <p class="anno viewer__title"></p>
        <button class="viewer__btn" type="button" data-viewer-close aria-label="Close viewer">
          <svg viewBox="0 0 24 24"><line x1="5" y1="5" x2="19" y2="19"/><line x1="19" y1="5" x2="5" y2="19"/></svg>
        </button>
      </div>
      <div class="viewer__stage"><img class="viewer__img" alt=""></div>
      <div class="viewer__foot">
        <p class="anno anno--dim viewer__count"></p>
        <div class="viewer__nav">
          <button class="viewer__btn" type="button" data-viewer-prev aria-label="Previous sheet">
            <svg viewBox="0 0 24 24"><polyline points="14,5 7,12 14,19"/></svg>
          </button>
          <button class="viewer__btn" type="button" data-viewer-next aria-label="Next sheet">
            <svg viewBox="0 0 24 24"><polyline points="10,5 17,12 10,19"/></svg>
          </button>
        </div>
      </div>`;
    document.body.appendChild(el);

    const img = $(".viewer__img", el);
    const title = $(".viewer__title", el);
    const count = $(".viewer__count", el);
    let i = 0;
    let opener = null;

    const show = (n, dir = 0) => {
      i = (n + plates.length) % plates.length;
      const p = plates[i];
      const swap = () => {
        img.src = p.full;
        img.alt = p.alt;
        title.textContent = p.title;
        count.textContent = `${String(i + 1).padStart(2, "0")} / ${String(plates.length).padStart(2, "0")}`;
      };
      if (!MOTION || !dir) { swap(); return; }
      gsap.timeline()
        .to(img, { xPercent: -6 * dir, opacity: 0, duration: 0.18, ease: "power2.in" })
        .add(swap)
        .fromTo(img, { xPercent: 6 * dir, opacity: 0 },
                     { xPercent: 0, opacity: 1, duration: 0.42, ease: "expo.out" });
    };

    const open = (n, from) => {
      plates = readPlates();
      if (!plates.length) return;
      opener = from || null;
      show(n);
      /* the sheet settles in from a beat behind */
      if (MOTION) {
        gsap.fromTo(img,
          { scale: 0.96, opacity: 0 },
          { scale: 1, opacity: 1, duration: 0.5, ease: "expo.out", overwrite: "auto" });
      }
      el.classList.add("is-open");
      document.documentElement.classList.add("is-locked");
      if (lenis) lenis.stop();
      $("[data-viewer-close]", el).focus();
    };

    const close = () => {
      el.classList.remove("is-open");
      document.documentElement.classList.remove("is-locked");
      if (lenis) lenis.start();
      if (opener) opener.focus();
    };

    /* delegated: wall tiles join the set after boot */
    document.addEventListener("click", (e) => {
      const b = e.target.closest("[data-plate]");
      if (!b) return;
      /* indexOf runs over the raw elements, not the mapped plate objects */
      open($$("[data-plate]").indexOf(b), b);
    });
    $("[data-viewer-close]", el).addEventListener("click", close);
    $("[data-viewer-prev]", el).addEventListener("click", () => show(i - 1, -1));
    $("[data-viewer-next]", el).addEventListener("click", () => show(i + 1, 1));
    el.addEventListener("click", (e) => { if (e.target === el || e.target.classList.contains("viewer__stage")) close(); });

    document.addEventListener("keydown", (e) => {
      if (!el.classList.contains("is-open")) return;
      if (e.key === "Escape") close();
      if (e.key === "ArrowLeft") show(i - 1, -1);
      if (e.key === "ArrowRight") show(i + 1, 1);
    });
  };

  /* ============================== PRELOADER ============================== */
  /* Square -> triangle -> circle, then the shape breaks into the five
     Lion team silhouettes, positioned where the hero will place them so
     the curtain lift is continuous. */
  const initPreloader = (figures, onDone) => {
    const done = () => {
      document.documentElement.classList.remove("is-locked");
      if (lenis) lenis.start();
      if (onDone) onDone();
      if (gsapOK) ScrollTrigger.refresh();
    };

    if (!MOTION || sessionStorage.getItem("uzo-seen")) {
      try { sessionStorage.setItem("uzo-seen", "1"); } catch (e) { /* private mode */ }
      done();
      return;
    }
    try { sessionStorage.setItem("uzo-seen", "1"); } catch (e) { /* private mode */ }

    document.documentElement.classList.add("is-locked");
    if (lenis) lenis.stop();

    const pre = document.createElement("div");
    pre.className = "preload";
    pre.setAttribute("aria-hidden", "true");
    pre.innerHTML = `
      <div class="preload__centre">
        <svg class="preload__shape" viewBox="0 0 40 40">
          <polygon points="2,2 20,2 38,2 38,20 38,38 20,38 2,38 2,20"/>
        </svg>
        <p class="preload__line anno">BLOCKING IN…&nbsp;<span class="preload__pct">000</span></p>
      </div>
      <div class="preload__lamp"></div>
      <div class="preload__sil"></div>`;
    document.body.prepend(pre);

    const stage = $(".preload__sil", pre);
    const pct = $(".preload__pct", pre);
    const poly = $(".preload__shape polygon", pre);

    const SQ = "2,2 20,2 38,2 38,20 38,38 20,38 2,38 2,20";
    const TRI = "20,2 29,2 38,20 38,38 20,38 2,38 2,20 11,2";
    const CIR = "20,3 30,8.5 37,20 30,31.5 20,37 10,31.5 3,20 10,8.5";

    const sils = figures.map((f) => {
      const im = new Image();
      im.src = f.src;
      im.alt = "";
      im.style.left = `${f.x * 100}%`;
      im.style.top = `${f.y * 100}%`;
      im.style.width = `${f.w * 100}%`;
      stage.appendChild(im);
      return im;
    });

    const counter = { v: 0 };
    const pad3 = (n) => String(n).padStart(3, "0");

    const tl = gsap.timeline({
      onComplete: () => {
        gsap.to(pre, {
          yPercent: -100, duration: 0.55, ease: "expo.inOut",
          onComplete: () => { pre.remove(); done(); },
        });
      },
    });

    /* tap anywhere: skip straight to the reveal */
    pre.addEventListener("pointerdown", () => tl.progress(1), { once: true });

    tl.to(counter, {
      v: 100, duration: 0.85, ease: "power2.out",
      onUpdate: () => { pct.textContent = pad3(Math.round(counter.v)); },
    }, 0);
    tl.to(poly, { attr: { points: TRI }, duration: 0.32, ease: "power2.inOut" }, 0.08);
    tl.to(poly, { attr: { points: CIR }, duration: 0.32, ease: "power2.inOut" }, 0.46);
    tl.to(".preload__shape", { scale: 2.2, opacity: 0, duration: 0.3, ease: "power2.in" }, 0.84);
    tl.to(".preload__line", { opacity: 0, duration: 0.18 }, 0.84);
    /* glow up, then the silhouettes settle into their hero positions */
    tl.to(".preload__lamp", { opacity: 1, duration: 0.45, ease: "power2.out" }, 0.82);
    tl.fromTo(sils,
      { opacity: 0, yPercent: 20, scaleY: 1.1 },
      { opacity: 1, yPercent: 0, scaleY: 1, duration: 0.5, ease: "expo.out", stagger: 0.04 }, 0.88);
    tl.to({}, { duration: 0.15 });
  };

  /* ============================== BOOT ============================== */
  const boot = () => {
    initNav();
    initReveals();
    initMagnets();
    initCounters();
    initScramble();
    initViewer();

    if (MOTION) {
      $$("img").forEach((img) =>
        img.addEventListener("load", () => ScrollTrigger.refresh(), { once: true }));
      window.addEventListener("load", () => ScrollTrigger.refresh());
    }
  };

  return {
    $, $$, REDUCED, TOUCH, MOTION, splitOK, IS_FILE,
    get lenis() { return lenis; },
    scrollTo, revealLines, revealPlate, initReveals, initPreloader, boot,
  };
})();

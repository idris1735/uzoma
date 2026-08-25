/* ============================================================
   main.js — boot, motion system, signature moments.
   The site is drawn in layers: preloader → lenis → hero
   resolve → award → about → portfolio x-ray → create/conform
   → teaching counters → footer scramble.
   If CDNs are unreachable or reduced motion is requested,
   the site stays static and fully readable.
   ============================================================ */

"use strict";

(() => {
  const REDUCED = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const IS_FILE = location.protocol === "file:";
  const TOUCH = window.matchMedia("(hover: none)").matches;

  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => Array.from(c.querySelectorAll(s));

  /* file:// + loading="lazy" never fires in Chromium — strip it
     so the site works when opened by double-click */
  if (IS_FILE) $$("img[loading]").forEach((img) => img.removeAttribute("loading"));

  const gsapOK = typeof gsap !== "undefined" && typeof ScrollTrigger !== "undefined";
  const lenisOK = typeof Lenis !== "undefined";
  const splitOK = typeof SplitType !== "undefined";

  if (!gsapOK || REDUCED) {
    document.body.classList.add("no-motion");
    return; // static site — every word still readable
  }

  gsap.registerPlugin(ScrollTrigger, ScrollToPlugin);

  /* ============================== LENIS ============================== */
  let lenis = null;
  if (lenisOK) {
    lenis = new Lenis({ lerp: 0.075, wheelMultiplier: 1 });
    lenis.on("scroll", ScrollTrigger.update);
    gsap.ticker.add((time) => lenis.raf(time * 1000));
    gsap.ticker.lagSmoothing(0);
    window.__uzo = { lenis }; // debugging handle
  }

  const scrollToTarget = (el) => {
    if (lenis) lenis.scrollTo(el, { offset: 0, duration: 1.4 });
    else el.scrollIntoView();
  };

  /* anchors ride Lenis; the mobile menu closes itself */
  $$('a[href^="#"]').forEach((a) => {
    a.addEventListener("click", (e) => {
      const id = a.getAttribute("href");
      if (id.length < 2) return;
      const target = $(id);
      if (!target) return;
      e.preventDefault();
      history.replaceState(null, "", id);
      const toggle = $("#nav-toggle");
      if (toggle) toggle.checked = false;
      scrollToTarget(target);
    });
  });

  /* refresh pin measurements once art loads */
  $$("img").forEach((img) => img.addEventListener("load", () => ScrollTrigger.refresh(), { once: true }));
  window.addEventListener("load", () => ScrollTrigger.refresh());

  /* ============================== REVEALS ============================== */
  const revealLines = (el, opts = {}) => {
    if (!splitOK || window.innerWidth < 768) {
      gsap.from(el, {
        y: 24, opacity: 0, duration: 1.0, ease: "expo.out",
        scrollTrigger: { trigger: el, start: "top 82%", once: opts.once !== false },
      });
      return;
    }
    const split = new SplitType(el, { types: "lines", mask: "lines" });
    gsap.from(split.lines || [el], {
      yPercent: 110, opacity: 0, duration: 0.95, ease: "expo.out",
      stagger: opts.stagger || 0.06,
      scrollTrigger: { trigger: el, start: "top 82%", once: opts.once !== false },
    });
  };

  /* ============================== COUNTERS ============================== */
  const initCounters = () => {
    const fmt = new Intl.NumberFormat("en-US");
    $$("[data-count]").forEach((el) => {
      const end = parseFloat(el.dataset.count);
      const year = el.hasAttribute("data-year");
      const obj = { v: 0 };
      gsap.to(obj, {
        v: end, duration: 1.6, ease: "expo.out",
        scrollTrigger: { trigger: el, start: "top 88%", once: true },
        onUpdate: () => {
          el.textContent = year ? String(Math.round(obj.v)) : fmt.format(Math.round(obj.v));
        },
      });
    });
  };

  /* ============================== HERO — the layer resolve ============================== */
  const initHero = () => {
    const typeIn = (el) => {
      const text = el.dataset.txt || (el.dataset.txt = el.textContent.trim());
      if (el.dataset.typed === "1") return;
      el.dataset.typed = "1";
      el.textContent = "";
      el.classList.add("typing");
      let i = 0;
      const step = () => {
        i++;
        el.textContent = text.slice(0, i);
        if (i < text.length) {
          setTimeout(step, 34 + Math.random() * 46);
        } else {
          el.classList.remove("typing");
        }
      };
      step();
    };

    /* construction strokes: draw on via dashoffset */
    const shapeEls = $$(".hero__annos .anno-shape > *");
    shapeEls.forEach((s) => {
      s.setAttribute("pathLength", "1");
      gsap.set(s, { strokeDasharray: 1, strokeDashoffset: 1 });
    });

    const tl = gsap.timeline({
      defaults: { ease: "none" },
      scrollTrigger: {
        trigger: ".hero", start: "top top", end: "+=100%",
        pin: true, scrub: 0.5, anticipatePin: 1,
      },
    });

    /* silhouette → flats → final render */
    tl.fromTo(".hero__pass--flat",
      { clipPath: "inset(100% 0% 0% 0%)" },
      { clipPath: "inset(0% 0% 0% 0%)", duration: 0.5 }, 0);
    tl.fromTo(".hero__pass--final",
      { clipPath: "inset(0% 100% 0% 0%)", opacity: 0 },
      { clipPath: "inset(0% 0% 0% 0%)", opacity: 1, duration: 0.4 }, 0.35);

    /* the name breathes against the resolving art */
    tl.to(".hero__name", { yPercent: -8, duration: 1 }, 0);

    /* annotations draw on, one by one, names type out */
    $$(".hero__annos .anno-item").forEach((item, idx) => {
      const els = $$("svg > *", item);
      if (!els.length) return; // margin notes carry no construction mark
      els.forEach((s) => {
        s.setAttribute("pathLength", "1");
        gsap.set(s, { strokeDasharray: 1, strokeDashoffset: 1 });
      });
      const pos = 0.14 + idx * 0.12;
      tl.from(item, { opacity: 0, y: 14, duration: 0.05 }, pos);
      tl.to(els, { strokeDashoffset: 0, duration: 0.06, stagger: 0.04 }, pos + 0.01);
      const nameEl = $(":scope > .anno", item);
      if (nameEl) tl.call(() => typeIn(nameEl), null, pos + 0.03);
    });

    tl.from(".anno-item--6", { opacity: 0, duration: 0.05 }, 0.72);
    tl.from(".hero__oneline", { opacity: 0, y: 10, duration: 0.05 }, 0.8);
  };

  /* ============================== AWARD — the trophy moment ============================== */
  const initAward = () => {
    const img = $(".award__trophy-img");

    const tl = gsap.timeline({
      defaults: { ease: "none" },
      scrollTrigger: {
        trigger: ".award", start: "top top", end: "+=120%",
        pin: true, scrub: 0.5, anticipatePin: 1,
      },
    });

    tl.fromTo(img,
      { yPercent: 62, rotate: -8, opacity: 0, scale: 0.94 },
      { yPercent: 0, rotate: 0, opacity: 1, scale: 1, duration: 0.45, ease: "expo.out" }, 0.04);
    tl.fromTo(".award__bloom", { opacity: 0 }, { opacity: 1, duration: 0.3 }, 0.04);

    /* kinetic type, masked line reveals, staggered */
    [
      ["--1", 0.28],
      ["--2", 0.36],
      ["--3", 0.44],
    ].forEach(([mod, pos]) => {
      tl.fromTo(`.award__line${mod} .display`,
        { yPercent: 112 }, { yPercent: 0, duration: 0.08, ease: "expo.out" }, pos);
    });

    tl.fromTo(".award__caa", { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.08 }, 0.56);
    tl.fromTo(".award__rule", { scaleX: 0 }, { scaleX: 1, duration: 0.1, ease: "power2.inOut" }, 0.64);

    /* the trophy reads scroll velocity */
    ScrollTrigger.create({
      trigger: ".award", start: "top top", end: "+=120%",
      onUpdate: (self) => {
        const v = gsap.utils.clamp(-7, 7, self.getVelocity() / 260);
        gsap.to(img, { rotation: v, duration: 0.5, overwrite: "auto" });
      },
    });
  };

  /* ============================== ABOUT — shape cycles per paragraph ============================== */
  const initAbout = () => {
    const labels = ["SQUARE — STUBBORN", "TRIANGLE — AGGRESSION", "CIRCLE — WARMTH"];
    const paras = $$(".about__flow .prose");
    const shapes = [$(".about__shape-sq"), $(".about__shape-tri"), $(".about__shape-cir")];
    const labelEl = $(".about__shape-label");

    shapes.forEach((s, i) => { if (i > 0) gsap.set(s, { opacity: 0, scale: 0.6 }); });

    paras.forEach((p, i) => {
      revealLines(p, { stagger: 0.06 });
      ScrollTrigger.create({
        trigger: p, start: "top 62%", end: "bottom 62%",
        onToggle: (self) => {
          if (!self.isActive) return;
          const idx = i % 3;
          shapes.forEach((s, k) => {
            gsap.to(s, {
              opacity: k === idx ? 1 : 0,
              scale: k === idx ? 1 : 0.6,
              rotate: k === idx ? 0 : -24,
              duration: 0.6, ease: "power2.inOut",
            });
          });
          labelEl.textContent = labels[idx];
        },
      });
    });
  };

  /* ============================== PORTFOLIO — x-ray + horizontal travel ============================== */
  const initPortfolio = () => {
    const track = $(".portfolio__track");

    /* x-ray: circular clip follows the pointer, radius eases */
    $$(".work-card__media").forEach((media) => {
      const sketch = $(".work-card__img--sketch", media);
      if (!sketch) return;

      let ra = 0, rt = 0, raf = 0;
      const maxR = () => {
        const r = media.getBoundingClientRect();
        return Math.max(r.width, r.height) * 0.6;
      };
      const easeTo = () => {
        ra += (rt - ra) * 0.14;
        if (Math.abs(rt - ra) < 0.6) ra = rt;
        sketch.style.clipPath = `circle(${ra}px at var(--mx, 50%) var(--my, 50%))`;
        if (ra !== rt) raf = requestAnimationFrame(easeTo);
      };
      const aim = (x, y) => {
        const r = media.getBoundingClientRect();
        media.style.setProperty("--mx", `${(x - r.left).toFixed(1)}px`);
        media.style.setProperty("--my", `${(y - r.top).toFixed(1)}px`);
      };
      const open = (x, y) => { aim(x, y); rt = maxR(); cancelAnimationFrame(raf); raf = requestAnimationFrame(easeTo); };
      const close = () => { rt = 0; cancelAnimationFrame(raf); raf = requestAnimationFrame(easeTo); };

      media.addEventListener("pointermove", (e) => { if (!media.dataset.pinned) open(e.clientX, e.clientY); });
      media.addEventListener("pointerleave", () => { if (!media.dataset.pinned) close(); });

      if (TOUCH) {
        media.addEventListener("click", (e) => {
          if (!media.dataset.pinned) {
            e.preventDefault();               // first tap reveals the sketch
            media.dataset.pinned = "1";
            open(e.clientX, e.clientY);
          } else {
            delete media.dataset.pinned;      // second tap navigates
            close();
          }
        });
      }
    });

    /* desktop: vertical scroll drives horizontal travel,
       track at 1.0x, captions at 1.15x */
    const mm = gsap.matchMedia();
    mm.add("(min-width: 901px)", () => {
      const metas = $$(".work-card__meta");
      const dist = () => Math.max(0, track.scrollWidth - document.documentElement.clientWidth + 40);

      gsap.to(track, {
        x: () => -dist(), ease: "none",
        scrollTrigger: {
          trigger: ".portfolio", start: "top top", end: () => "+=" + dist(),
          pin: true, scrub: 1, invalidateOnRefresh: true, anticipatePin: 1,
        },
      });

      gsap.to(metas, {
        x: () => -0.15 * dist(), ease: "none",
        scrollTrigger: {
          trigger: ".portfolio", start: "top top", end: () => "+=" + dist(),
          scrub: 1, invalidateOnRefresh: true,
        },
      });
    });
  };

  /* ============================== CREATE / CONFORM — the page takes the test ============================== */
  const initConform = () => {
    const section = $(".conform");
    if (!section) return;
    const tint = $(".conform__tint");
    const marks = $$(".conform__marks svg");
    const line = $(".conform__line");
    const wordL = $(".conform__side--left");
    const wordR = $(".conform__side--right");
    const mix = { v: 0.5 };

    /* scatter (CREATE) and rigid grid (CONFORM) positions */
    const scatter = [], rigid = [];
    const measure = () => {
      const W = section.clientWidth, H = section.clientHeight;
      const sc = [[16, 22], [72, 18], [28, 68], [62, 76], [46, 44]];
      const rg = [[30, 50], [40, 50], [50, 50], [60, 50], [70, 50]];
      sc.forEach(([px, py], i) => {
        scatter[i] = { x: (W * px) / 100 - W / 2, y: (H * py) / 100 - H / 2 };
      });
      rg.forEach(([px, py], i) => {
        rigid[i] = { x: (W * px) / 100 - W / 2, y: (H * py) / 100 - H / 2 };
      });
    };
    measure();
    window.addEventListener("resize", measure);

    gsap.set(marks, { left: "50%", top: "50%", xPercent: -50, yPercent: -50 });

    const apply = () => {
      const m = mix.v;
      section.style.filter = `grayscale(${(1 - m).toFixed(3)})`;
      tint.style.opacity = (0.16 * m).toFixed(3);
      line.style.letterSpacing = `${(0.02 + 0.1 * m).toFixed(3)}em`;
      wordL.style.opacity = 1 - m;
      wordR.style.opacity = m;
      marks.forEach((el, i) => {
        const s = scatter[i], r = rigid[i];
        gsap.set(el, {
          x: r.x + (s.x - r.x) * m,
          y: r.y + (s.y - r.y) * m,
          rotation: m * (i * 17 - 34),
        });
      });
    };
    apply();

    if (TOUCH) {
      /* no pointer to test with — the test takes itself, slowly */
      gsap.to(mix, {
        v: 1, duration: 4.5, ease: "sine.inOut",
        yoyo: true, repeat: -1, repeatDelay: 1.4, onUpdate: apply,
      });
    } else {
      const setMix = gsap.quickTo(mix, "v", { duration: 0.7, ease: "power2.out", onUpdate: apply });
      section.addEventListener("pointermove", (e) => {
        const r = section.getBoundingClientRect();
        setMix(gsap.utils.clamp(0, 1, (e.clientX - r.left) / r.width));
      });
      section.addEventListener("pointerleave", () => setMix(0.5));
    }
  };

  /* ============================== FOOTER — the scramble ============================== */
  const initScramble = () => {
    const el = $(".footer__email");
    if (!el) return;
    const target = el.textContent.trim();
    const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    let raf = 0;

    const scramble = () => {
      cancelAnimationFrame(raf);
      let frame = 0;
      const total = 14;
      const tick = () => {
        frame++;
        const p = frame / total;
        el.textContent = target.split("").map((c, i) => {
          if (c === "@" || c === ".") return c;
          if (i < p * target.length) return c;
          return chars[(Math.random() * chars.length) | 0];
        }).join("");
        if (frame < total) raf = requestAnimationFrame(tick);
        else el.textContent = target;
      };
      tick();
    };

    el.addEventListener("mouseenter", scramble);
    el.addEventListener("focus", scramble);
  };

  /* ============================== PRELOADER ============================== */
  const initPreloader = (onLoaded) => {
    const skip = () => {
      document.documentElement.classList.remove("is-locked");
      if (lenis) lenis.start();
      onLoaded();
    };

    if (sessionStorage.getItem("uzo-preload")) { skip(); return; }
    try { sessionStorage.setItem("uzo-preload", "1"); } catch (e) { /* private mode */ }

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
      <div class="preload__sil">
        <img src="assets/hero-sil-1.png" alt="">
        <img src="assets/hero-sil-2.png" alt="">
        <img src="assets/hero-sil-3.png" alt="">
        <img src="assets/hero-sil-4.png" alt="">
        <img src="assets/hero-sil-5.png" alt="">
      </div>`;
    document.body.prepend(pre);

    const pct = $(".preload__pct");
    const poly = $(".preload__shape polygon");
    const sils = $$(".preload__sil img");
    const counter = { v: 0 };
    const pad3 = (n) => String(n).padStart(3, "0");

    /* square → triangle → circle, one continuous morph (8-pt polygons) */
    const SQ = "2,2 20,2 38,2 38,20 38,38 20,38 2,38 2,20";
    const TRI = "20,2 29,2 38,20 38,38 20,38 2,38 2,20 11,2";
    const CIR = "20,3 30,8.5 37,20 30,31.5 20,37 10,31.5 3,20 10,8.5";

    const finish = () => {
      gsap.to(pre, {
        yPercent: -100, duration: 0.6, ease: "expo.inOut",
        onComplete: () => { pre.remove(); skip(); },
      });
    };

    const tl = gsap.timeline({ onComplete: finish });
    tl.to(counter, {
      v: 100, duration: 1.15, ease: "power2.out",
      onUpdate: () => { pct.textContent = pad3(Math.round(counter.v)); },
    }, 0);
    tl.to(poly, { attr: { points: TRI }, duration: 0.48, ease: "power2.inOut" }, 0.1);
    tl.to(poly, { attr: { points: CIR }, duration: 0.48, ease: "power2.inOut" }, 0.6);
    /* the shape explodes into the five silhouettes */
    tl.to(".preload__shape", { scale: 1.7, opacity: 0, duration: 0.32, ease: "power2.inOut" }, 1.15);
    tl.to(".preload__line", { opacity: 0, duration: 0.2 }, 1.15);
    tl.to(sils, { opacity: 1, scale: 1, duration: 0.5, ease: "power2.inOut", stagger: 0.04 }, 1.18);
  };

  /* ============================== BOOT ============================== */
  const heroEntrance = () => {
    gsap.fromTo(".hero__name span",
      { y: 26, opacity: 0 },
      { y: 0, opacity: 1, duration: 1.05, ease: "expo.out", stagger: 0.08 });
    gsap.fromTo(".hero__oneline", { opacity: 0 }, { opacity: 1, duration: 1, delay: 0.2, ease: "expo.out" });
    gsap.fromTo(".hero__corner", { opacity: 0 }, { opacity: 1, duration: 0.9, delay: 0.3, ease: "expo.out" });
  };

  initHero();
  initAward();
  initAbout();
  initPortfolio();
  initConform();
  initCounters();
  initScramble();
  initPreloader(heroEntrance);
})();


/* ============================================================
   UZOMA DUNKWU — UNIFIED APP
   SPA Router + Cinematic Transitions + All Animation Systems
   ============================================================ */

(function() {
  'use strict';

  // ============================================================
  // CONFIG
  // ============================================================
  const CFG = {
    easeOutExpo: 'power4.out',
    easeOutQuart: 'power3.out',
    easeInOutCirc: 'circ.inOut',
    easeElastic: 'elastic.out(1, 0.5)',
    durationFast: 0.4,
    durationNormal: 0.8,
    durationSlow: 1.2,
    stagger: 0.08
  };

  // ============================================================
  // STATE
  // ============================================================
  const State = {
    currentPage: 'home',
    isTransitioning: false,
    lenis: null,
    lightboxIndex: 0,
    lightboxItems: [],
    scrubInstances: new Map()
  };

  // ============================================================
  // DOM CACHE
  // ============================================================
  const DOM = {
    preloader: document.getElementById('preloader'),
    preloaderFill: document.getElementById('preloader-fill'),
    preloaderPct: document.getElementById('preloader-pct'),
    cursor: document.getElementById('cursor'),
    cursorDot: document.querySelector('.cursor__dot'),
    cursorRing: document.querySelector('.cursor__ring'),
    cursorGlow: document.querySelector('.cursor__glow'),
    cursorLabel: document.getElementById('cursor-label'),
    curtain: document.getElementById('curtain'),
    curtainWord: document.getElementById('curtain-word'),
    curtainLeft: document.querySelector('.curtain__panel--left'),
    curtainRight: document.querySelector('.curtain__panel--right'),
    lightbox: document.getElementById('lightbox'),
    lightboxImg: document.getElementById('lightbox-img'),
    lightboxNo: document.getElementById('lightbox-no'),
    lightboxTitle: document.getElementById('lightbox-title'),
    lightboxClose: document.getElementById('lightbox-close'),
    lightboxPrev: document.getElementById('lightbox-prev'),
    lightboxNext: document.getElementById('lightbox-next'),
    nav: document.querySelector('.site-nav'),
    navLinks: document.querySelectorAll('.site-nav__link'),
    siteHead: document.getElementById('site-head')
  };

  // ============================================================
  // UTILITIES
  // ============================================================
  const U = {
    qs: (s, c) => (c || document).querySelector(s),
    qsa: (s, c) => Array.from((c || document).querySelectorAll(s)),
    clamp: (v, min, max) => Math.min(max, Math.max(min, v)),
    lerp: (a, b, t) => a + (b - a) * t,
    randomChar: () => {
      const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*';
      return chars[Math.floor(Math.random() * chars.length)];
    }
  };

  // ============================================================
  // PRELOADER
  // ============================================================
  function initPreloader() {
    // Only wait on images that the browser will actually fetch right now:
    // eager images inside the page that is visible. Lazy images in hidden
    // pages never load, and preload="none" videos never fire loadeddata.
    const assets = U.qsa('img[src]').filter(el =>
      el.loading !== 'lazy' && el.closest('.page, body') && !el.closest('.page:not(.is-active)')
    );
    const total = assets.length;
    let loaded = 0;
    let finished = false;

    function update(pct) {
      if (DOM.preloaderFill) DOM.preloaderFill.style.width = pct + '%';
      if (DOM.preloaderPct) DOM.preloaderPct.textContent = Math.round(pct) + '%';
    }

    function done() {
      if (finished) return;
      finished = true;
      update(100);
      setTimeout(() => {
        DOM.preloader.classList.add('is-done');
        document.documentElement.classList.add('is-ready');
        setTimeout(() => {
          DOM.preloader.style.display = 'none';
          initRouter();
        }, 800);
      }, 400);
    }

    // Hard ceiling: the page must never be held hostage by one slow file.
    setTimeout(done, 4000);

    if (total === 0) { done(); return; }

    const tick = () => { loaded++; update((loaded / total) * 100); if (loaded >= total) done(); };
    assets.forEach(el => {
      if (el.complete && el.naturalWidth) tick();
      else { el.onload = el.onerror = tick; }
    });
  }

  // ============================================================
  // CUSTOM CURSOR
  // ============================================================
  function initCursor() {
    if (window.matchMedia('(pointer: coarse)').matches) {
      DOM.cursor.style.display = 'none';
      document.body.style.cursor = 'auto';
      U.qsa('a, button').forEach(el => el.style.cursor = 'pointer');
      return;
    }

    let mx = 0, my = 0, dx = 0, dy = 0, rx = 0, ry = 0;
    let active = true, raf = null;

    document.addEventListener('mousemove', e => { mx = e.clientX; my = e.clientY; if (!active) { active = true; loop(); } });

    function loop() {
      if (!active) return;
      dx = U.lerp(dx, mx, 0.2);
      dy = U.lerp(dy, my, 0.2);
      rx = U.lerp(rx, mx, 0.12);
      ry = U.lerp(ry, my, 0.12);
      DOM.cursorDot.style.transform = `translate(${dx}px, ${dy}px)`;
      DOM.cursorRing.style.transform = `translate(${rx}px, ${ry}px)`;
      DOM.cursorGlow.style.transform = `translate(${rx}px, ${ry}px)`;
      DOM.cursorLabel.style.transform = `translate(${rx}px, ${ry}px)`;
      raf = requestAnimationFrame(loop);
    }
    loop();

    // State machine
    const setState = (state, label) => {
      DOM.cursor.className = 'cursor' + (state ? ' ' + state : '');
      if (label) DOM.cursorLabel.textContent = label;
    };

    document.addEventListener('mouseover', e => {
      const t = e.target;
      if (t.closest('[data-plate], .plate__btn')) return setState('is-viewing', 'VIEW');
      if (t.closest('[data-scrub], .scrub__stage')) return setState('is-dragging', 'DRAG');
      if (t.closest('[data-play], .film__play')) return setState('is-playing', 'PLAY');
      if (t.closest('a, button, [data-magnet]')) return setState('is-linking');
      setState('');
    });

    document.addEventListener('mouseout', e => {
      if (!e.relatedTarget || !e.relatedTarget.closest('a, button, [data-magnet], [data-plate], [data-scrub], [data-play]')) {
        setState('');
      }
    });

    // Magnetic buttons
    U.qsa('[data-magnet]').forEach(el => {
      const str = parseFloat(el.dataset.magnet) || 0.3;
      el.addEventListener('mousemove', e => {
        const r = el.getBoundingClientRect();
        el.style.transform = `translate(${(e.clientX - r.left - r.width/2) * str}px, ${(e.clientY - r.top - r.height/2) * str}px)`;
      });
      el.addEventListener('mouseleave', () => { el.style.transform = ''; });
    });

    document.addEventListener('visibilitychange', () => {
      if (document.hidden) { active = false; cancelAnimationFrame(raf); }
      else { active = true; loop(); }
    });
  }

  // ============================================================
  // LENIS + SCROLLTRIGGER
  // ============================================================
  function initLenis() {
    State.lenis = new Lenis({
      duration: 1.2,
      easing: t => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
      smoothWheel: true
    });

    // Driven by the GSAP ticker only — a second rAF loop double-steps it.
    State.lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add(time => State.lenis.raf(time * 1000));
    gsap.ticker.lagSmoothing(0);

    // Nav scroll state
    State.lenis.on('scroll', ({ scroll }) => {
      DOM.siteHead.classList.toggle('is-scrolled', scroll > 100);
    });
  }

  // ============================================================
  // CURTAIN TRANSITION
  // ============================================================
  function playCurtain(text, onMid, onEnd) {
    const tl = gsap.timeline();
    DOM.curtain.classList.add('is-active');
    DOM.curtainWord.textContent = text || '';

    // Panels close
    tl.fromTo(DOM.curtainLeft, { x: '-100%' }, { x: '0%', duration: 0.5, ease: CFG.easeOutExpo }, 0);
    tl.fromTo(DOM.curtainRight, { x: '100%' }, { x: '0%', duration: 0.5, ease: CFG.easeOutExpo }, 0);

    // Text reveal
    tl.fromTo(DOM.curtainWord, { y: '100%', opacity: 0 }, { y: '0%', opacity: 1, duration: 0.4, ease: CFG.easeOutExpo }, 0.3);

    // Hold
    tl.to({}, { duration: 0.3 });

    // Callback at midpoint
    tl.call(() => { if (onMid) onMid(); });

    // Text exit
    tl.to(DOM.curtainWord, { y: '-100%', opacity: 0, duration: 0.3, ease: 'power2.in' });

    // Panels open
    tl.to(DOM.curtainLeft, { x: '-100%', duration: 0.5, ease: CFG.easeOutExpo }, '+=0.1');
    tl.to(DOM.curtainRight, { x: '100%', duration: 0.5, ease: CFG.easeOutExpo }, '<');

    tl.call(() => {
      DOM.curtain.classList.remove('is-active');
      if (onEnd) onEnd();
    });

    return tl;
  }

  // ============================================================
  // ROUTER
  // ============================================================
  function initRouter() {
    // Parse initial URL
    const hash = location.hash.replace('#', '');
    const path = location.pathname.replace(/^\//, '');
    const pages = ['home', 'eow', 'iyanu', 'personal', 'storyboards'];

    let startPage = 'home';
    let startScroll = null;
    let startHash = null;

    if (pages.includes(hash)) {
      startPage = hash;
    } else if (pages.includes(path)) {
      startPage = path;
    } else if (hash) {
      // Could be a section scroll on home, or a film hash on storyboards
      const homeSections = ['about', 'portfolio', 'products', 'contact', 'hero', 'teaching', 'conform'];
      const filmHashes = ['coma-toes', 'cash-trapped', 'cash-trapped-two'];
      if (homeSections.includes(hash)) { startScroll = hash; }
      else if (filmHashes.includes(hash)) { startPage = 'storyboards'; startHash = hash; }
    }

    // Hide all pages, show start page
    U.qsa('.page').forEach(p => p.classList.remove('is-active'));
    const startEl = document.getElementById('page-' + startPage);
    if (startEl) startEl.classList.add('is-active');
    State.currentPage = startPage;
    updateNavActive(startPage);

    // Run entrance
    setTimeout(() => {
      runPageEntrance(startPage, () => {
        if (startScroll) scrollToSection(startScroll);
        if (startHash) scrollToHash(startHash);
      });
    }, 100);

    // Nav click handlers
    U.qsa('[data-nav]').forEach(link => {
      link.addEventListener('click', e => {
        e.preventDefault();
        const page = link.dataset.nav;
        const scroll = link.dataset.scroll;
        const hash = link.dataset.hash;

        if (page === State.currentPage && scroll) {
          scrollToSection(scroll);
          return;
        }
        if (page === State.currentPage && hash) {
          scrollToHash(hash);
          return;
        }

        navigateTo(page, { scroll, hash });
      });
    });

    // Browser back/forward
    window.addEventListener('popstate', () => {
      const h = location.hash.replace('#', '');
      const p = location.pathname.replace(/^\//, '');
      const target = pages.includes(h) ? h : pages.includes(p) ? p : 'home';
      if (target !== State.currentPage) {
        navigateTo(target, { noPush: true });
      }
    });
  }

  function navigateTo(page, opts = {}) {
    if (State.isTransitioning || page === State.currentPage) return;
    State.isTransitioning = true;

    const fromEl = document.getElementById('page-' + State.currentPage);
    const toEl = document.getElementById('page-' + page);
    if (!toEl) { State.isTransitioning = false; return; }

    // Get page label for curtain
    const labels = {
      home: 'HOME',
      eow: 'EYES OF WAKANDA',
      iyanu: 'IYANU',
      personal: 'PERSONAL',
      storyboards: 'STORYBOARDS'
    };

    // Exit current page
    const exitTl = gsap.timeline();
    const exitEls = fromEl.querySelectorAll('[data-reveal], .display, .prose, .anno-item, .case__fact, .frame, .plate, .board-tile, .work-card');
    exitTl.to(exitEls, { y: -30, opacity: 0, stagger: 0.01, duration: 0.35, ease: 'power2.in' });
    exitTl.to(fromEl, { opacity: 0, duration: 0.2, ease: 'power2.in' }, '-=0.15');

    exitTl.call(() => {
      fromEl.classList.remove('is-active');
      toEl.classList.add('is-active');
      State.currentPage = page;
      updateNavActive(page);
      window.scrollTo(0, 0);
      if (!opts.noPush) {
        history.pushState({}, '', page === 'home' ? location.pathname : '#' + page);
      }

      // Curtain transition
      playCurtain(labels[page] || '', null, () => {
        runPageEntrance(page, () => {
          State.isTransitioning = false;
          if (opts.scroll) setTimeout(() => scrollToSection(opts.scroll), 300);
          if (opts.hash) setTimeout(() => scrollToHash(opts.hash), 300);
        });
      });
    });
  }

  function updateNavActive(page) {
    DOM.navLinks.forEach(link => {
      const navPage = link.dataset.nav;
      link.classList.toggle('is-active', navPage === page);
      link.removeAttribute('aria-current');
      if (navPage === page) link.setAttribute('aria-current', 'page');
    });
  }

  function scrollToSection(id) {
    const el = document.getElementById(id);
    if (el && State.lenis) State.lenis.scrollTo(el, { offset: -80, duration: 1.5 });
  }

  function scrollToHash(id) {
    const el = document.getElementById(id);
    if (el && State.lenis) State.lenis.scrollTo(el, { offset: -100, duration: 1.5 });
  }

  // ============================================================
  // PAGE ENTRANCE ANIMATIONS
  // ============================================================
  function runPageEntrance(page, callback) {
    // the page is visible now, so its text can finally be measured and split
    initSplitReveals(document.getElementById('page-' + page));
    switch(page) {
      case 'home': entranceHome(callback); break;
      case 'eow': entranceWork('eow', callback); break;
      case 'iyanu': entranceWork('iyanu', callback); break;
      case 'personal': entranceWork('personal', callback); break;
      case 'storyboards': entranceStoryboards(callback); break;
      default: if (callback) callback();
    }
  }

  function entranceHome(cb) {
    const tl = gsap.timeline({ onComplete: cb });
    const page = document.getElementById('page-home');

    // Hero sheet 3D flip in
    const sheet = page.querySelector('.hero__sheet');
    if (sheet) {
      tl.fromTo(sheet,
        { rotateX: 20, y: 80, opacity: 0, scale: 0.9 },
        { rotateX: 0, y: 0, opacity: 1, scale: 1, duration: 1.2, ease: CFG.easeOutExpo }
      );
    }

    // Passes resolve
    const passes = page.querySelectorAll('.hero__pass');
    if (passes.length) {
      tl.fromTo(passes[0], { opacity: 0, filter: 'blur(30px)' }, { opacity: 1, filter: 'blur(0px)', duration: 0.6 }, '-=0.6');
      tl.to(passes[1], { opacity: 1, duration: 0.5 }, '+=0.2');
      tl.to(passes[0], { opacity: 0, duration: 0.3 }, '<0.2');
      tl.to(passes[2], { opacity: 1, duration: 0.5 }, '+=0.15');
      tl.to(passes[1], { opacity: 0, duration: 0.3 }, '<0.2');
      tl.to(passes[3], { opacity: 1, duration: 0.7 }, '+=0.15');
      tl.to(passes[2], { opacity: 0, duration: 0.4 }, '<0.3');
    }

    // Meta tags
    tl.to(page.querySelectorAll('.hero__meta .anno'), { x: 0, opacity: 1, stagger: 0.1, duration: 0.5 }, '-=0.3');

    // Name character reveal
    const nameChars = page.querySelectorAll('.hero__word span');
    if (nameChars.length) {
      tl.fromTo(nameChars,
        { y: '120%', opacity: 0, rotateX: -90 },
        { y: '0%', opacity: 1, rotateX: 0, duration: 0.7, stagger: 0.03, ease: CFG.easeOutExpo },
        '-=0.4'
      );
    }

    // Annotations
    tl.to(page.querySelectorAll('.anno-item'), { opacity: 1, y: 0, stagger: 0.08, duration: 0.5 }, '-=0.3');

    // Base info
    tl.fromTo(page.querySelector('.hero__base'), { y: 20, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5 }, '-=0.2');

    // Init home scroll animations
    initHomeScrollAnimations();
  }

  function entranceWork(pageId, cb) {
    const page = document.getElementById('page-' + pageId);
    const tl = gsap.timeline({ onComplete: cb });

    tl.fromTo(page.querySelector('.case__title'),
      { y: 60, opacity: 0 },
      { y: 0, opacity: 1, duration: 1, ease: CFG.easeOutExpo }
    );
    tl.fromTo(page.querySelectorAll('.case__fact'),
      { y: 20, opacity: 0 },
      { y: 0, opacity: 1, stagger: 0.1, duration: 0.6, ease: CFG.easeOutQuart },
      '-=0.6'
    );
    tl.fromTo(page.querySelector('.case__intro'),
      { y: 20, opacity: 0 },
      { y: 0, opacity: 1, duration: 0.6, ease: CFG.easeOutQuart },
      '-=0.4'
    );
    tl.fromTo(page.querySelector('.case__sheet'),
      { y: 60, opacity: 0, scale: 0.95 },
      { y: 0, opacity: 1, scale: 1, duration: 1.2, ease: CFG.easeOutExpo },
      '-=0.4'
    );

    initWorkScrollAnimations(page);
  }

  function entranceStoryboards(cb) {
    const page = document.getElementById('page-storyboards');
    const tl = gsap.timeline({ onComplete: cb });

    tl.fromTo(page.querySelector('.case__title'),
      { y: 60, opacity: 0 },
      { y: 0, opacity: 1, duration: 1, ease: CFG.easeOutExpo }
    );
    tl.fromTo(page.querySelectorAll('.case__fact'),
      { y: 20, opacity: 0 },
      { y: 0, opacity: 1, stagger: 0.1, duration: 0.6 },
      '-=0.6'
    );
    tl.fromTo(page.querySelectorAll('.frame'),
      { y: 30, opacity: 0, scale: 0.96 },
      { y: 0, opacity: 1, scale: 1, stagger: 0.06, duration: 0.6, ease: CFG.easeOutQuart },
      '-=0.3'
    );

    initBoardsAnimations();
  }

  // ============================================================
  // HOME SCROLL ANIMATIONS
  // ============================================================
  function initHomeScrollAnimations() {
    const page = document.getElementById('page-home');
    if (!page) return;

    // Hero parallax
    gsap.to(page.querySelector('.hero__sheet'), {
      y: -80, rotationY: 5, ease: 'none',
      scrollTrigger: { trigger: page.querySelector('.hero'), start: 'top top', end: 'bottom top', scrub: 1 }
    });
    gsap.to(page.querySelector('.hero__name'), {
      y: -40, opacity: 0, ease: 'none',
      scrollTrigger: { trigger: page.querySelector('.hero'), start: 'top top', end: '50% top', scrub: 1 }
    });

    // Award section
    const awardTl = gsap.timeline({
      scrollTrigger: { trigger: page.querySelector('.award'), start: 'top 70%', once: true }
    });
    awardTl.fromTo(page.querySelector('.award__trophy-img'),
      { y: 60, opacity: 0, rotateY: -30 },
      { y: 0, opacity: 1, rotateY: 0, duration: 1, ease: CFG.easeOutExpo }
    );
    awardTl.fromTo(page.querySelector('.award__line--1 .display'), { y: '100%' }, { y: '0%', duration: 0.8 }, '-=0.6');
    awardTl.fromTo(page.querySelector('.award__line--2 .display'), { y: '100%' }, { y: '0%', duration: 0.8 }, '-=0.5');
    awardTl.fromTo(page.querySelector('.award__line--3 .display'), { y: 20, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6 }, '-=0.3');
    awardTl.fromTo(page.querySelector('.award__caa'), { y: 20, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6 }, '-=0.2');
    awardTl.fromTo(page.querySelector('.award__rule'), { scaleX: 0 }, { scaleX: 1, duration: 0.8 }, '-=0.2');

    // Award ghost parallax
    gsap.to(page.querySelector('.award__ghost'), {
      y: -60, rotation: 3, ease: 'none',
      scrollTrigger: { trigger: page.querySelector('.award'), start: 'top bottom', end: 'bottom top', scrub: 1 }
    });

    // About prose stagger
    gsap.fromTo(page.querySelectorAll('.about__flow .prose'),
      { y: 40, opacity: 0 },
      { y: 0, opacity: 1, stagger: 0.15, duration: 0.8, ease: CFG.easeOutQuart,
        scrollTrigger: { trigger: page.querySelector('.about__flow'), start: 'top 75%', once: true }
      }
    );

    // About shape morph
    const aboutShape = page.querySelector('.about__shape');
    const aboutLabel = page.querySelector('.about__shape-label');
    if (aboutShape) {
      const svgs = aboutShape.querySelectorAll('svg');
      const shapes = [
        { name: 'SQUARE — STUBBORN', active: 0 },
        { name: 'TRIANGLE — AGILE', active: 1 },
        { name: 'CIRCLE — WHOLE', active: 2 }
      ];
      let idx = 0;
      ScrollTrigger.create({
        trigger: page.querySelector('.about'),
        start: 'top center', end: 'bottom center',
        onUpdate: (self) => {
          const newIdx = Math.min(2, Math.floor(self.progress * 3));
          if (newIdx !== idx) {
            idx = newIdx;
            svgs.forEach((svg, i) => {
              if (i === shapes[idx].active) {
                gsap.to(svg, { opacity: 1, scale: 1, rotation: 0, duration: 0.6, ease: 'back.out(1.7)' });
              } else {
                gsap.to(svg, { opacity: 0, scale: 0.8, rotation: i < shapes[idx].active ? -90 : 90, duration: 0.4 });
              }
            });
            if (aboutLabel) {
              gsap.to(aboutLabel, { opacity: 0, duration: 0.2, onComplete: () => {
                aboutLabel.textContent = shapes[idx].name;
                gsap.to(aboutLabel, { opacity: 1, duration: 0.3 });
              }});
            }
          }
        }
      });
    }

    // Wall parallax columns
    const wallCols = page.querySelector('.wall__cols');
    if (wallCols) {
      const artworks = [
        'assets/thumbs/eow/eow-01-lineup.jpg','assets/thumbs/eow/eow-02-noni.jpg',
        'assets/thumbs/eow/eow-03-noni-keys.jpg','assets/thumbs/eow/eow-04-old-noni.jpg',
        'assets/thumbs/eow/eow-05-traveller.jpg','assets/thumbs/eow/eow-06-councilman.jpg',
        'assets/thumbs/eow/eow-07-kuda.jpg','assets/thumbs/eow/eow-08-tafari.jpg',
        'assets/thumbs/eow/eow-09-lion-guard.jpg','assets/thumbs/eow/eow-10-chainmakers.jpg',
        'assets/thumbs/eow/eow-11-harem.jpg','assets/thumbs/eow/eow-12-seamstresses.jpg',
        'assets/thumbs/eow/eow-13-ethiopian.jpg','assets/thumbs/eow/eow-14-crowd.jpg',
        'assets/thumbs/eow/eow-15-dora.jpg','assets/thumbs/eow/eow-16-flashback.jpg',
        'assets/thumbs/eow/eow-17-dora-02.jpg','assets/thumbs/eow/eow-18-crowd-02.jpg',
        'assets/thumbs/eow/eow-19-crowd-03.jpg','assets/thumbs/iyanu/iyanu-01-ideation.jpg',
        'assets/thumbs/iyanu/iyanu-02-exploration.jpg','assets/thumbs/iyanu/iyanu-03-exploration.jpg',
        'assets/thumbs/iyanu/iyanu-04-biyi.jpg','assets/thumbs/iyanu/iyanu-05-biyi-02.jpg',
        'assets/thumbs/iyanu/iyanu-06-0621.jpg','assets/thumbs/iyanu/iyanu-07-0621-02.jpg',
        'assets/thumbs/personal/personal-01-afro-ninja.jpg','assets/thumbs/personal/personal-02-pirate.jpg',
        'assets/thumbs/personal/personal-03-vampire.jpg','assets/thumbs/personal/personal-04-femme.jpg',
        'assets/thumbs/personal/personal-05-hands.jpg','assets/thumbs/personal/personal-06-people.jpg',
        'assets/thumbs/personal/personal-07-mammal.jpg','assets/thumbs/personal/personal-08-gangster.jpg',
        'assets/thumbs/personal/personal-09-sketches.jpg','assets/thumbs/personal/personal-10-dump.jpg',
        'assets/thumbs/personal/personal-11-futuristic.jpg','assets/thumbs/personal/personal-12-sketch.jpg'
      ];
      const colCount = window.innerWidth < 900 ? 3 : 5;
      for (let i = 0; i < colCount; i++) {
        const col = document.createElement('div');
        col.className = 'wall__col';
        for (let j = 0; j < 8; j++) {
          const img = document.createElement('img');
          img.src = artworks[(i + j * colCount) % artworks.length];
          img.alt = ''; img.loading = 'lazy';
          col.appendChild(img);
        }
        wallCols.appendChild(col);
        gsap.to(col, {
          y: i % 2 === 0 ? -80 : 80, ease: 'none',
          scrollTrigger: { trigger: page.querySelector('.wall'), start: 'top bottom', end: 'bottom top', scrub: 1 }
        });
      }
    }

    // Portfolio cards
    gsap.fromTo(page.querySelectorAll('.work-card'),
      { y: 60, opacity: 0, rotateX: 10 },
      { y: 0, opacity: 1, rotateX: 0, stagger: 0.2, duration: 1, ease: CFG.easeOutExpo,
        scrollTrigger: { trigger: page.querySelector('.portfolio__track'), start: 'top 80%', once: true }
      }
    );

    // Portfolio 3D tilt + probe
    page.querySelectorAll('.work-card__link').forEach(card => {
      const probe = card.querySelector('.work-card__probe');
      card.addEventListener('mousemove', e => {
        const r = card.getBoundingClientRect();
        const x = (e.clientX - r.left) / r.width - 0.5;
        const y = (e.clientY - r.top) / r.height - 0.5;
        card.style.transform = `translateY(-6px) perspective(1000px) rotateX(${-y * 8}deg) rotateY(${x * 8}deg)`;
        if (probe) { probe.style.left = (e.clientX - r.left) + 'px'; probe.style.top = (e.clientY - r.top) + 'px'; }
      });
      card.addEventListener('mouseleave', () => { card.style.transform = ''; });
    });

    // Board tiles
    gsap.fromTo(page.querySelectorAll('.board-tile'),
      { y: 40, opacity: 0, scale: 0.95 },
      { y: 0, opacity: 1, scale: 1, stagger: 0.12, duration: 0.8, ease: CFG.easeOutQuart,
        scrollTrigger: { trigger: page.querySelector('.boards__row'), start: 'top 80%', once: true }
      }
    );
    page.querySelectorAll('.board-tile').forEach(tile => {
      const video = tile.querySelector('video');
      if (!video) return;
      tile.addEventListener('mouseenter', () => { video.play().catch(() => {}); });
      tile.addEventListener('mouseleave', () => { video.pause(); video.currentTime = 0; });
    });

    // Conform
    gsap.fromTo(page.querySelector('.conform__centre'), { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 1, ease: CFG.easeOutQuart,
      scrollTrigger: { trigger: page.querySelector('.conform'), start: 'top 60%', once: true }
    });
    gsap.to(page.querySelector('.conform__art'), {
      y: -100, scale: 1.15, ease: 'none',
      scrollTrigger: { trigger: page.querySelector('.conform'), start: 'top bottom', end: 'bottom top', scrub: 1 }
    });

    // Teaching counters
    page.querySelectorAll('.teaching__num').forEach(el => {
      const target = parseInt(el.dataset.count);
      if (!target) return;
      ScrollTrigger.create({
        trigger: el, start: 'top 85%', once: true,
        onEnter: () => {
          el.classList.add('is-shuffling');
          let frames = 0;
          const interval = setInterval(() => {
            frames++;
            el.textContent = Math.floor(Math.random() * target * 1.5).toLocaleString();
            if (frames >= 30) {
              clearInterval(interval);
              el.classList.remove('is-shuffling');
              gsap.to({ val: 0 }, { val: target, duration: 0.8, ease: 'power4.out',
                onUpdate: function() { el.textContent = Math.round(this.targets()[0].val).toLocaleString(); }
              });
            }
          }, 50);
        }
      });
    });

    // Products
    gsap.fromTo(page.querySelector('.products__visual'), { scale: 0.8, opacity: 0, rotation: -20 },
      { scale: 1, opacity: 1, rotation: 0, duration: 1.2, ease: CFG.easeOutExpo,
        scrollTrigger: { trigger: page.querySelector('.products'), start: 'top 75%', once: true }
      }
    );
    gsap.fromTo(page.querySelectorAll('.products__info > *'), { y: 30, opacity: 0 },
      { y: 0, opacity: 1, stagger: 0.1, duration: 0.7, ease: CFG.easeOutQuart,
        scrollTrigger: { trigger: page.querySelector('.products__info'), start: 'top 80%', once: true }
      }
    );

    // Footer socials
    gsap.fromTo(page.querySelectorAll('.footer__social'), { x: -20, opacity: 0 },
      { x: 0, opacity: 1, stagger: 0.08, duration: 0.5, ease: CFG.easeOutQuart,
        scrollTrigger: { trigger: page.querySelector('.footer__body'), start: 'top 90%', once: true }
      }
    );

    // Footer marquee speed
    const marqueeTrack = page.querySelector('.footer__marquee-track');
    if (marqueeTrack) {
      State.lenis.on('scroll', ({ velocity }) => {
        marqueeTrack.style.animationDuration = Math.max(5, 30 - Math.abs(velocity) * 0.5) + 's';
      });
    }
  }

  // ============================================================
  // WORK PAGE SCROLL ANIMATIONS
  // ============================================================
  function initWorkScrollAnimations(page) {
    if (!page) return;

    // Case sheet parallax
    const sheet = page.querySelector('.case__sheet');
    if (sheet) {
      gsap.fromTo(sheet, { y: 60, opacity: 0, scale: 0.96 },
        { y: 0, opacity: 1, scale: 1, duration: 1.2, ease: CFG.easeOutExpo,
          scrollTrigger: { trigger: sheet, start: 'top 80%', once: true }
        }
      );
    }

    // Next work peek
    const nextWork = page.querySelector('.next-work');
    if (nextWork) {
      const peek = nextWork.querySelector('.next-work__peek');
      if (peek) {
        gsap.to(peek, { y: -40, ease: 'none',
          scrollTrigger: { trigger: nextWork, start: 'top bottom', end: 'bottom top', scrub: 1 }
        });
      }
    }

    // Scrub sliders
    page.querySelectorAll('[data-scrub]').forEach(stage => {
      initScrub(stage);
    });

    // Plates reveal
    const plates = page.querySelectorAll('[data-reveal="plate"]');
    if (plates.length) {
      gsap.fromTo(plates, { opacity: 0, scale: 0.96, y: 20 },
        { opacity: 1, scale: 1, y: 0, duration: 0.7, stagger: 0.08, ease: CFG.easeOutQuart,
          scrollTrigger: { trigger: plates[0].closest('.plates__grid, .case'), start: 'top 80%', once: true }
        }
      );
    }
  }

  // ============================================================
  // SCRUB SLIDER
  // ============================================================
  function initScrub(stage) {
    const passes = stage.querySelectorAll('.scrub__pass');
    const handle = stage.querySelector('.scrub__handle');
    const input = stage.querySelector('.scrub__input');
    const stagesList = stage.parentElement.querySelector('.scrub__stages');
    const stageNames = stagesList?.querySelectorAll('[data-stage]');
    if (!passes.length || !handle || !input) return;

    const total = passes.length;
    let isDragging = false;

    function update(value) {
      const pct = value / 1000;
      const idx = Math.min(total - 1, Math.floor(pct * total));
      const progress = (pct * total) - idx;
      handle.style.left = (pct * 100) + '%';
      passes.forEach((pass, i) => {
        if (i < idx) pass.style.clipPath = 'inset(0 0 0 0)';
        else if (i === idx) pass.style.clipPath = `inset(0 ${100 - (progress * 100)}% 0 0)`;
        else pass.style.clipPath = 'inset(0 100% 0 0)';
      });
      stageNames?.forEach((name, i) => name.classList.toggle('is-on', i === idx));
    }

    input.addEventListener('input', e => update(parseInt(e.target.value)));
    stageNames?.forEach(name => {
      name.addEventListener('click', () => {
        const idx = parseInt(name.dataset.stage);
        const val = (idx / (total - 1)) * 1000;
        gsap.to(input, { value: val, duration: 0.6, ease: 'power2.out', onUpdate: () => update(parseInt(input.value)) });
      });
    });

    stage.addEventListener('mousedown', e => { if (e.target !== input) { isDragging = true; updateFromMouse(e); } });
    document.addEventListener('mousemove', e => { if (isDragging) updateFromMouse(e); });
    document.addEventListener('mouseup', () => isDragging = false);

    function updateFromMouse(e) {
      const r = stage.getBoundingClientRect();
      const val = Math.round(Math.max(0, Math.min(1, (e.clientX - r.left) / r.width)) * 1000);
      input.value = val; update(val);
    }

    stage.addEventListener('touchstart', e => { isDragging = true; updateFromTouch(e.touches[0]); }, { passive: true });
    stage.addEventListener('touchmove', e => { if (isDragging) updateFromTouch(e.touches[0]); }, { passive: true });
    stage.addEventListener('touchend', () => isDragging = false);

    function updateFromTouch(t) {
      const r = stage.getBoundingClientRect();
      const val = Math.round(Math.max(0, Math.min(1, (t.clientX - r.left) / r.width)) * 1000);
      input.value = val; update(val);
    }

    stage.addEventListener('keydown', e => {
      if (e.key === 'ArrowRight') { const v = Math.min(1000, parseInt(input.value) + 100); input.value = v; update(v); }
      else if (e.key === 'ArrowLeft') { const v = Math.max(0, parseInt(input.value) - 100); input.value = v; update(v); }
    });

    update(0);
    State.scrubInstances.set(stage, { update });
  }

  // ============================================================
  // STORYBOARD ANIMATIONS
  // ============================================================
  function initBoardsAnimations() {
    const page = document.getElementById('page-storyboards');
    if (!page) return;

    // Video play/pause
    page.querySelectorAll('[data-play]').forEach(btn => {
      const player = btn.closest('.film__player');
      const video = player?.querySelector('video');
      const label = btn.querySelector('[data-play-label]');
      if (!video) return;
      btn.addEventListener('click', () => {
        if (video.paused) { video.play(); video.muted = false; btn.classList.add('is-playing'); if (label) label.textContent = 'PAUSE'; }
        else { video.pause(); btn.classList.remove('is-playing'); if (label) label.textContent = 'PLAY THE ANIMATIC'; }
      });
      video.addEventListener('ended', () => { btn.classList.remove('is-playing'); if (label) label.textContent = 'PLAY THE ANIMATIC'; });
    });

    // Film strip drag
    page.querySelectorAll('[data-strip]').forEach(strip => {
      let isDown = false, startX, scrollLeft;
      strip.addEventListener('mousedown', e => { isDown = true; strip.style.cursor = 'grabbing'; startX = e.pageX - strip.offsetLeft; scrollLeft = strip.scrollLeft; });
      strip.addEventListener('mouseleave', () => { isDown = false; strip.style.cursor = 'grab'; });
      strip.addEventListener('mouseup', () => { isDown = false; strip.style.cursor = 'grab'; });
      strip.addEventListener('mousemove', e => { if (!isDown) return; e.preventDefault(); strip.scrollLeft = scrollLeft - (e.pageX - strip.offsetLeft - startX) * 2; });
    });
  }

  // ============================================================
  // LIGHTBOX
  // ============================================================
  function initLightbox() {
    // Collect all plate items across all pages
    function refreshItems() {
      State.lightboxItems = U.qsa('[data-plate]').map(btn => ({
        src: btn.dataset.plate,
        title: btn.dataset.title || '',
        no: btn.dataset.no || ''
      }));
    }
    refreshItems();

    function open(index) {
      if (index < 0 || index >= State.lightboxItems.length) return;
      State.lightboxIndex = index;
      const item = State.lightboxItems[index];
      DOM.lightboxImg.src = item.src;
      DOM.lightboxNo.textContent = item.no;
      DOM.lightboxTitle.textContent = item.title;
      DOM.lightbox.classList.add('is-open');
      if (State.lenis) State.lenis.stop();
    }

    function close() {
      DOM.lightbox.classList.remove('is-open');
      if (State.lenis) State.lenis.start();
    }

    function next() { open(State.lightboxIndex + 1); }
    function prev() { open(State.lightboxIndex - 1); }

    // Click handlers on plates
    document.addEventListener('click', e => {
      const plate = e.target.closest('[data-plate]');
      if (!plate) return;
      refreshItems();
      const idx = State.lightboxItems.findIndex(item => item.src === plate.dataset.plate);
      if (idx >= 0) open(idx);
    });

    DOM.lightboxClose.addEventListener('click', close);
    DOM.lightboxNext.addEventListener('click', next);
    DOM.lightboxPrev.addEventListener('click', prev);
    DOM.lightbox.addEventListener('click', e => { if (e.target === DOM.lightbox) close(); });
    document.addEventListener('keydown', e => {
      if (!DOM.lightbox.classList.contains('is-open')) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowRight') next();
      if (e.key === 'ArrowLeft') prev();
    });
  }

  // ============================================================
  // SPLITTYPE REVEALS
  // ============================================================
  function initSplitReveals(root) {
    U.qsa('[data-reveal="lines"]', root || document).forEach(el => {
      // an element inside a hidden page measures zero-width lines
      if (!el.offsetParent && el.offsetWidth === 0) return;
      // Only init if not already split
      if (el.dataset.split) return;
      el.dataset.split = 'true';

      const split = new SplitType(el, { types: 'lines,words,chars' });
      split.lines?.forEach(line => {
        const wrap = document.createElement('div');
        wrap.style.overflow = 'hidden';
        wrap.style.display = 'block';
        line.parentNode.insertBefore(wrap, line);
        wrap.appendChild(line);
      });

      gsap.fromTo(split.chars,
        { y: '120%', opacity: 0, rotateX: -40 },
        {
          y: '0%', opacity: 1, rotateX: 0, duration: 0.8, ease: CFG.easeOutExpo, stagger: 0.02,
          scrollTrigger: { trigger: el, start: 'top 85%', once: true }
        }
      );
    });
  }

  // ============================================================
  // SIMPLE REVEALS
  // ============================================================
  function initSimpleReveals() {
    const obs = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const el = entry.target;
          gsap.to(el, { y: 0, opacity: 1, duration: 0.8, ease: CFG.easeOutQuart, onComplete: () => obs.unobserve(el) });
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

    U.qsa('[data-reveal]:not([data-reveal="lines"]):not([data-reveal="plate"])').forEach(el => obs.observe(el));
  }

  // ============================================================
  // SCRAMBLE TEXT
  // ============================================================
  function initScramble() {
    U.qsa('[data-scramble]').forEach(el => {
      const original = el.textContent;
      let rafId = null;
      el.addEventListener('mouseenter', () => {
        let frame = 0;
        if (rafId) cancelAnimationFrame(rafId);
        function scramble() {
          frame++;
          const progress = frame / 12;
          let text = '';
          for (let i = 0; i < original.length; i++) {
            if (original[i] === ' ') { text += ' '; continue; }
            text += (i / original.length < progress) ? original[i] : U.randomChar();
          }
          el.textContent = text;
          if (progress < 1.2) rafId = requestAnimationFrame(scramble);
          else el.textContent = original;
        }
        scramble();
      });
      el.addEventListener('mouseleave', () => {
        if (rafId) cancelAnimationFrame(rafId);
        el.textContent = original;
      });
    });
  }

  // ============================================================
  // ABOUT COUNTERS
  // ============================================================
  function initCounters() {
    U.qsa('[data-count]').forEach(el => {
      const target = parseInt(el.dataset.count);
      const isYear = el.dataset.year !== undefined;
      ScrollTrigger.create({
        trigger: el, start: 'top 85%', once: true,
        onEnter: () => {
          gsap.to({ val: isYear ? target - 10 : 0 }, {
            val: target, duration: 2, ease: 'power2.out',
            onUpdate: function() {
              const v = Math.round(this.targets()[0].val);
              el.textContent = isYear ? v : v.toLocaleString();
            }
          });
        }
      });
    });
  }

  // ============================================================
  // NAV MOBILE TOGGLE
  // ============================================================
  function initNavToggle() {
    const toggle = document.getElementById('nav-toggle');
    if (!toggle) return;
    toggle.addEventListener('change', () => {
      document.body.style.overflow = toggle.checked ? 'hidden' : '';
    });
    U.qsa('.site-nav__link').forEach(link => {
      link.addEventListener('click', () => { toggle.checked = false; document.body.style.overflow = ''; });
    });
  }

  // ============================================================
  // INIT ALL
  // ============================================================
  const REDUCED = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function init() {
    if (REDUCED) {
      // show everything, wire up only what is needed to use the site
      document.documentElement.classList.add('is-ready');
      DOM.preloader.style.display = 'none';
      U.qsa('[data-reveal]').forEach(el => { el.style.opacity = 1; el.style.transform = 'none'; });
      U.qsa('.hero__pass').forEach((el, i, a) => { el.style.opacity = i === a.length - 1 ? 1 : 0; });
      U.qsa('.anno-item, .about__flow .prose, .hero__meta .anno')
        .forEach(el => { el.style.opacity = 1; el.style.transform = 'none'; });
      initLightbox();
      initNavToggle();
      initRouter();
      return;
    }
    initPreloader();
    initCursor();
    initLenis();
    initLightbox();
    initSimpleReveals();
    initScramble();
    initCounters();
    initNavToggle();
    // Router is initialized by preloader when done
  }

  // Start
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();

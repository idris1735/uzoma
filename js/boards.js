/* ============================================================
   boards.js — storyboard page.

   Each filmstrip translates sideways as the page scrolls down.
   The clip under each strip plays on request, one at a time.
   ============================================================ */

"use strict";

(() => {
  const { $, $$, MOTION } = window.UZ;

  /* ============================== FILMSTRIPS ============================== */
  const initStrips = () => {
    if (!MOTION) return;

    $$("[data-strip]").forEach((strip) => {
      const section = strip.closest(".film");
      const travel = () => Math.max(0, strip.scrollWidth - document.documentElement.clientWidth + 32);

      gsap.fromTo(strip,
        { x: 0 },
        {
          x: () => -travel(), ease: "none",
          scrollTrigger: {
            trigger: section, start: "top bottom", end: "bottom top",
            scrub: 0.9, invalidateOnRefresh: true,
          },
        });

      /* panels rise in once the section enters the viewport */
      gsap.from($$(".frame", strip), {
        yPercent: 14, opacity: 0, duration: 0.9, ease: "expo.out", stagger: 0.05,
        scrollTrigger: { trigger: section, start: "top 78%", once: true },
      });
    });
  };

  /* ============================== PLAYERS ============================== */
  const initPlayers = () => {
    const players = $$(".film__player");

    const stopAll = (except) => {
      players.forEach((p) => {
        if (p === except) return;
        const v = $("video", p);
        const label = $("[data-play-label]", p);
        if (v && !v.paused) v.pause();
        if (label) label.textContent = "PLAY THE ANIMATIC";
      });
    };

    players.forEach((player) => {
      const video = $("video", player);
      const btn = $("[data-play]", player);
      const label = $("[data-play-label]", player);
      if (!video || !btn) return;

      btn.addEventListener("click", () => {
        if (video.paused) {
          stopAll(player);
          const p = video.play();
          if (p && p.catch) p.catch(() => { label.textContent = "PLAY THE ANIMATIC"; });
          label.textContent = "PAUSE";
        } else {
          video.pause();
          label.textContent = "PLAY THE ANIMATIC";
        }
      });

      video.addEventListener("click", () => btn.click());

      /* stop playback once the player leaves the viewport */
      if (MOTION) {
        ScrollTrigger.create({
          trigger: player, start: "top bottom", end: "bottom top",
          onLeave: () => { video.pause(); label.textContent = "PLAY THE ANIMATIC"; },
          onLeaveBack: () => { video.pause(); label.textContent = "PLAY THE ANIMATIC"; },
        });
      }
    });
  };

  window.UZ.boot();
  initStrips();
  initPlayers();
})();

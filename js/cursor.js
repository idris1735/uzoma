/* ============================================================
   cursor.js — custom cursor.
   28px ring and crosshair, lerped at 0.12. Scales up over links,
   swaps to a nib over images, and leaves a short trail of marks
   when moving fast. Disabled on touch and under reduced motion.
   ============================================================ */

"use strict";

(() => {
  const fine = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (!fine || reduced) return;

  /* ---- DOM ---- */
  const cursor = document.createElement("div");
  cursor.className = "cursor";
  cursor.setAttribute("aria-hidden", "true");
  cursor.innerHTML = `
    <div class="cursor__ring">
      <svg viewBox="0 0 28 28">
        <circle cx="14" cy="14" r="12.25"/>
        <line x1="14" y1="0.5" x2="14" y2="27.5"/>
        <line x1="0.5" y1="14" x2="27.5" y2="14"/>
      </svg>
    </div>
    <div class="cursor__nib">
      <svg viewBox="0 0 24 24"><polygon points="0.5,0.5 23.5,0.5 23.5,23.5 0.5,23.5"/></svg>
    </div>
    <span class="cursor__label"></span>`;

  const trail = document.createElement("canvas");
  trail.className = "cursor__trail";
  document.body.append(cursor, trail);
  document.documentElement.classList.add("has-cursor");

  /* ---- trail canvas ---- */
  const ctx = trail.getContext("2d");
  let W = 0, H = 0;

  const sizeCanvas = () => {
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    W = window.innerWidth;
    H = window.innerHeight;
    trail.width = W * dpr;
    trail.height = H * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  };
  sizeCanvas();
  window.addEventListener("resize", sizeCanvas);

  const SHAPES = ["sq", "tri", "cir"];
  const marks = [];
  let shapeIdx = 0;

  const spawn = () => {
    marks.push({
      x: pos.x, y: pos.y,
      s: SHAPES[shapeIdx++ % 3],
      r: (Math.random() - 0.5) * Math.PI,
      size: 5 + Math.random() * 4,
      life: 1,
    });
    if (marks.length > 36) marks.shift();
  };

  const drawMarks = () => {
    ctx.clearRect(0, 0, W, H);
    ctx.strokeStyle = "#A3FF12";
    ctx.lineWidth = 1;
    for (let i = marks.length - 1; i >= 0; i--) {
      const m = marks[i];
      m.life -= 0.035;
      if (m.life <= 0) { marks.splice(i, 1); continue; }
      ctx.globalAlpha = m.life * 0.5;
      ctx.save();
      ctx.translate(m.x, m.y);
      ctx.rotate(m.r);
      ctx.beginPath();
      if (m.s === "sq") {
        ctx.rect(-m.size / 2, -m.size / 2, m.size, m.size);
      } else if (m.s === "tri") {
        ctx.moveTo(0, -m.size * 0.6);
        ctx.lineTo(m.size * 0.55, m.size * 0.5);
        ctx.lineTo(-m.size * 0.55, m.size * 0.5);
        ctx.closePath();
      } else {
        ctx.arc(0, 0, m.size / 2, 0, Math.PI * 2);
      }
      ctx.stroke();
      ctx.restore();
    }
    ctx.globalAlpha = 1;
  };

  /* ---- lerp loop (0.12) ---- */
  const pos = { x: innerWidth / 2, y: innerHeight / 2 };   // rendered
  const target = { x: innerWidth / 2, y: innerHeight / 2 }; // pointer
  const prev = { x: target.x, y: target.y };
  let seen = false;

  const frame = () => {
    pos.x += (target.x - pos.x) * 0.12;
    pos.y += (target.y - pos.y) * 0.12;
    cursor.style.transform = `translate3d(${pos.x}px, ${pos.y}px, 0)`;

    const speed = Math.hypot(target.x - prev.x, target.y - prev.y);
    prev.x = target.x;
    prev.y = target.y;
    if (speed > 5) spawn();   // only leave a trail when moving quickly

    drawMarks();
    requestAnimationFrame(frame);
  };

  window.addEventListener("pointermove", (e) => {
    if (!seen) {
      seen = true;
      cursor.style.opacity = 1;
      pos.x = target.x = prev.x = e.clientX;
      pos.y = target.y = prev.y = e.clientY;
    }
    target.x = e.clientX;
    target.y = e.clientY;
  }, { passive: true });

  /* ---- hover states ---- */
  const label = cursor.querySelector(".cursor__label");

  /* action word, by what the pointer is over */
  const LABELS = [
    [".plate__btn", "OPEN"],
    ["[data-scrub]", "DRAG"],
    [".board-tile, .film__video, [data-play]", "PLAY"],
  ];

  const labelFor = (t) => {
    if (!t.closest) return "";
    for (const [sel, word] of LABELS) if (t.closest(sel)) return word;
    return "";
  };

  window.addEventListener("pointerover", (e) => {
    const t = e.target;
    if (t.closest && t.closest(".work-card__media, .hero__pass, .award__trophy-img, .plate__btn, img")) {
      cursor.classList.add("is-image");
    }
    if (t.closest && t.closest("a, button, input, [data-cursor]")) {
      cursor.classList.add("is-link");
    }
    const word = labelFor(t);
    if (word) {
      label.textContent = word;
      cursor.classList.add("has-label");
    }
  }, true);

  window.addEventListener("pointerout", (e) => {
    const next = e.relatedTarget;
    if (!next || !next.closest || !next.closest("img, .work-card__media, .plate__btn")) {
      cursor.classList.remove("is-image");
    }
    if (!next || !next.closest || !next.closest("a, button, input, [data-cursor]")) {
      cursor.classList.remove("is-link");
    }
    if (!next || !labelFor(next)) cursor.classList.remove("has-label");
  }, true);

  window.addEventListener("pointerdown", () => cursor.classList.add("is-down"));
  window.addEventListener("pointerup", () => cursor.classList.remove("is-down"));
  window.addEventListener("blur", () => { cursor.style.opacity = 0; });
  window.addEventListener("focus", () => { if (seen) cursor.style.opacity = 1; });

  frame();
})();

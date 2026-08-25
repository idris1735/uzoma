# -*- coding: utf-8 -*-
"""
Dev tooling. Re-samples storyboard filmstrip frames, keeping the n brightest
(non-black) timestamps — the source MP4s contain fade-to-black sections.
Run once with:  python tools/fix_frames.py
"""
import os, subprocess, sys
import imageio_ffmpeg
from PIL import Image, ImageStat

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FF = imageio_ffmpeg.get_ffmpeg_exe()
TMP = os.path.join(ROOT, "_probe")
os.makedirs(TMP, exist_ok=True)

jobs = [
    ("Storyboards/Cash-trapped_Part1.mp4", "cash-trapped-a", 8, 259.5),
    ("Storyboards/Cash_Trapped_Part2.mp4", "cash-trapped-b", 7, 214.4),
]

for rel, stem, n, dur in jobs:
    src = os.path.join(ROOT, rel)
    scores = []
    for k in range(30):
        t = 0.5 + (dur - 1.0) * k / 29
        out = os.path.join(TMP, f"{stem}_{k:02d}.jpg")
        r = subprocess.run([FF, "-y", "-ss", f"{t:.2f}", "-i", src,
                            "-frames:v", "1", "-q:v", "4", out],
                           capture_output=True)
        if r.returncode == 0 and os.path.exists(out):
            try:
                st = ImageStat.Stat(Image.open(out).convert("RGB"))
                m = sum(st.mean)
                scores.append((m, t, out))
            except Exception:
                pass
    scores.sort(reverse=True)
    chosen = sorted([s for s in scores if s[0] > 100][:n], key=lambda s: s[1])
    print(f"{stem}: {len(scores)} probed, kept {len(chosen)}")
    for i, (m, t, out) in enumerate(chosen):
        dst = os.path.join(ROOT, "assets", "boards", f"{stem}-f{i+1:02d}.jpg")
        os.replace(out, dst)
        print(f"  f{i+1:02d} @ {t:6.1f}s  brightness {m:5.1f}")

for p in os.listdir(TMP):
    os.remove(os.path.join(TMP, p))
os.rmdir(TMP)
print("== DONE ==")

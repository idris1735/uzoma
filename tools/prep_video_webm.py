# -*- coding: utf-8 -*-
"""
Dev tooling. Encodes WebM (VP9) copies of the hover animatics so browsers
without H.264 (some Chromium builds, older environments) still play them.
The <video> tags list the MP4 first, then the WebM, so every browser
picks the first source it supports.
Run once with:  python tools/prep_video_webm.py
"""
import os, subprocess, sys
import imageio_ffmpeg

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIDEO = os.path.join(ROOT, "assets", "video")
FF = imageio_ffmpeg.get_ffmpeg_exe()

for stem in ["coma-toes", "cash-trapped-a", "cash-trapped-b"]:
    src = os.path.join(VIDEO, f"{stem}.mp4")
    out = os.path.join(VIDEO, f"{stem}.webm")
    if not os.path.exists(src):
        print("MISSING", src); sys.exit(1)
    r = subprocess.run(
        [FF, "-y", "-i", src,
         "-c:v", "libvpx-vp9", "-crf", "36", "-b:v", "0",
         "-deadline", "good", "-cpu-used", "2",
         "-pix_fmt", "yuv420p", "-an", out],
        capture_output=True, text=True)
    if r.returncode != 0:
        print("ERR", r.stderr[-500:]); sys.exit(1)
    print(f"encoded {stem}.webm  ({os.path.getsize(out)} bytes)")

print("== DONE ==")

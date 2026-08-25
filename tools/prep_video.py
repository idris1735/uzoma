# -*- coding: utf-8 -*-
"""
Dev tooling. Extracts filmstrip frames from the storyboard MP4s and re-encodes
lightweight hover-animatic copies into /assets/boards and /assets/video.
Run once with:  python tools/prep_video.py
"""
import os, subprocess, sys
import imageio_ffmpeg

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC  = os.path.join(ROOT, "Storyboards")
FRAMES = os.path.join(ROOT, "assets", "boards")
VIDEO  = os.path.join(ROOT, "assets", "video")
FF = imageio_ffmpeg.get_ffmpeg_exe()

os.makedirs(FRAMES, exist_ok=True)
os.makedirs(VIDEO, exist_ok=True)

def run(args):
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode != 0:
        print("ERR", r.stderr[-600:]); sys.exit(1)

def probe_dur(src):
    r = subprocess.run([FF, "-i", src], capture_output=True, text=True)
    for line in r.stderr.splitlines():
        if "Duration" in line:
            h, m, s = line.split("Duration:")[1].split(",")[0].strip().split(":")
            return int(h)*3600 + int(m)*60 + float(s)
    return 0

jobs = [
    ("Coma_Toes_IG.mp4",        "coma-toes",       8),
    ("Cash-trapped_Part1.mp4",  "cash-trapped-a",  8),
    ("Cash_Trapped_Part2.mp4",  "cash-trapped-b",  7),
]

for src, stem, n in jobs:
    path = os.path.join(SRC, src)
    dur = probe_dur(path)
    print(f"== {stem}  {dur:.1f}s  {n} frames")
    # frames at evenly spaced timestamps
    for k in range(n):
        t = 1.0 + (dur - 3.0) * k / (n - 1)
        out = os.path.join(FRAMES, f"{stem}-f{k+1:02d}.jpg")
        run([FF, "-y", "-ss", f"{t:.2f}", "-i", path,
             "-vf", "scale=1280:-2", "-frames:v", "1", "-q:v", "3", out])
        print("   ", os.path.basename(out))
    # light hover-animatic: a short representative clip (720p, low bitrate, no audio)
    clip_start = dur * 0.40  # past intros, into the meat of the board
    out = os.path.join(VIDEO, f"{stem}.mp4")
    run([FF, "-y", "-ss", f"{clip_start:.2f}", "-t", "8", "-i", path,
         "-vf", "scale=-2:720", "-c:v", "libx264", "-preset", "fast", "-crf", "30",
         "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-an", out])
    print("   encoded", os.path.basename(out))

print("== DONE ==")

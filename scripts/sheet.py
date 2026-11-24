#!/usr/bin/env python3
# Ported from the box's motion/reels/sheet.py. Contact sheet of stills from a rendered reel, for QA and review messages.
# Usage: sheet.py REEL T1,T2,... OUT.png [--video project/final.mp4]
# REEL is a reel build folder; relative names are looked up in $Q9_REELS_DIR (default: current directory).
# Each still is 216x384 (a 9:16 thumbnail); stills sit side by side with a 10 px white gutter.
import subprocess, sys, os, argparse, tempfile
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("reel"); ap.add_argument("times"); ap.add_argument("out")
ap.add_argument("--video", default="project/final.mp4", help="path inside REEL (default project/final.mp4)")
a = ap.parse_args()
R = a.reel if os.path.isdir(a.reel) else os.path.join(os.environ.get("Q9_REELS_DIR", "."), a.reel)
ts = [float(x) for x in a.times.split(',')]
tmp = tempfile.mkdtemp(prefix="sheet_")
ims = []
for t in ts:
    p = os.path.join(tmp, f'_s_{t}.png'); subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(t), '-i', os.path.join(R, a.video), '-frames:v', '1', p], check=True); ims.append(Image.open(p).resize((216, 384)))
sh = Image.new('RGB', (226 * len(ims), 384), 'white')
for i, im in enumerate(ims): sh.paste(im, (i * 226, 0))
sh.save(a.out)

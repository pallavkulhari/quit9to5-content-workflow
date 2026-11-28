#!/usr/bin/env python3
# Ported from the box's motion/reels/process_vo.py. Same algorithm; the per-reel script texts and paths are now inputs.
# take1.mp3 -> vo.wav (pauses >min_sil trimmed to keep_sil (default 0.45s/0.34s; per-reel via --trim), loudnorm -15 LUFS) -> faster-whisper word times
#   -> aligned to the exact script words -> audio/timing.json + project/assets/captions.json   (local, $0)
#
# Usage:
#   process_vo.py REEL [REEL ...] [--script-file FILE] [--model small.en]
# REEL is a reel build folder (e.g. 005_toxic_hike_L2). Relative names are looked up in $Q9_REELS_DIR
# (default: current directory). Each reel needs:
#   REEL/audio/take1.mp3            the ElevenLabs take
#   REEL/audio/script.txt           the exact approved voiceover as one paragraph (or pass --script-file)
#   REEL/project/assets/            created if missing; captions.json is written here
# Env: Q9_REELS_DIR, WHISPER_MODEL (default small.en).
import subprocess, re, json, sys, os, difflib, argparse
import numpy as np
from faster_whisper import WhisperModel

ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument("reels", nargs="+")
ap.add_argument("--script-file", help="voiceover text file (default REEL/audio/script.txt); only valid with one REEL")
ap.add_argument("--model", default=os.environ.get("WHISPER_MODEL", "small.en"))
ap.add_argument('--trim', nargs=2, type=float, metavar=('MIN_SIL','KEEP_SIL'), default=(0.45,0.34), help='min pause to trim and pause kept (e.g. 0.9 0.55 for a gentle trim)')
args = ap.parse_args()
min_sil, keep_sil = args.trim
half = keep_sil / 2.0

def strip_caption_quotes(tok):
    # Drop typographic/straight double quotes from caption-pill tokens; keep apostrophes.
    return tok.translate({ord(c): None for c in '"“”«»'})


if args.script_file and len(args.reels) > 1:
    sys.exit("--script-file works with a single REEL")
REELS_DIR = os.environ.get("Q9_REELS_DIR", ".")


def reel_path(r):
    return r if os.path.isdir(r) else os.path.join(REELS_DIR, r)


m = WhisperModel(args.model, device='cpu', compute_type='int8')
def norm(w): return re.sub(r"[^a-z0-9]", "", w.lower())
for name in args.reels:
    R = reel_path(name)
    A = f"{R}/audio"; src = f"{A}/take1.mp3"; out = f"{A}/vo.wav"
    script_file = args.script_file or f"{A}/script.txt"
    if not os.path.exists(src): sys.exit(f"missing {src}")
    if not os.path.exists(script_file): sys.exit(f"missing {script_file} (the exact approved voiceover, one paragraph)")
    SCRIPT = " ".join(open(script_file, encoding="utf-8").read().split())
    os.makedirs(f"{R}/project/assets", exist_ok=True)
    o = subprocess.run(['ffmpeg', '-nostdin', '-i', src, '-af', 'silencedetect=n=-38dB:d=0.12', '-f', 'null', '-'], capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', o)]; en = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', o)]
    dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', src], capture_output=True, text=True).stdout)
    S = list(zip(st, en)); keep = []; cur = 0.0
    if S and S[0][0] < 0.05: cur = max(0, S[0][1] - 0.10)
    for a, b in S:
        if a < 0.05 or b >= dur - 0.01: continue
        if b - a > min_sil: keep.append((cur, a + half)); cur = b - half
    end = min(dur, S[-1][0] + 0.3) if S and S[-1][1] >= dur - 0.01 else dur
    keep.append((cur, end))
    f = ''.join(f'[0:a]atrim={a:.4f}:{b:.4f},asetpts=PTS-STARTPTS[s{i}];' for i, (a, b) in enumerate(keep))
    f += ''.join(f'[s{i}]' for i in range(len(keep))) + f'concat=n={len(keep)}:v=0:a=1,aresample=48000,loudnorm=I=-15:TP=-1.5:LRA=11[o]'
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', src, '-filter_complex', f, '-map', '[o]', '-ar', '48000', '-ac', '2', out], check=True)
    pcm = np.frombuffer(subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-i', out, '-f', 'f32le', '-ac', '1', '-ar', '16000', '-'], capture_output=True).stdout, np.float32)
    segs, _ = m.transcribe(pcm, language='en', word_timestamps=True, beam_size=5)
    W = [{'w': w.word.strip(), 's': round(w.start, 3), 'e': round(w.end, 3)} for s in segs for w in s.words]
    vd = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', out], capture_output=True, text=True).stdout)
    # align: spoken-form tokens for script words
    disp = SCRIPT.split()
    spoken = {'9to5': ['nine', 'to', 'five'], '9to5,': ['nine', 'to', 'five'], '9to5.': ['nine', 'to', 'five'], '9to5?': ['nine', 'to', 'five'], 'quit9to5.in.': ['quit', 'nine', 'to', 'five', 'dot', 'in']}
    sp = []; own = []
    for i, d in enumerate(disp):
        for t in spoken.get(d, [norm(d)]): sp.append(t); own.append(i)
    hw = []; hown = []
    for j, w in enumerate(W):
        n = norm(w['w']); parts = {'9to5': ['nine', 'to', 'five'], '925': ['nine', 'to', 'five'], 'ninetofive': ['nine', 'to', 'five']}.get(n, [n])
        for p in parts: hw.append(p); hown.append(j)
    sm = difflib.SequenceMatcher(a=sp, b=hw, autojunk=False)
    T = [None] * len(disp)
    for a, b, k in sm.get_matching_blocks():
        for x in range(k):
            i = own[a + x]; j = hown[b + x]
            if T[i] is None: T[i] = [W[j]['s'], W[j]['e']]
            else: T[i][1] = max(T[i][1], W[j]['e'])
    # interpolate gaps
    for i in range(len(T)):
        if T[i] is None:
            p = next((T[k][1] for k in range(i - 1, -1, -1) if T[k]), 0.0); q = next((T[k][0] for k in range(i + 1, len(T)) if T[k]), vd)
            T[i] = [p + 0.02, min(q, p + 0.3)]
    miss = sum(1 for i in range(len(T)) if not any(own[a + x] == i for a, b, k in sm.get_matching_blocks() for x in range(k)))
    words = [{'t': strip_caption_quotes(d), 's': round(T[i][0], 3), 'e': round(T[i][1], 3)} for i, d in enumerate(disp)]
    C = []; cur = []
    for w in words:
        if cur and (len(cur) == 4 or len(' '.join(x['t'] for x in cur + [w])) > 24): C.append(cur); cur = []
        cur.append(w)
        if re.search(r"[.,?!]$", w['t']): C.append(cur); cur = []
    if cur: C.append(cur)
    chunks = [{'s': c[0]['s'], 'e': c[-1]['e'], 'words': c} for c in C]
    json.dump({'duration': vd, 'whisper': W, 'words': words, 'chunks': chunks}, open(f"{A}/timing.json", 'w'), ensure_ascii=False, indent=0)
    json.dump(chunks, open(f"{R}/project/assets/captions.json", 'w'), ensure_ascii=False)
    print(name, 'dur', round(vd, 2), 'whisper', len(W), 'script', len(disp), 'unmatched', miss)
    print(' '.join(w['w'] for w in W))
    for c in chunks: print(f"  {c['s']:6.2f}-{c['e']:6.2f} " + ' '.join(w['t'] for w in c['words']))

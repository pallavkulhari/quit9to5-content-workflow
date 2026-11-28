#!/usr/bin/env python3
# Ported from the box's motion/reels/splice_cta.py. Same algorithm; reels, cut points and the CTA take are now inputs.
# Replaces the end of an existing voiceover with a pre-recorded shared CTA take (used when the CTA wording changed
# after a reel was voiced, as with reels 001 and 002 on 20 Nov 2026). Rewrites timing.json and captions.json.
#
# Usage:
#   splice_cta.py REEL=CUT_SECONDS [REEL=CUT_SECONDS ...] [--cta-wav PATH] [--gap 0.30] [--model small.en]
# e.g. splice_cta.py 001_quit_faster_L2=30.22 002_tell_family_L2=28.80
# CUT_SECONDS is the time in REEL/audio/vo.wav where the old CTA starts (read it from REEL/audio/timing.json).
# REEL needs audio/vo.wav and audio/timing.json from process_vo.py. Writes audio/vo_final.wav.
# Env: Q9_REELS_DIR (default: current directory), CTA_WAV (default $Q9_REELS_DIR/shared_cta/cta.wav),
#      CTA_TEXT (default the mandatory reel CTA), WHISPER_MODEL (default small.en).
import subprocess, json, re, os, sys, argparse
import numpy as np
from faster_whisper import WhisperModel

REELS_DIR = os.environ.get("Q9_REELS_DIR", ".")
ap = argparse.ArgumentParser()
ap.add_argument("cuts", nargs="+", help="REEL=CUT_SECONDS")
ap.add_argument("--cta-wav", default=os.environ.get("CTA_WAV", os.path.join(REELS_DIR, "shared_cta", "cta.wav")))
ap.add_argument("--gap", type=float, default=0.30)
ap.add_argument("--model", default=os.environ.get("WHISPER_MODEL", "small.en"))
args = ap.parse_args()
CUT = {}
for c in args.cuts:
    r, _, t = c.partition("=")
    if not t: sys.exit(f"bad argument {c!r}; use REEL=CUT_SECONDS")
    CUT[r] = float(t)
CTA = os.environ.get("CTA_TEXT", "My book Quit 9to5 is coming out soon. Join the waitlist in bio.").split()
if not os.path.exists(args.cta_wav): sys.exit(f"missing CTA take {args.cta_wav}")


def reel_path(r):
    return r if os.path.isdir(r) else os.path.join(REELS_DIR, r)


m = WhisperModel(args.model, device='cpu', compute_type='int8')
def dur(f): return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f], capture_output=True, text=True).stdout)
pcm = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', args.cta_wav, '-f', 'f32le', '-ac', '1', '-ar', '16000', '-'], capture_output=True).stdout, np.float32)
segs, _ = m.transcribe(pcm, language='en', word_timestamps=True, beam_size=5)
CW = [{'w': w.word.strip(), 's': w.start, 'e': w.end} for s in segs for w in s.words]
print('CTA whisper:', [c['w'] for c in CW])
for name, cut in CUT.items():
    R = reel_path(name)
    A = f'{R}/audio'; GAP = args.gap
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{A}/vo.wav', '-i', args.cta_wav, '-filter_complex',
      f'[0:a]atrim=0:{cut},afade=t=out:st={cut-0.04}:d=0.04,asetpts=PTS-STARTPTS[a];anullsrc=r=48000:cl=stereo,atrim=0:{GAP}[g];[1:a]asetpts=PTS-STARTPTS[b];[a][g][b]concat=n=3:v=0:a=1[o]',
      '-map', '[o]', '-ar', '48000', '-ac', '2', f'{A}/vo_final.wav'], check=True)
    off = cut + GAP
    T = json.load(open(f'{A}/timing.json'))
    words = [w for w in T['words'] if w['s'] < cut - 0.05]
    # map CTA words: whisper tokens to script by order (handle 9 to 5 splitting)
    toks = []
    for c in CW:
        n = re.sub(r'[^a-z0-9]', '', c['w'].lower()); toks.append((n, c['s'], c['e']))
    seq = []; i = 0
    for d in CTA:
        dn = re.sub(r'[^a-z0-9]', '', d.lower())
        if dn == '9to5':
            js = [k for k in range(i, min(i + 4, len(toks)))]
            acc = ''; s = None
            for k in js:
                acc += toks[k][0]; s = s if s is not None else toks[k][1]
                if acc in ('9to5', '925', 'ninetofive', '95'): seq.append({'t': d, 's': round(s + off, 3), 'e': round(toks[k][2] + off, 3)}); i = k + 1; break
            else: seq.append({'t': d, 's': round(toks[i][1] + off, 3), 'e': round(toks[i][2] + off, 3)}); i += 1
        else:
            seq.append({'t': d, 's': round(toks[i][1] + off, 3), 'e': round(toks[i][2] + off, 3)}); i += 1
    words += seq
    chunks = [c for c in T['chunks'] if c['words'][0]['s'] < cut - 0.05]
    # the CTA is chunked 4/4/3/rest, as on the box ("My book Quit 9to5" / "is coming out soon." / "Join the waitlist" / "in bio.")
    chunks += [{'s': seq[0]['s'], 'e': seq[3]['e'], 'words': seq[0:4]}, {'s': seq[4]['s'], 'e': seq[7]['e'], 'words': seq[4:8]},
               {'s': seq[8]['s'], 'e': seq[10]['e'], 'words': seq[8:11]}, {'s': seq[11]['s'], 'e': seq[-1]['e'], 'words': seq[11:]}]
    d = dur(f'{A}/vo_final.wav')
    T.update({'duration_final': d, 'cta_cut': cut, 'cta_offset': off, 'words_final': words, 'chunks_final': chunks})
    json.dump(T, open(f'{A}/timing.json', 'w'), ensure_ascii=False, indent=0)
    json.dump(chunks, open(f'{R}/project/assets/captions.json', 'w'), ensure_ascii=False)
    print(name, 'final', round(d, 2)); [print(f"  {c['s']:6.2f}-{c['e']:6.2f} " + ' '.join(w['t'] for w in c['words'])) for c in chunks[-6:]]

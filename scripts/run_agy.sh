#!/usr/bin/env bash
# Ported from the box's motion/reels/run_agy.sh. Runs the P1 builder (Antigravity `agy` CLI with Gemini 4 Neon)
# on one or more L2 reel folders in parallel. Each folder must already contain BRIEF.md, ref_L2/ and project/
# (with assets/vo.wav, assets/captions.json, captions4.js, gsap.min.js, fonts, book_cover.jpeg).
# Output: REEL/project/final.mp4, REEL/project/qa/*.png, REEL/NOTES.md, log in REEL/agy.log.
#
# Usage: scripts/run_agy.sh 006_hike_L2 [007_other_L2 ...]
# Env:
#   Q9_REELS_DIR   folder holding the reel folders and COMMON_REEL_BRIEF.md (required)
#   AGY_BIN        agy executable (default: agy on PATH)
#   M / AGY_MODEL  model (default gemini-4-neon-high)
#   NODE_BIN       optional dir prepended to PATH so npx/hyperframes resolve (Node 22)
#   AGY_EXTRA_DIRS optional space-separated extra read dirs (the box used the blog folder, for facts.md)
# No secrets are used here; agy reads its own login.
set -euo pipefail
: "${Q9_REELS_DIR:?set Q9_REELS_DIR to the folder holding the reel folders}"
cd "$Q9_REELS_DIR"
[ -n "${NODE_BIN:-}" ] && export PATH="$NODE_BIN:$PATH"
AGY="${AGY_BIN:-agy}"
M="${M:-${AGY_MODEL:-gemini-4-neon-high}}"
EXTRA=()
for d in ${AGY_EXTRA_DIRS:-}; do EXTRA+=(--add-dir "$d"); done
[ "$#" -gt 0 ] || { echo "usage: $0 REEL [REEL ...]" >&2; exit 2; }
for R in "$@"; do
 ( set +e; cd "$R" || exit 1; "$AGY" -p "Read BRIEF.md and ../COMMON_REEL_BRIEF.md, study the references in ./ref_L2 (look at the PNGs), then build the Hyperframes project in ./project exactly as specified: write index.html, run lint, check, render, mux the voiceover into project/final.mp4, extract QA stills, look at them and iterate until polished, then write NOTES.md. Work autonomously; do not ask questions." --model "$M" --dangerously-skip-permissions --add-dir "$Q9_REELS_DIR/$R" --add-dir "$Q9_REELS_DIR/$R/ref_L2" ${EXTRA[@]+"${EXTRA[@]}"} --print-timeout 0 > agy.log 2>&1; echo "exit $?" >> agy.log ) &
done
wait

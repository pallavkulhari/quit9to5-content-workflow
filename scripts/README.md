# scripts/

Ported from the box with hard-coded paths replaced by environment variables or CLI arguments (see `.env.example`). The algorithms are unchanged unless noted. `UPSTREAM.tsv` records which box file each one came from, so the Saturday sync can report when the box version changes.

## Reels

| File | What it does | Inputs |
|---|---|---|
| `process_vo.py` | ElevenLabs take → `audio/vo.wav` (pauses > 0.45 s trimmed to 0.34 s, −15 LUFS), faster-whisper word times aligned to the exact script, `audio/timing.json` and `project/assets/captions.json` | `REEL` folder(s); `REEL/audio/take1.mp3`; `REEL/audio/script.txt` or `--script-file`; `Q9_REELS_DIR`, `WHISPER_MODEL`. (The box version had the scripts hard-coded in a dict; now they are read from file.) |
| `splice_cta.py` | Replaces the end of an existing voiceover with the shared CTA take and re-times captions | `REEL=CUT_SECONDS` pairs; `--cta-wav` / `CTA_WAV`; `CTA_TEXT`. (The box version had the cut points hard-coded.) |
| `sheet.py` | Contact sheet of stills (216×384 each) from `REEL/project/final.mp4` | `REEL`, comma-separated times, output PNG; `--video` |
| `run_agy.sh` | Runs the P1 builder (`agy`, `gemini-4-neon-high`) on L2 reel folders in parallel, with the same instruction as on the box | `Q9_REELS_DIR` (required), `AGY_BIN`, `AGY_MODEL`/`M`, `NODE_BIN`, `AGY_EXTRA_DIRS` |
| `l2_reference/005_toxic_hike/` | The builder's `tools/art.py` (SVG drawing helpers) and `tools/build.py` (writes `index.html`) from reel 005, plus `assets/captions4.js` (the caption pill) and `hyperframes.json`. Reference for `tools_ref/` in new builds. Paths are relative to the project folder. | see the folder's README |

## Cards, memes, covers

| File | What it does | Env |
|---|---|---|
| `cards/var.py` | v1a quote card: `make1(text, "L", out)` → 1024 px square | `Q9_FONT_INTER`, `Q9_CARD_ASSETS` |
| `cards/make_insta.py` | 9:16 story version: `make_insta(text, out)`; CLI `python3 make_insta.py "text" out.png` | same |
| `cards/fmt12.py` | Structured card helpers (title, checklist, numbers, myth/reality, steps) on the v1a template | same |
| `memes/meme_lib.py` | `meme(template, top, bottom, boxes)` → 1080×1350 with a "quit9to5.in" corner mark | `MEME_TEMPLATES`, `Q9_FONT_INTER` |
| `crosspost/make_x_cover.py` | X Article cover at 5:2 (3000×1200) with safe zone, preview and debug images. Written for post 8; copy and edit per post. | `BLOG_THUMB_BG`, `X_COVER_OUT_DIR`, fonts |

## Blog

| File | What it does |
|---|---|
| `blog/autochecks.py` | Pre-publish mechanical checks: `python3 autochecks.py postNN.md ["So, how do you …"]` |
| `blog/build_html.py` | Paste-ready beehiiv HTML: `python3 build_html.py postNN.md postNN_publish.html` |
| `blog/live_qa.py` | Post-publish QA with screenshots: `python3 live_qa.py <url> [source.md]` (`BLOG_QA_DIR`) |
| `blog/make_thumb.py` | Thumbnail pattern (1200×630): copy per post; `python3 make_thumb.py out.jpg` (`BLOG_THUMB_BG`) |

## Sync and safety

| File | What it does |
|---|---|
| `sync_from_box.sh` | Weekly Saturday refresh (see `SYNC.md`). Has box-path defaults because it runs on the box. |
| `lib/sanitise.py` | Path, ID, email, phone and manuscript-reference scrubbing used by the sync |
| `lib/secret_scan.py` | Repo scan; exits 1 on any unallowlisted hit |
| `secret-scan-allowlist.txt` | Reviewed false positives (`<glob><TAB><regex>`) |
| `UPSTREAM.tsv` | Source path and sha256 of each ported script |

None of these scripts read or contain secrets. ElevenLabs, Buffer and Drive calls are made through connectors or APIs by the agent, not by these scripts.

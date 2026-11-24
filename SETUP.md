# Setup

What you need to run the workflow off the box, and which environment variables each tool needs. All variables are listed, with placeholders, in [.env.example](.env.example). Copy it to `.env` (never commit `.env`) and fill in what Pallav shares.

```bash
cp .env.example .env      # fill in values
set -a; . ./.env; set +a  # load into your shell
```

## Accounts and access Pallav must share

| Service | What you need | Env vars | Used for |
|---|---|---|---|
| ElevenLabs | API key or the ElevenLabs MCP connector; access to his cloned voice | `ELEVENLABS_API_KEY`, `ELEVENLABS_VOICE_ID`, `ELEVENLABS_MODEL_ID` (eleven_v4), `ELEVENLABS_LANGUAGE` (hi), `ELEVENLABS_SIMILARITY` (0.9), `ELEVENLABS_STABILITY` (0.5) | Reel voiceovers. The only paid service allowed without asking; log each call in `PAID_CALL_LEDGER`. |
| Buffer | Buffer MCP connector (or an API token) for the "Quit 9to5" organisation | `BUFFER_ACCESS_TOKEN`, `BUFFER_ORG_ID`, `BUFFER_CHANNEL_INSTAGRAM`, `BUFFER_CHANNEL_LINKEDIN`, `BUFFER_CHANNEL_THREADS`, `POST_TIMEZONE`, `SLOT_TIMES` | Scheduling Instagram, LinkedIn Page, Threads. Free plan: 10 scheduled posts per channel. |
| Google Drive | Drive connector or OAuth access to the "Motion reels" folder | `GDRIVE_MOTION_REELS_FOLDER_ID`, optional `GDRIVE_BLOG_DOCS_FOLDER_ID`, `POST_LOG_SHEET_ID` | Public video URLs for Buffer; blog paste Docs; post-log Sheet. The folder must be "Anyone with the link: Viewer" (set in the Drive web UI). |
| beehiiv | A browser session on the blog's editor (login may need a device code from Pallav's email; ask him) | optional `BEEHIIV_API_KEY`, `BEEHIIV_PUBLICATION_ID` for read-back checks | Publishing blog posts (browser only on the free plan). |
| Substack | A browser session for pallavkulhari.substack.com | `SUBSTACK_URL` | Cross-posted posts (approval needed) and text-only Notes. |
| X | Pallav signs in himself (Google SSO) | none | X Article drafts only. Not a Buffer channel. |
| Image host | An account with a public image host (the box uses iili.io) | `IMAGE_HOST_API_KEY` | Public image URLs for card and carousel posts in Buffer. |
| Review bot | How to reach RRRI, "The Viewer" | `REVIEW_BOT_ID`, `REVIEW_BOT_CONTACT` | Sending live links after anything goes live. |
| Pallav | A chat channel for review messages | `PALLAV_REVIEW_CHANNEL` | Previews, captions (one per message), questions. |

Never put real values in any committed file. If you need an ID in a doc, write a placeholder like `<BUFFER_CHANNEL_ID_INSTAGRAM>`.

## Local tools

| Tool | Version / notes | Env vars | Used by |
|---|---|---|---|
| Python 3.10+ | `pip install faster-whisper numpy pillow beautifulsoup4 markdown` (`opencv-python` only for the carousel book render on the box) | `WHISPER_MODEL` (small.en) | `scripts/process_vo.py`, `splice_cta.py`, `sheet.py`, card/blog/meme/cover scripts |
| ffmpeg + ffprobe | any recent build | | voiceover processing, mux, QA stills, faststart remux |
| Node.js 22 | for `npx hyperframes` | `NODE_BIN` (dir prepended to PATH, optional) | Hyperframes |
| Hyperframes | **0.9.72**, via `npx --yes hyperframes@0.9.72 …` | `HYPERFRAMES_VERSION` | lint, check, render |
| GSAP | `gsap.min.js` from the `gsap` npm package, copied into each reel's `project/assets/` (not shipped in this repo) | | the L2 timeline |
| Antigravity `agy` CLI | logged in; model `gemini-4-neon-high` | `AGY_BIN`, `AGY_MODEL`, `AGY_EXTRA_DIRS`, `Q9_REELS_DIR` | P1 builder, `scripts/run_agy.sh` |
| Claude Code | with the Hyperframes skills if available | | P2 builder; any pipeline step |
| Gemini CLI | optional | | script drafting with `prompts/script-reel-gemini.md` |
| Google Chrome (headless) | | | screenshots in `scripts/blog/live_qa.py` |
| curl, sha256sum | | | verifying public Drive downloads before scheduling |

## Fonts and brand assets (not in this repo)

Ask Pallav for these; they are binary and stay out of git:
- Fonts: Inter Tight, Inter, Caveat (reels); Inter variable (cards, memes); Josefin Sans variable (blog thumbnails, X covers). Env: `Q9_FONT_INTER`, `Q9_FONT_JOSEFIN`, `Q9_FONT_DEJAVU_BOLD`.
- `book_cover.jpeg` (reel end card, cards), `pallav_photo.jpg` (card avatar). Env: `Q9_CARD_ASSETS`.
- `t4_seven.jpg`, the notebook-grid background for blog thumbs and X covers. Env: `BLOG_THUMB_BG`.
- The L2 reference frames (`ref_L2/F1..F8.png`) and the shared CTA take (`shared_cta/cta.wav`, env `CTA_WAV`).
- Meme templates (env `MEME_TEMPLATES`).

## Working folders

Set `Q9_ROOT` to your working content folder and `Q9_REELS_DIR` to its `motion/reels`. The folder convention for reels is in [docs/reels.md](docs/reels.md). Keep media in these working folders or in Drive, never in this repo (`.gitignore` blocks media).

## Paths in ported scripts

Every script in `scripts/` takes its paths from environment variables or CLI arguments; there are no hard-coded box paths. See [scripts/README.md](scripts/README.md). The only script with box defaults is `scripts/sync_from_box.sh`, which is meant to run on the box.

## Check your setup

```bash
python3 -c "import faster_whisper, numpy, PIL; print('python ok')"
ffmpeg -version | head -1
npx --yes hyperframes@0.9.72 doctor
python3 scripts/lib/secret_scan.py .     # must PASS before you share or commit anything
```

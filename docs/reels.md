# Reels: idea → script → voice → L2 build → QA → Drive → Buffer

The daily Instagram motion reel is the main format. Each reel is a voiceover in Pallav's cloned voice over light-theme kinetic type ("L2" style), built as a Hyperframes HTML composition and rendered to a 1080×1920 mp4. The same file also goes to LinkedIn and Threads.

Canonical references: reels **004 runway** and **005 toxic hike** ([examples/](../examples/)). Earlier reels (001–003) used the older clipped style and the old CTA; use them only for build mechanics.

Read first: [rules/approval-gates.md](../rules/approval-gates.md), [rules/content-rules.md](../rules/content-rules.md), [rules/voice-and-style.md](../rules/voice-and-style.md).

## 0. Folder convention

Under `$Q9_REELS_DIR`:

```
NNN_slug/                 script work: SCRIPT.md (draft + beat table), SCRIPT_APPROVED.md or SCRIPT_vN_voiceover.md,
                          CAPTION*.txt, THREADS.txt
NNN_slug_L2/              the build
  BRIEF.md                beat-by-beat brief for the builder (times from captions.json)
  NOTES.md                builder's notes + parent QA/delivery log
  CAPTION.txt THREADS.txt (when the caption is reworked at build time)
  audio/                  take1.mp3, vo.wav, timing.json, script.txt
  ref_L2/                 approved L2 reference frames, BRIEF/COMMON_BRIEF, frames_index.html
  project/                Hyperframes project: index.html, hyperframes.json, package.json, meta.json,
                          assets/ (vo.wav, captions.json, captions4.js, gsap.min.js, fonts, book_cover.jpeg),
                          tools/ (art.py, build.py), tools_ref/ (helpers from the latest approved build), qa/
NNN_slug_L2.mp4           posting copy (faststart)
shared_cta/cta.wav        shared CTA take, for splice_cta.py
COMMON_REEL_BRIEF.md      L2 rules (copy: playbooks/COMMON_REEL_BRIEF.md)
```

## 1. Idea (Pallav picks)

- Ideas live in [playbooks/APPROVED_IDEAS.md](../playbooks/APPROVED_IDEAS.md) with Pallav's note for each. Honour the note (e.g. A2 runway: "connect it with startups and explain it properly"; A4: "give the reader full context").
- Only work on ideas he has approved. New idea? Propose it with its source (book chapter, blog post, facts.md row) and wait.
- One idea per reel. If it needs "and also", it is two reels.

## 2. Script draft (Claude or Gemini, 004/005 style)

Use [prompts/script-reel-claude.md](../prompts/script-reel-claude.md) or [prompts/script-reel-gemini.md](../prompts/script-reel-gemini.md). The method is [skills/instagram-reel-script/SKILL.md](../skills/instagram-reel-script/SKILL.md), and the rulebook is [playbooks/SCRIPT_PLAYBOOK.md](../playbooks/SCRIPT_PLAYBOOK.md); where they disagree, the playbook wins.

What a good script does (from the 21–22 Nov rules):
- **Hook from the idea itself.** A quit opener only if the topic leads there.
- **Explains out loud** in coherent full sentences ("Let me tell you about…"), defining each concept before applying it.
- **One chain of thought**: each line answers the question the previous one raised. Write the chain check.
- **One open loop**, set in the first few seconds and paid off after about 70% of the runtime.
- **At most two spoken numbers**; other figures on screen; maths rechecked; examples labelled.
- **A send-worthy line** someone would forward.
- **One first-person proof line** where the book supports it, never invented.
- **Payoff, then the mandatory CTA**: "My book Quit 9to5 is coming out soon. Join the waitlist in bio."
- Length: the explaining voice needs room. 004 is 135 spoken words, a 44.7 s take padded to 46 s; 005 is 143 words, a 55.8 s take padded to 58 s. Cut repetition, never definitions.

Deliverable in `NNN_slug/SCRIPT.md`: the one-sentence idea and sources; a beat table (time, voiceover, on-screen text, L2 object and motion, retention job); the clean voiceover block; the chain check; why it retains; 1–2 alternative hooks; the Instagram/LinkedIn caption and the Threads text ([docs/captions.md](captions.md)). Status line at the top: "script draft, nothing built, voiced or scheduled".

## 3. Pallav approves the script

- Send the clean voiceover (and the beat idea) for review. Expect rewrites: 004 went through two versions, 005 through three before "Can be built".
- On approval, save the exact approved text as `SCRIPT_APPROVED.md` (or `SCRIPT_vN_voiceover.md`) with the date and his words.
- Nothing is voiced or built from an unapproved draft.

## 4. Voice (ElevenLabs clone)

Settings used for 004 and 005:

| Setting | Value |
|---|---|
| Voice | Pallav's clone (`ELEVENLABS_VOICE_ID`, from Pallav) |
| Model | `eleven_v4` |
| Language code | `hi` |
| Similarity | 0.9 |
| Stability | 0.5 |
| Takes | 1 |

- Input is the exact approved script. Write `9to5` as "nine-to-five" in the TTS input only; captions keep `9to5`.
- On the box the take was generated through the ElevenLabs MCP connector (a creative flow node; one generation). From elsewhere, use the same connector or the ElevenLabs text-to-speech API with the settings above. Never retry a generation call blindly: each call is a new charge.
- Save the take as `NNN_slug_L2/audio/take1.mp3`. Save the approved text as one paragraph in `audio/script.txt`.
- Log the paid call in the ledger (about 700–820 credits, roughly $0.13–0.15, for a 46–58 s take).

## 5. Process the voiceover (local, free)

```bash
export Q9_REELS_DIR=/path/to/reels
python3 scripts/process_vo.py NNN_slug_L2
```

It trims pauses longer than 0.45 s to 0.34 s, loudness-normalises to −15 LUFS (`audio/vo.wav`, 48 kHz stereo), transcribes with faster-whisper (`small.en`) for word times, aligns them to the exact script words, and writes `audio/timing.json` and `project/assets/captions.json` (chunks of at most 4 words / 24 characters, split at punctuation).

Check the printout: `unmatched` should be 0 or close to it, and the Whisper text should match the script. If Whisper mishears a word:
- First try an isolated-clip transcription of just that word (005's "Salary." was missed by the full-file pass but read correctly in isolation; no retake was needed).
- If the audio itself is wrong, retake only that line and splice it (reel 003).
- Hand-fix chunking if needed, keeping the exact script words.

If the CTA wording changes after voicing, `scripts/splice_cta.py REEL=CUT_SECONDS` replaces the old ending with the shared CTA take and rewrites the timings (used for reels 001 and 002).

## 6. L2 Hyperframes build

### The L2 look (from the moodboard v4 pick and `playbooks/COMMON_REEL_BRIEF.md`)

Light-theme kinetic type with **one polished illustrated object per beat**:
- Flat cream background `#F3EDE1`; ink `#141312` with 5 px outlines; flat fills with one shade and soft ground shadows; accent red `#D54E4C`; butter-yellow `#F2D98B` for highlighter swipes.
- Each beat is one bold statement (Inter Tight 800, 110–170 px, left at x 90, at most two lines, one word red or highlighter-swiped) plus one big illustrated object (at least 420 px tall, roughly y 330–1150). Never a text-only beat. Object labels in Inter 600, 30–36 px, uppercase, letter-spaced.
- One recurring object family across the reel (004: the QUIT door and runway strip; 005: the offer letter and dimension cards), so the last teaching beat can mirror frame 1.
- Motion is real motion graphics, not fades: words slide up from masks, highlighters draw left to right, objects pop with overshoot, numbers roll deterministically, strike-throughs draw, gentle camera push per beat, real transitions between beats. Hold every finished state at least 0.6 s.
- Each motion lands within about 0.15 s of its spoken word (times from `captions.json`).

**Zones (1080×1920, strict):** graphics and graphic text inside x 80–960, y 180–1170 (x > 960 stays clear for the Reels icons). y 1170–1250 is an empty gap. **Captions only in a dark pill at y 1250–1390**, drawn by `captions4.js` (theme `ink`: near-black pill, cream text, spoken word in soft coral). Nothing below y 1420.

**Loop ending:** frame 1 is already on screen and moving (no fade from blank). The last teaching beat returns to frame 1's object (004: the closed QUIT door swings open; 005: the offer letter returns with the dimension cards spread and TOXICITY red). The end card then holds completely still for about 1.5–2 s so the cut back to frame 1 reads as intentional.

**End card (CTA):** tilted book cover with shadow and warm halo, "Coming soon.", red pill "Join the waitlist → link in bio". No URL anywhere.

**Fine print:** money-number reels carry "Educational, not financial advice." small (Inter 600, 26 px, ink at 55%) at x 90, y ≈ 1132. No music. British spelling.

### Prepare the build folder

1. `NNN_slug_L2/ref_L2/`: copy from the previous approved build (L2 reference frames, `COMMON_BRIEF.md`, `frames_index.html`).
2. `project/`: `hyperframes.json`, `package.json`, `meta.json`; `assets/` with `vo.wav`, `captions.json`, `captions4.js` (in [scripts/l2_reference/](../scripts/l2_reference/)), `gsap.min.js` (from the `gsap` npm package), the fonts (Inter Tight, Inter, Caveat) and `book_cover.jpeg`; `tools_ref/` with the latest approved build's `art.py` and `build.py`.
3. Write `BRIEF.md` in the shape of [examples/005_toxic_hike/L2_BRIEF.md](../examples/005_toxic_hike/L2_BRIEF.md): duration D (the `vo.wav` length plus roughly 1.3–2.2 s so the end card can hold: 44.66 → 46.0 s for 004, 55.79 → 58.0 s for 005), the recurring object family, the fine-print rule, the exact numbers allowed on screen, then one numbered beat per spoken sentence with its start time from `captions.json`, the statement text, the object and each timed motion.

### Build it

Builder priority (Pallav, 20 Nov 2026): **P1** Antigravity `agy` with Gemini 4 Neon (`gemini-4-neon-high`); **P2** Claude Code (Opus) with Hyperframes; **P3** the agent itself. Hyperframes **0.9.72** renders in every case. 004 and 005 were both built by P1.

P1:
```bash
export Q9_REELS_DIR=/path/to/reels AGY_MODEL=gemini-4-neon-high
scripts/run_agy.sh NNN_slug_L2
```

P2 (from `NNN_slug_L2/`, in Claude Code): give it the same instruction `run_agy.sh` uses: read `BRIEF.md` and `../COMMON_REEL_BRIEF.md`, study `./ref_L2` (look at the PNGs), build the Hyperframes project in `./project` exactly as specified (write `index.html`, lint, check, render, mux the voiceover into `project/final.mp4`, extract QA stills, look at them and iterate), then write `NOTES.md`. The Hyperframes skills (`hyperframes`, `hyperframes-core`, `hyperframes-cli`) help here.

The Hyperframes contract the builder must follow (from the common brief):
- `<html data-resolution="portrait">`; root `<div id="root" data-composition-id="main" data-start="0" data-duration="D" data-width="1080" data-height="1920">`.
- Each beat is `<section class="clip scene" data-start=".." data-duration=".." data-track-index="N">` with a unique track index.
- One paused GSAP timeline registered as `window.__timelines["main"]`, ending with `tl.to({},{duration:0.01},D-0.01);`.
- Deterministic only: no `Math.random`, no `Date`, no CSS animations or transitions, no rAF, no external URLs. Fonts via `@font-face` from `assets/`.
- Captions: inline `captions.json` as `CHUNKS` and call `window.addCaptions4(tl, CHUNKS, {theme:"ink", lastEnd:D})`. Do not edit `captions4.js` or the caption text.

Commands, in `project/`:
```bash
[ -n "$NODE_BIN" ] && export PATH="$NODE_BIN:$PATH"
npx --yes hyperframes@0.9.72 lint      # fix errors
npx --yes hyperframes@0.9.72 check     # fix errors
npx --yes hyperframes@0.9.72 render --quality looks -o out.mp4
ffmpeg -y -i out.mp4 -i assets/vo.wav -filter_complex "[1:a]apad[a]" -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -t D final.mp4
```
Render silent, then mux; `apad` pads the voice to D so the end card holds.

Expected, harmless warnings (single-file structure, `film_silent` before mux, `outside_safe_zone` against TikTok/Shorts overlays, fast caption chunks) are listed in the 004/005 `L2_NOTES.md`.

## 7. QA (timing, captions, loop, CTA)

The builder extracts stills at the middle and end of every beat (`ffmpeg -y -ss T -i final.mp4 -frames:v 1 qa/tT.png`), looks at them and iterates at least once. The parent agent then checks again:

- [ ] `ffprobe final.mp4`: 1080×1920, has audio, duration D.
- [ ] Frame at t = 0 already shows the hook object (no blank fade-in).
- [ ] Every beat: statement plus one illustrated object; nothing clipped, cramped, text-only or off-palette.
- [ ] Nothing in the y 1170–1250 gap; nothing overlapping the caption pill; fine print (if any) above the pill.
- [ ] Captions: exact script words; the highlighted word matches the voice (spot-check against `timing.json`); the CTA is word for word.
- [ ] Each object/number lands on its spoken word (±0.15 s).
- [ ] On-screen numbers exactly as briefed, with the EXAMPLE stamp where needed.
- [ ] Loop: the last teaching beat mirrors frame 1; the end card holds still about 1.5–2 s.
- [ ] End card: cover, "Coming soon.", "Join the waitlist → link in bio"; no URL anywhere.
- [ ] No music.

Make a contact sheet for the record and the review message:
```bash
python3 scripts/sheet.py NNN_slug_L2 0.05,3.0,8.5,14,20,26,33,40,47,52,57.5 sheet.png
```

Then make the posting copy: remux `final.mp4` with `-movflags +faststart` (stream copy) to `../NNN_slug_L2.mp4` and record its sha256, size and duration in `NOTES.md`. Make a small review preview (a 540p copy under 8 MB).

## 8. Review preview to Pallav

- Send the small 9:16 review preview (never the posting mp4), the contact sheet if useful, and each caption **in its own message** (Instagram/LinkedIn caption, Threads text, and the Substack Note if one is planned).
- State the proposed slot (2 PM or 7 PM IST, which date).
- Wait. "Perfect" is not "schedule".

## 9. Pallav says "schedule": Drive + Buffer

1. **Drive:** upload the posting copy to the "Motion reels" folder (`GDRIVE_MOTION_REELS_FOLDER_ID`). The folder is "Anyone with the link: Viewer", so the file should inherit it. The Drive connector cannot create anyone-with-link grants; if the file is not public, set it in the Drive web UI.
2. **Verify** the public URL `https://drive.usercontent.google.com/download?id=<DRIVE_FILE_ID>&export=download&confirm=t` with `curl`: the sha256 of the download must equal the local posting copy. If you get a Google sign-in page, the share is wrong. Keep files under about 95 MB.
3. **Buffer:** three automatic, custom-scheduled posts at the approved slot. Details and payloads: [docs/scheduling-buffer.md](scheduling-buffer.md).
   - Instagram: video asset, `metadata.instagram = {type: "reel", shouldShareToFeed: true, isAiGenerated: false}`, the caption, no music.
   - LinkedIn: the same video and caption.
   - Threads: the same video, `THREADS.txt` (500 characters or fewer).
4. Re-read every post (`get_post`): status scheduled, correct `dueAt`, correct video URL. Report the result.
5. Append rows to the post log (`POST_LOG_CSV` and the sheet): date/slot, template `motion-reel`, file, hook, caption, tags, channels, Buffer post IDs, status, media URL, link-counter note.
6. Optional: schedule a text-only Substack Note at the same slot ([docs/substack-notes.md](substack-notes.md)).

## 10. When live

- Check the posts went live at the slot.
- Send the live links to the review bot (RRRI, "The Viewer"); see [rules/content-rules.md](../rules/content-rules.md).
- Update the reel's `NOTES.md` and the post log status.

## Time and cost per reel (from 004/005)

Script: several review rounds with Pallav. Voice: one ElevenLabs take (~$0.15). Build: one `agy` run, first try for 004, three render/QA rounds for 005. Everything else is local and free.

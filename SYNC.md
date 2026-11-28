# Weekly Saturday refresh

The box keeps evolving: new approved reels, playbook corrections, skill edits. Once a week, on **Saturday**, this repo is refreshed from the box so outside agents work from current rules.

## What runs

A weekly job on the box (Saturday, IST) runs:

```bash
scripts/sync_from_box.sh            # or --dry-run first to preview
```

It reads the live box sources, regenerates the generated folders, checks the ported scripts for upstream changes, runs the secret scan, and prints a short report of what changed. Then a human or agent reviews the diff and finishes the job (below).

Environment (defaults are the box paths):

| Variable | Default | Meaning |
|---|---|---|
| `Q9_ROOT` | the box's `quit9to5/` folder | content root |
| `Q9_MOTION_DIR` | `$Q9_ROOT/motion` | playbooks, ideas |
| `Q9_REELS_DIR` | `$Q9_MOTION_DIR/reels` | reel folders, `COMMON_REEL_BRIEF.md` |
| `Q9_SKILLS_DIR` | the box's agent-skills folder | `instagram-reel-script/SKILL.md` |
| `APPROVED_REELS` | `004_runway 005_toxic_hike` | reel script folders mirrored into `examples/` |
| `DEST` | repo root (detected from the script's location) | where to write |

Flags: `--dry-run` (report only, write nothing), `--update-upstream` (record new upstream hashes after you have re-ported a script).

## The split: generated vs curated

| Area | Type | Who changes it |
|---|---|---|
| `playbooks/` | **generated** | rewritten by the sync on every run from the box sources |
| `examples/` | **generated** | rewritten by the sync (text files of the reels in `APPROVED_REELS`) |
| `skills/instagram-reel-script/SKILL.md` | **generated** | box skill snapshot plus `PLAYBOOK_PATCH.md` appended (skipped if the box skill already has the 21 Nov rules) |
| `skills/instagram-reel-script/PLAYBOOK_PATCH.md` | curated | edited by hand when the playbook gains rules the skill lacks |
| `docs/`, `rules/`, `prompts/` | curated | a human or agent, on Saturday, after reading the sync diff |
| `README.md`, `SETUP.md`, `SYNC.md`, `CHANGELOG.md`, `NOTICE`, `.env.example`, `.gitignore` | curated | same |
| `scripts/` | curated (ported) | the sync never overwrites them; it reports **upstream drift** using `scripts/UPSTREAM.tsv` (box path + sha256 of the source when it was last ported). Re-port by hand, keeping paths parameterised, then run `--update-upstream`. |

The sync never touches curated files, so carefully written docs are not lost. If a playbook change means a doc is now wrong (for example a new CTA, a new builder, a new cadence), update the doc by hand during the Saturday review.

## What it copies, and what it never copies

Copies (text only, sanitised):
- `SCRIPT_PLAYBOOK.md`, `APPROVED_IDEAS.md`, `INSTAGRAM_SCRIPT_METHOD.md` (motion/), `COMMON_REEL_BRIEF.md` (reels/), `style-study.md`, `WAITLIST-PLAN.md` (sections about out-of-scope channels removed);
- for each approved reel: top-level `.md` and `.txt` files of `NNN_slug/` and `NNN_slug_L2/` (scripts, captions, Threads text, `BRIEF.md` → `L2_BRIEF.md`, `NOTES.md` → `L2_NOTES.md`), skipping byte-identical duplicates and `.log` files, never descending into `project/`, `audio/` or `ref_L2/`;
- the `instagram-reel-script` skill.

Never copies: `manuscript.md` or any book draft, media (mp4, wav, mp3, mov, png, jpg, jpeg, webp, gif, pdf, docx), `.env` files, secrets, `node_modules`, `.hyperframes` caches, render outputs, Quora or Reddit material, `source-accounts.md`. Draft reels that are not approved (e.g. the 006 drafts awaiting approval) are not mirrored; add a reel to `APPROVED_REELS` only after Pallav approves it.

## Scrubbing and the scan

Every copied file passes through `scripts/lib/sanitise.py`, which:
- rewrites box paths to variables (`$Q9_ROOT`, `$Q9_REELS_DIR`, `$NODE_BIN`, `$AGY_BIN`, `$PAID_CALL_LEDGER`, …);
- replaces Drive/Google file IDs, Buffer-style 24-hex IDs, 64-hex hashes, ElevenLabs-style 20-character IDs, UUIDs and GA4 IDs with placeholders;
- replaces real email addresses with `you@example.com` and phone numbers with `<PHONE>`;
- replaces manuscript line references with "manuscript.md (private, not included)";
- drops lines and sections that mention Quora or Reddit;
- fixes relative links so they resolve inside the repo.

Then `scripts/lib/secret_scan.py` scans the staged output **before** anything is written (the sync aborts and leaves the repo untouched if it fails), and scans the whole repo again at the end. It exits non-zero on: forbidden files, key/token shapes, account-ID shapes, long digit runs, real emails, phone numbers and unparameterised box paths. Reviewed false positives are listed in `scripts/secret-scan-allowlist.txt` and explained in [docs/SECRETS-SCAN.md](docs/SECRETS-SCAN.md). Never add an allowlist entry for a real secret; fix the source instead.

## Safe to rerun

The output depends only on the box sources, and the copy step only runs when something differs, so a second run with no source change reports "no changes" and writes nothing. Each run builds into a temporary staging folder, so a failure part-way leaves the repo as it was.

## The Saturday checklist

1. `scripts/sync_from_box.sh --dry-run` and read the report.
2. `scripts/sync_from_box.sh`.
3. Read the diff of `playbooks/`, `examples/` and the skill (`git diff` once the repo is under git; otherwise compare with the zip from last week).
4. If any rule changed (CTA, hook rules, builder order, voice settings, cadence, Buffer limits, approval rules), update `docs/`, `rules/` and `prompts/` to match.
5. If the report lists **UPSTREAM CHANGED**, re-port that script into `scripts/` with paths parameterised, then `scripts/sync_from_box.sh --update-upstream`.
6. If a newly approved reel should become a reference, add it to `APPROVED_REELS` (and to the job's environment) and rerun.
7. `python3 scripts/lib/secret_scan.py .` must PASS.
8. Add a dated entry to [CHANGELOG.md](CHANGELOG.md).
9. Commit and push (once a remote exists), then rebuild the zip if one is being shared.

## Git remote

The intended home is a **private** GitHub repository, something like `pallavkulhari/quit9to5-content-workflow`. It has not been created or verified from the box as of 24 Nov 2026; this repo is currently a local folder plus a zip. When the remote exists:

```bash
git init && git add -A && git commit -m "Initial packaging"
git remote add origin https://github.com/<owner>/quit9to5-content-workflow.git
git push -u origin main
```

Keep it private. Run the secret scan before every push.

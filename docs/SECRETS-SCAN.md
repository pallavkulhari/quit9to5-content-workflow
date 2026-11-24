# Secrets and redaction scan log

Run before every share, commit or zip. Two scans, plus two content checks.

## 1. Repo scanner (blocking)

```bash
python3 scripts/lib/secret_scan.py .
```

This also runs automatically at the end of `scripts/sync_from_box.sh`, and on the staged output before the sync writes anything. It fails on forbidden files (any `.env` except `.env.example`, media and binary extensions, `manuscript.md`, `part-one-draft.*`, `source-accounts.md`, `node_modules`, `.hyperframes`, `__pycache__` binaries), key and token shapes, Buffer-style 24-hex IDs, Drive/Google IDs, ElevenLabs-style 20-character IDs, UUIDs, GA4 IDs, 10+ digit runs, real email addresses, Indian phone numbers and unparameterised box paths.

**Result, 24 Nov 2026 (initial packaging):** PASS, 0 unallowlisted hits, 69 text files.

During packaging it caught, and these were then fixed:
- the sanitiser had mangled a bracket in a manuscript reference (regex fixed);
- `__pycache__/*.pyc` left by a compile check (deleted; `.gitignore` covers them);
- an SSH-style GitHub remote example in SYNC.md, which looks like an email address (changed to an HTTPS placeholder).

Reviewed false positives (in `scripts/secret-scan-allowlist.txt`):

| File | Match | Why it is allowed |
|---|---|---|
| `playbooks/SCRIPT_PLAYBOOK.md` | `linkedin.com/posts/vibhutiverma27_reel-content-viral-activity-<19 digits>-nsr1` | Public URL of a research source cited in the playbook. The digits are a public post ID, not a credential. |
| `scripts/sync_from_box.sh` | the two `${VAR:-<box path>}` defaults for `Q9_ROOT` and `Q9_SKILLS_DIR` | Intentional box defaults: the sync job runs on the box. Every other script takes paths from env/CLI. |

The scanner skips its own pattern files (`scripts/lib/secret_scan.py`, `scripts/lib/sanitise.py`, the allowlist).

## 2. Keyword scan (advisory)

```bash
rg -i 'api[_-]?key|token|secret|password|sk-|Bearer|@gmail|\+91|AIza|xox[baprs]-|ya29\.|ghp_|github_pat_|sk-ant-|sk_live|xai-|[0-9]{10,}' .
rg -i --hidden 'api[_-]?key|token|secret|password' .env.example
```

**Result, 24 Nov 2026:** no real values. All hits are false positives:
- empty variable names in `.env.example` (`ELEVENLABS_API_KEY=`, `BUFFER_ACCESS_TOKEN=`, `IMAGE_HOST_API_KEY=`, `BEEHIIV_API_KEY=`) and the same names in SETUP.md and docs/scheduling-buffer.md;
- the words "secret", "secrets", "tokens" in rules and docs ("never commit secrets", "secret scan");
- "tokens" in code comments of `process_vo.py` and `splice_cta.py` (speech-to-text word tokens);
- the regex patterns themselves in `scripts/lib/secret_scan.py` and `scripts/lib/sanitise.py`;
- the public LinkedIn post ID in the playbook (above).

## 3. Source-specific searches

- Buffer-style 24-hex IDs, `drive.google.com` / `id=1…` IDs, 20-character mixed IDs, `@outlook` / `@yahoo` / `@hotmail`, WhatsApp, `+91`, 10-digit mobile numbers: only hit is the word "WhatsApp" in `playbooks/WAITLIST-PLAN.md` (about link previews). False positive.
- Every concrete ID seen while reading the sources was searched for literally (the ElevenLabs voice ID, the Drive folder and file IDs for the "Motion reels" folder and reels 003–005, the Obsidian vault folder, the post-log Sheet, a blog Google Doc, Buffer post IDs, an ElevenLabs flow ID, a content UUID, the beehiiv publication prefix, the GA4 ID, file hashes, the publisher's editorial email and names from the contract notes): **0 matches**.

## 4. Scope and book-text checks

- Quora and Reddit: mentioned only as exclusions (README, CHANGELOG, SYNC, rules, crossposting, the sync script's drop list). Their sections were removed from the copied WAITLIST-PLAN.
- Manuscript: a 9-word shingle comparison of every repo file against `manuscript.md` (private, not included) found only short overlaps inside the approved public captions of reels 004 and 005 (e.g. "When I quit, I had a runway of roughly three years") and one quote of that caption in docs/captions.md. These are published, Pallav-approved captions, not book passages. No manuscript passages are in the repo. `SCRIPTS.md` and the reel 006 drafts were left out because they quote the manuscript.

## If the scan fails

Fix the source (box file or curated doc), or extend `scripts/lib/sanitise.py` so the sync scrubs it. Only add an allowlist line for something you have checked is public and harmless, and record it in the table above.

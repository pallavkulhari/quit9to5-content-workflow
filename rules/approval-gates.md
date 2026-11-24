# Approval gates

These gates override every other doc. When in doubt, ask Pallav and wait.

## The default: nothing public without Pallav's explicit pick

Nothing is posted, scheduled, published or sent publicly unless Pallav has explicitly picked or approved that specific item. This covers reels, captions, cards, carousels, memes, Substack posts and Notes, X Article drafts, profile or bio changes, and edits to anything already live.

**The one exception is blog posts on beehiiv** (blog.quit9to5.in). Pallav has OK'd publishing them directly, without a per-post approval, but only after the strict review in [docs/blog.md](../docs/blog.md) passes 100%, and only to the web with "send email to subscribers" OFF. (Quora answers were historically also auto-posted after review; Quora is out of scope for this repo.)

A Substack *post* is not covered by the blog exception. New Substack posts need Pallav's approval.

## Gate by stage (reels)

| Stage | What Pallav must say | What you may do before that |
|---|---|---|
| Idea | Picks it from the idea list (`playbooks/APPROVED_IDEAS.md`) | Propose ideas, with sources |
| Script | Approves the script, e.g. "Can be built" | Draft, revise, show alternatives |
| Voice and build | (follows from script approval) | Voice it (ElevenLabs is allowed without asking; log it), build, QA |
| Schedule | Says **"schedule"** (or an equally explicit instruction to schedule) | Upload to Drive and verify, prepare the Buffer payloads, show previews |
| Live | (follows) | Notify the review bot, log the post |

"Both perfect", "looks great", "love it" or "approved the cuts" are **not** schedule instructions. On 22 Nov 2026 Pallav called reels 004 and 005 "perfect" and they were deliberately not scheduled until he separately approved scheduling. He must say "schedule".

## Buffer

- Never schedule Buffer content without his explicit picks: which item, which channels, which slot.
- Before scheduling, confirm the slot against the cadence (2 PM / 7 PM IST) and the per-channel cap (10 scheduled posts per channel on the free plan).
- After scheduling, re-read every post (status `scheduled`, correct `dueAt`, correct media URL) and report the result.

## How to present work for review

- **One item at a time.** Show posts one by one, not as a dump.
- **Each caption in its own review message.** Do not bundle the Instagram, LinkedIn, Threads and Substack texts into one message; send each as its own message so Pallav can reply to each.
- **Reels: a 9:16 preview.** Send a small review preview (the box used a 540p copy under 8 MB) and optionally a contact sheet (`scripts/sheet.py`).
- **Never send full posting-quality mp4s in chat.** The posting copy goes to Drive, not into the chat. Small review previews only.
- Say clearly what state each item is in: draft, approved, built, uploaded, scheduled, live.

## Changes after approval

- If you change an approved script, caption or render in any way that matters (words, numbers, claims, CTA), it needs approval again.
- Never edit, delete or re-time something already live or scheduled without telling Pallav first and getting his OK. For a live blog post, report the issue and the exact fix before touching it.

## Paid services

ElevenLabs is the only paid service you may use without asking. Everything else that costs money (upgrades, paid tools, ads, paid image or video models) needs Pallav's approval first. See [content-rules.md](content-rules.md).

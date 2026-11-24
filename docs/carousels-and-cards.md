# Carousels and cards

Still-image formats. Cards are the original Quit 9to5 pillar (October–November 2026); carousels are being added, and **on some days a carousel replaces the second (7 PM IST) reel**. Prompt: [prompts/carousel-or-cards.md](../prompts/carousel-or-cards.md).

## Card formats on the box

| Format | Generator | Output |
|---|---|---|
| Quote / tweet-style card, template v1a (approved, final) | [scripts/cards/var.py](../scripts/cards/var.py) `make1(text, "L", out)` | 1024 px square (rendered at 3x, downsampled) |
| 9:16 story version of the same card | [scripts/cards/make_insta.py](../scripts/cards/make_insta.py) `make_insta(text, out)` | 1080×1920 |
| Structured cards: checklist, numbers, myth vs reality, 3-step framework | [scripts/cards/fmt12.py](../scripts/cards/fmt12.py) helpers on the v1a template | square + story |
| Photo book-page card | `cards/template_v2/make_bookphoto2.py` on the box (not ported) | 70–90 words, one highlighted key line, footer "Quit 9to5 · Coming January 2027" |

**Template v1a:** white background with a coral top bar (213, 78, 76) and charcoal text (45, 45, 44); Pallav's avatar with a thin ring, "Pallav Kulhari" with a blue badge and the handle; the line in Inter at 42 px; the book cover bottom-left with a red rule and "Coming January 2027" beside it. No bold "Quit 9to5" text beside the cover (the cover shows the title). No fake like counts. In the text, `\n` starts a new paragraph and `[text]` gets a soft red highlight.

Assets the generators need (not in the repo, ask Pallav): `pallav_photo.jpg`, `book_cover.jpeg`, plus the Inter variable font. Point `Q9_CARD_ASSETS` and `Q9_FONT_INTER` at them.

Batch pattern on the box: copy the latest `gen_batchN.py`, replace the list of lines and the output folder, run it; it prints the wrapped line count per card. Keep each card to 2–4 lines (about 12–40 words).

## Writing card lines

Sources: the book first (career dimensions, money as a stress painkiller, retirement myth, golden handcuffs, Career Satisfaction Score, irreplaceability), then LinkedIn posts, then new lines aligned with a chapter. Label each line `book`, `LinkedIn` or `new (ch X idea)`.

Style (from [playbooks/style-study.md](../playbooks/style-study.md)): one idea per card; 12–30 words is best, about 40 the ceiling; the punch in the last 3–6 words; concrete anchors (₹, LPA, EMI, hike, manager, Sunday); superlatives and thought experiments ("Count…", "Imagine…") work without context; mirrored pairs only when both halves are concrete.

**Review rubric (score 0–2 each, pass at 11/14 with no zero on 1, 4 or 5):** standalone in 3 seconds; clear insight; on theme and traceable to a chapter; no banned patterns; no AI cadence or cliché; no textbook tone; punchy turn at the end.

**Hard gates (fail any = reject):** G1 relatable to an ordinary Indian salaried person; G2 logically airtight on first read; G3 closes the loop ("okay, so what do I do?" is answered). Standing rules: introduce every concept before using it; every card answers "so what?".

Workflow: draft about 25 candidates → review harshly as Pallav would ("would a Pune IT employee nod on first read?") → keep the best 10 → render → open every card at full size and check wrapping, overlaps and crispness → report each line with its source, why it passes, and the rejects with reasons → Pallav picks → approved cards are copied to the final folder.

Captions for cards: add something the card doesn't say and end on an action or payoff. No hashtags, no em dashes. Waitlist link per the link-in-5 counter.

## Carousels

The carousel built on the box is **"cover reveal"** (`carousel/cover-reveal/`): 17 slides at 1080×1350 that progressively tear a hole in a sheet of paper to reveal a rendered 3D paperback of the book on a warm studio backdrop (`scene.py` renders the book scene; `make.py` renders the slides with deterministic torn-edge profiles and a contact sheet). It is a book-announcement asset, not an explainer.

For explainer carousels that replace the second reel, reuse the reel's thinking:
- One idea, one chain of thought, the hook on slide 1 (4–7 words) and the payoff near the end.
- One statement plus one visual per slide, in the L2 palette or the card template; numbers appear on the slide where they are explained; label examples.
- Last slide: the book cover, "Coming soon" / "Coming January 2027" and "Join the waitlist: link in bio".
- 1080×1350 for Instagram and LinkedIn. Caption per [captions.md](captions.md).
- Approval: Pallav picks the carousel and the slot, and says "schedule". Image URLs must be public (image host).

## Older still-card reels (insta-auto)

Before motion reels, some cards were turned into short still-image Instagram Reels (`insta-auto/*_reel.mp4`) that were not scheduled through Buffer; Pallav posted them to Instagram himself. From 21 Nov 2026 motion reels are scheduled as automatic Buffer Reels instead; the still-card reels are history.

## Logging

Every scheduled card or carousel gets a post-log row (see [scheduling-buffer.md](scheduling-buffer.md)). Approved lines go to the rubric's gold examples, rejected ones to its anti-patterns, so the next batch learns.

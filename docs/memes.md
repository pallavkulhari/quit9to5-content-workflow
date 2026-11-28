# Memes

Memes are the third content pillar after book cards and reels (research written 21 Oct 2026). They earn reach with relatable Indian office humour and plug the book only occasionally. Every meme batch has so far been "unscheduled, awaiting Pallav's picks": nothing posts without his pick.

## What works (from the box research)

- Formats: classic templates (Drake, Two Buttons, Gru's plan, Distracted Boyfriend, Expanding Brain, Change my mind, Is this a pigeon?, This is fine), original text/comic formats ("POV:", Notes-app style, chat mock-ups, expectation vs reality in brand style), and generated scenes ("corporate guy at a laptop at 11 PM").
- The Indian accounts that win use rupee, EMI and appraisal specifics, some Hinglish, and one punchline per image.
- Themes: hikes swallowed by EMIs and rent, appraisal waits, "quick call" culture, notice periods, Sunday dread, loyalty vs restructuring, chai-break complaining vs building an exit.

## Legal and safety (follow strictly)

India has no general meme fair use; using film stills or stock photos on a brand account that promotes a book is commercial use. Safest first:
1. Original or generated images, or Pallav's own photos.
2. Classic template plus new text: transformative, no logos, no implied endorsement. Acceptable.
3. Film/TV stills: rarely; no plug and no book cover on those posts; never use an actor's face to sell.

Never: repost someone else's meme (even with credit), post tweet screenshots, or mock real people by name. Take anything down at once if a rights-holder complains. Do not imitate real actors' likenesses in generated images.

## Making them

- Local and on-brand with Pillow: [scripts/memes/meme_lib.py](../scripts/memes/meme_lib.py) `meme(template, top=..., bottom=..., boxes=[...])` places the template on a 1080×1350 canvas, fits text into boxes (white with stroke, or black), and adds a small grey "quit9to5.in" corner mark. Templates live in a local folder (`MEME_TEMPLATES`), not in the repo.
- The box also writes a 9:16 story version by pasting the 1080×1350 meme onto a white 1080×1920 canvas.
- Imgflip and similar tools add watermarks and grant no rights to the underlying image; prefer local rendering.
- No paid image tools without Pallav's approval.

## Captions

Each meme gets a one- or two-sentence caption that turns the joke into a takeaway, in Pallav's voice. Examples from batch 5:
- Two Buttons (appraisal): "We wait 12 months for one letter to tell us what our work was worth. That wait is the real cost of depending on one salary."
- Gru (hike/EMI): "Every hike came with a bigger EMI. Five years in, the salary is higher and the freedom is lower."

Plug on at most one in three memes, and word every plug differently. The link-in-5 counter still applies to the waitlist link.

## Cadence (proposed in the research)

About three memes a week (e.g. Monday dread, Wednesday, Friday evening); Instagram and Threads get all of them, LinkedIn gets about one a week (the cleanest one). Grow only if saves and shares beat the card pillar. Within the current two-slot day, a meme takes a slot only when Pallav picks it for one.

## Review

Show the batch with each caption, the template source and the risk tier. Pallav picks; then it follows the normal Buffer flow. Notify the review bot when live.

## Quit 9to5 patch (from `playbooks/SCRIPT_PLAYBOOK.md`, 20–22 Nov 2026)

The skill above is generic and marks brand inputs as **[BRAND]**. For Quit 9to5, fill them in with the rules below. They come from Pallav's corrections recorded in the playbook. Where anything above disagrees, these rules win, and the playbook wins over both.

### [BRAND] voice: explain it out loud (21 Nov 2026, overrides Step 4's "short sentences")
- Write like Pallav explaining something out loud: **coherent full sentences** that define a concept before applying it ("Let me tell you about…"). Do not write crisp, clipped fragment lines. Reel 004's first draft was rejected as "too crisp and incoherent" for exactly this reason.
- Define every concept before you use it (runway, career dimensions, irreplaceable). Give the viewer the full context; don't assume they know the idea.
- British spelling (optimising, per cent in captions). Indian context: rupees, lakh, EMI, salary, manager, 9to5.
- No em dashes, no "so basically", no "in this video", no greeting.

### [BRAND] hook (21 Nov 2026, overrides the "Goal hook" default)
- **Do not force every reel to open with "Want to quit your 9to5?"** The hook comes from the reel's own idea. Use a quit opener only when the topic genuinely leads there (savings, runway, EMIs). Reel 005's first draft was rejected because its "Want to quit your 9to5?" opener was unrelated to the topic; the approved version opens on the job-offer dilemma itself.
- Never open with a term the viewer hasn't been given a reason to care about. Introduce jargon (e.g. "runway") only after the why.

### [BRAND] mandatory CTA (20 Nov 2026, every reel, last spoken line)
> My book Quit 9to5 is coming out soon. Join the waitlist in bio.

- Same words in the voiceover, the burned-in captions and the end card. No URL in the voice or on screen for reels (the older "Join the waitlist at quit9to5.in" close in the S2/S3 skeletons is retired for reels).
- End card: tilted book cover with shadow, "Coming soon.", a pill "Join the waitlist → link in bio". Hold it still about 1.5–2 s so the loop back to frame 1 reads as intentional.

### [BRAND] fact base and compliance
- Claims come only from the book (`manuscript.md`, private, not included), published blog posts, or `blog/facts.md`. Never invent a personal story, statistic or quote. Label illustrative numbers as **EXAMPLE** on screen.
- Number/money reels carry small on-screen fine print "Educational, not financial advice." (not spoken). Captions that give numbers end with it before the CTA.
- At most two spoken numbers. Recheck the maths. Show exact figures on screen (₹19.2 lakh, not 19).

### [BRAND] length (from the 004/005 reference reels)
- The retention rules allow 30–38 s for one worked example and 25–30 s for a pure reframe. The approved reference reels ran longer because the explaining voice needs room: 004 runway is 135 spoken words (46 s), 005 toxic hike is 143 words (58 s). Every second still has to earn the next. Cut repetition, not definitions.

### [BRAND] reference scripts (22 Nov 2026)
Pallav called reels 004 and 005 "perfect" and asked for future scripts in the same way:
- `examples/004_runway/SCRIPT_v2_voiceover.md`
- `examples/005_toxic_hike/SCRIPT_APPROVED.md`

Copy from them: a hook that comes from the idea itself; the "let me tell you about…" explaining flow in full sentences; concepts defined before they are applied; one first-person proof line where the book supports it; the mandatory CTA at the end.

### [BRAND] visual style and builder
- Style L2 (`playbooks/COMMON_REEL_BRIEF.md`): light cream background, kinetic type statement plus one polished illustrated object per beat, captions in a dark pill at y 1250–1390, a last teaching beat that loops back to frame 1.
- Builder priority (20 Nov 2026): P1 Antigravity `agy` with `gemini-4-neon-high`; P2 Claude Code with Opus; P3 the agent builds it itself. Hyperframes 0.9.72 renders in every case.

### [BRAND] approval
- A script is a draft until Pallav approves it ("Can be built"). Nothing is voiced, built or scheduled from an unapproved draft. See `rules/approval-gates.md`.

# Prompt: caption pack from an approved script

Turns an approved reel voiceover into the Instagram/LinkedIn caption, the Threads text and (optionally) a Substack Note. Works in Claude or Gemini. Give it: the approved voiceover, the on-screen numbers, the sources, and the two reference caption sets in `examples/`.

---

You are writing the captions for an approved Instagram reel by Pallav Kulhari (book *Quit 9to5*, Embassy Books, January 2027). Goal: waitlist signups. Follow `docs/captions.md`, `rules/voice-and-style.md` and `rules/content-rules.md`. Match the style of `examples/004_runway/CAPTION_v2.txt`, `examples/005_toxic_hike/CAPTION.txt` and their `THREADS.txt` files.

**Approved voiceover:**
{paste}

**Numbers shown on screen:** {e.g. ₹12 lakh, ₹6 lakh / year, 2 years, or "none"}
**Sources and allowed personal facts:** {list}

Write three texts:

1. **Instagram + LinkedIn caption** (one shared text):
   - Line 1: the reel's idea as a claim or its hook, strong enough to work alone.
   - Then explain the concept more fully than the reel did, in full sentences in Pallav's explaining voice.
   - Add value the reel had no room for: the full worked example ("Here's an example, not a target…") or "How to calculate yours:" with 2–3 `→` steps, or the nuance.
   - At most one first-person line, only if the sources support it.
   - A closing question or reframe.
   - "Educational, not financial advice." on its own line if money numbers appear.
   - Last line exactly: "My book Quit 9to5 is coming out soon. Join the waitlist in bio."
   - No hashtags, no links, no emojis, no em dashes. British spelling ("50 per cent").
2. **Threads**: the same idea compressed to **500 characters or fewer**, same CTA last. Report the character count.
3. **Substack Note** (only if asked): text-only, about Threads length, ending with "Join the waitlist at quit9to5.in." unless Pallav has set another wording.

Rules: every number must match the reel exactly; add no claim beyond the voiceover and the sources; no "X, not Y" constructions.

Output each text in its own fenced block with a heading, so each can be sent to Pallav as a separate review message.

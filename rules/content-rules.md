# Content rules

Applies to every piece of Quit 9to5 content. Where a playbook and this file disagree, the newer dated rule from Pallav wins; when unsure, ask.

## 1. The goal and the only CTA link

- The goal of everything is waitlist signups at **quit9to5.in** (`https://www.quit9to5.in/`).
- It is the only CTA destination. Do not send people anywhere else as the call to action.

## 2. CTA on every reel

Every reel ends with this exact spoken line, in the voiceover, the burned-in captions and the end card:

> My book Quit 9to5 is coming out soon. Join the waitlist in bio.

- No URL in the reel's voice or on screen. The end card shows the cover, "Coming soon." and a pill "Join the waitlist → link in bio".
- The Instagram, LinkedIn and Threads captions of a reel also end with the same line.
- Older scripts that end "From my book, Quit 9to5. Join the waitlist at quit9to5.in." use the retired close; replace it.

Other formats:
- **Cards and image posts** follow the link-in-5 counter: every fifth Buffer post carries the waitlist link in its caption, the four before it carry none (newest rule, 10 Nov 2026). LinkedIn and Threads use the plain `https://quit9to5.in` (long UTM links look broken there). Reels count towards the counter but never carry a URL.
- **Blog posts** carry soft waitlist links with UTMs (see [docs/blog.md](../docs/blog.md)).

## 3. Hooks come from the idea itself

- Do **not** force "Want to quit your 9to5?" onto every hook. Use a quitting opener only when the topic genuinely leads there (savings, runway, EMIs). Reel 004 (runway) opens with it; reel 005 (a job offer) does not.
- Never open on a term the viewer has no reason to care about yet ("runway"). Give the why first, then name the concept.
- No greeting, no "in this video", no clickbait formulas.

## 4. Pull ideas from the book where they exist

- The North Star is the book. Where a book idea exists for a topic, use it (career dimensions, runway, irreplaceability, Alignment Tax, Career Satisfaction Score, money as a painkiller, and so on).
- Approved fact sources only: the book (`manuscript.md`, private, not included; ask Pallav or the box agent for the relevant passage), published blog posts, `blog/facts.md` on the box, and Pallav's own statements. Label every claim's source in the script notes.
- Never invent a personal story, quote, number or statistic. Do not imply something happened to Pallav unless he has said so (reel 005's notes record that he did not take a toxic job for a hike, so no script may suggest it).
- Never paste book text into public content beyond what Pallav has approved, and never into this repo.

Facts that are already public in captions and scripts, and may be restated:
- *Quit 9to5* is published by Embassy Books, out January 2027.
- Waitlist: quit9to5.in.
- Pallav kept his spending low and saved 50–75 per cent of his earnings (blog and LinkedIn also give "40% rising to 70–75%"; use the figure your source gives and say which).
- He uses the startup "runway" framing: savings divided by spending. When he quit he had a runway of roughly three years (some sources say three to four years).

## 5. Money and finance caveats

- Whenever content gives money numbers (runway examples, savings rates, EMIs, SIPs), add **"Educational, not financial advice."**
  - Reels: small on-screen fine print, never spoken.
  - Captions: its own line, just before the CTA.
- Label illustrative figures as an **example** ("Example, not a target") and keep them on screen, not in a stream of spoken maths.
- Recompute every calculation. Show exact figures (₹19.2 lakh, not 19). Use Indian formatting (₹12 lakh, ₹6,00,000).
- Do not give advice Pallav has not given (specific investments, insurance products, debt order) unless he confirms it.
- Reels that are not about money numbers (e.g. 005, career dimensions) do not carry the fine print.

## 6. Notify the review bot after anything goes live

After any public content goes live (reel, caption post, card, blog post, Substack post or Note, X Article), send the live link(s) to **RRRI, "The Viewer"**, Pallav's post-publish review bot. It reviews live content against rubrics and logs flags; it does not edit or publish. Its ID and contact are placeholders in `.env.example` (`REVIEW_BOT_ID`, `REVIEW_BOT_CONTACT`). If you cannot reach it, tell Pallav the links so he can forward them.

## 7. Paid services

- **ElevenLabs is the only paid service allowed without asking.**
- Log every paid call (including failed ones that cost $0) as a row in the paid-call ledger (`PAID_CALL_LEDGER`), with columns `timestamp_ist,bot,provider,model_or_service,purpose,units,unit_type,cost_usd,cost_basis,notes`. Example from reel 005: `eleven_v4`, one take, about 818 credits, estimate about $0.15.
- Do one take per voiceover. Retake only a line that speech-to-text mishears (reel 003 retook one line and spliced it).
- Anything else that costs money needs Pallav's approval first.

## 8. Spelling, format, channel hygiene

- British spelling: per cent (in prose and captions), optimising, practise (verb), learnt, programme. Rupees with ₹ and lakh.
- No em or en dashes in published copy. No hashtags on cards. No engagement bait ("comment YES").
- Original content only: no reposted memes, no tweet screenshots, no watermarks from other tools.
- Do not schedule anything to X via Buffer; X is not a Buffer channel any more.
- Do not resume Reddit or Quora work; both are outside this workflow.

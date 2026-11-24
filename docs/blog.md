# Blog posts (beehiiv, with Substack cross-posts)

The blog is blog.quit9to5.in on beehiiv (free plan). Posts are search-led, 900–1,200 words, in Pallav's blog voice, and each one pulls from a book framework or Pallav's own answers. Prompt: [prompts/blog-post.md](../prompts/blog-post.md).

**Approval:** blog posts are the one format Pallav lets go live without a per-post approval, but only when the strict review below passes 100%, and only to the web with email OFF. Substack versions of a post do need his approval ([crossposting.md](crossposting.md)).

## Cadence and picking a topic

- Tue, Thu and Sat around 10:00 AM IST (the box runs this as a routine).
- Topics come from `blog/calendar.md` on the box (target keyword, angle, book source, internal links). Already-live posts are listed in `blog/existing-posts.md`; never repeat one, link to it instead.
- Mix rule used on the box: if Pallav's answers exist for a topic (`postNN-work/pallav-answers.md`), write that one; if not, write a "book post" from an uncovered chapter. Topics waiting on his answers stay waiting; ask him, don't invent.

## Fact and voice sources

- `blog/facts.md` (on the box) is the only fact source, plus the book (`manuscript.md`, private, not included) and Pallav's own answers. Add new rows to `facts.md` when you use a new book passage.
- Voice: `blog/existing-posts.md` style analysis, the LinkedIn voice guide and [rules/voice-and-style.md](../rules/voice-and-style.md).

## Workflow (one file per step in `blog/postNN-work/`)

1. **Audit.** Read the live posts and everything published since. Check the calendar for cannibalisation.
2. **Brief: the 5-question gate.** One line each, or don't write the post:
   1. The exact reader question, in the reader's words (e.g. "how much savings before quitting job").
   2. The direct answer in 1–2 sentences (becomes the answer paragraph near the top).
   3. Where every fact comes from (`facts.md` row). Gaps listed as `[PALLAV: ...]`.
   4. What only Pallav can say (his story, numbers, framework). If nothing, stop and ask him.
   5. Which book framework or chapter, and which 2–3 older posts it links to.
3. **Outline: one idea per H2**, with the one-sentence bridge to the next H2. The H2s read top to bottom as one argument: hook, problem, answer, proof, mechanics, action, close. (Example: post 8's outline goes from "What did my parents say when I told them?" through "When should your family's worry stop you?" to "What happens after you've made the call?")
4. **Draft:**
   - personal hook in 1–3 short, literal lines (no scene-setting metaphors);
   - the answer to the title within the first ~150 words, in 40–60 quotable words ("So, how do you …? …");
   - a top CTA line straight after it: "(My book, *Quit 9to5*, comes out in January 2027. [Join the Quit 9to5 waitlist](https://www.quit9to5.in/?utm_source=blog&utm_medium=post&utm_campaign=waitlist&utm_content=<slug>-top) to hear when it's out.)";
   - 6–9 H2s, all questions; paragraphs of 1–4 lines;
   - the framework in bold, introduced as "In my upcoming book, *Quit 9to5*, I…";
   - 1–2 pull quotes; 2–3 internal links to older posts on descriptive anchors (the post title);
   - ending order: closing callback, "Thought exercise:", then the italic CTA block with the second waitlist link (`utm_content=<slug>-end`).
5. **De-AI and repetition pass.** Banned words and patterns ([rules/voice-and-style.md](../rules/voice-and-style.md)); no triplets or fragment runs in consecutive sections; each idea and number explained in one place only; filler words ("actually", "really", "simply", "just") two times or fewer in the whole post.
6. **Fact check.** Every number, claim and story beat against `facts.md`; recompute all arithmetic; anything unsourced is cut or asked about **before** publishing.
7. **AI-SEO pass.** Each H2 opens with a sentence that answers it; extractable blocks (formula, worked numbers, steps); title = reader's question, 60 characters or fewer; SEO title 60 or fewer (48 or fewer if you want " | Quit 9to5" to show); meta description 120–155 characters with the query phrase and one concrete fact; subtitle 70–120 characters; slug 3–6 lowercase hyphenated words with the keyword.
8. **Thumbnail.** 1200×630 JPG in the approved series style: light notebook-grid background, flat charcoal illustration with one red accent on the left, two-line Josefin Sans title on the right (line 1 ink, line 2 red, grey stroke). Copy [scripts/blog/make_thumb.py](../scripts/blog/make_thumb.py) per post. Compare side by side with earlier thumbs and at feed size (~360 px).
9. **Mechanical checks:** `python3 scripts/blog/autochecks.py postNN.md "So, how do you <lead-in>"` (word count, banned hits, dashes, curly quotes, filler, "X, not Y", ₹/÷ counts, H2s all questions, links and waitlist count, bold %, answer position, metadata lengths). Check every link returns 200.
10. **Build the HTML:** `python3 scripts/blog/build_html.py postNN.md postNN_publish.html` (UTF-8, `<meta charset="utf-8">`).
11. **Pre-publish gate:** the full strict checklist (voice, coherence, repetition, banned patterns, facts, encoding, formatting, links, SEO metadata, thumbnail, distribution settings) must be 100% ticked; save the ticked copy as `postNN-work/review.md`. The full list is in `blog/REVIEW-PROCESS.md` on the box; its key points are in this doc.
12. **Publish in the beehiiv web editor** (the connector cannot create or publish posts on this plan). On the box the HTML is uploaded to Google Drive as a Doc or served locally, then pasted into beehiiv. Set title, subtitle, slug, SEO title, meta description and thumbnail (thumbnail on top ON); quote blocks in the left-bar "Side quote" style used by older posts; dividers with beehiiv's divider block; audience **web only**, "send email to subscribers" **OFF** (confirm on the final review screen); author Pallav Kulhari; publish date now.
13. **Post-publish QA at once:** `python3 scripts/blog/live_qa.py <live-url> postNN_publish.md`. It fetches with a cache-buster and checks HTTP 200, title/meta/og:image, no mojibake or placeholders, no dashes, ₹ count equals the source, headings, quote-block style, every link, and takes desktop and mobile screenshots (needs `beautifulsoup4` and headless Chrome). Then by eye: text diff against the source, headings in order, thumbnail shows, nothing overflows on mobile, 0 emails sent.
14. **Report and notify.** Send Pallav the live link and two screenshots (top and the CTA end) with any issue and its exact fix (don't edit the live post without telling him). Send the live link to the review bot (RRRI, "The Viewer"). Mark the calendar row PUBLISHED.

## Known beehiiv gotchas

- Pasting HTML can garble ₹ and ÷; check the editor preview and the live page.
- beehiiv appends " | Quit 9to5" to the `<title>`.
- The theme has a second H1 ("Quit 9to5") in the page chrome; leave it.
- Google Doc conversion can turn the top divider into a "## ---" heading and bold text into H2s; fix these in the editor after pasting.
- A tall headless screenshot shows a blank band under the hero image; that is an artefact.

## Distribution after publishing

- Substack cross-post (needs approval) and X Article draft: [crossposting.md](crossposting.md).
- A reel or card can later pull from the post's idea; link the source post in the script notes.

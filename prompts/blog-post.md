# Prompt: blog post in Pallav's style

For blog.quit9to5.in (beehiiv). Follow `docs/blog.md`. Give the model the brief (5-question gate), the outline, the fact rows from `facts.md`, Pallav's answers if any, and 1–2 published posts as voice references.

---

You are writing a blog post for Pallav Kulhari's blog, blog.quit9to5.in, ahead of his book *Quit 9to5* (Embassy Books, January 2027). It should read like Pallav talking to a younger cousin: plain, earnest, first person, Indian context (₹, lakh, EMI, hike, manager), British spelling.

**Reader question (title):** {e.g. "How Do You Learn a New Skill While Working Full Time?"}
**Target keyword:** {…}
**Direct answer (1–2 sentences):** {…}
**Book framework / chapter:** {name it; it goes in bold, introduced as "In my upcoming book, *Quit 9to5*, I…"}
**Pallav's own story and numbers (only these):** {…}
**Facts allowed (facts.md rows):** {…}
**Internal links (2–3 older posts, title + URL):** {…}
**Slug:** {3–6 words}
**Outline (one idea per H2, with bridges):** {…}

Write the post in Markdown with this front matter: `title`, `seo_title` (60 characters or fewer), `subtitle` (70–120), `target_keyword`, `slug`, `meta_description` (120–155, with the keyword and one concrete fact), `thumbnail`.

Body rules:
- Open with a personal, literal hook in 1–3 short lines. No scene-setting metaphor.
- Within the first ~150 words, the answer paragraph: "So, {question}? {40–60 quotable words}".
- Then the top CTA line: (My book, *Quit 9to5*, comes out in January 2027. [Join the Quit 9to5 waitlist](https://www.quit9to5.in/?utm_source=blog&utm_medium=post&utm_campaign=waitlist&utm_content={slug}-top) to hear when it's out.)
- 6–9 H2s, all questions, following the outline; each H2 opens with a sentence that answers it. Paragraphs of 1–4 lines. Lists only for 3+ parallel items.
- The book framework in bold once; 1–2 pull quotes (as `>` blocks, no typed quote marks).
- His recurring phrases at most once each: "my upcoming book, *Quit 9to5*", "on your own terms", "first-principles", "Do you see it?", "Thought exercise:".
- End: a closing callback, then "Thought exercise:", then an italic CTA block with the second waitlist link (`utm_content={slug}-end`). Book mentioned at most 3 times; exactly 2 waitlist links.
- 900–1,200 words.
- Never: em or en dashes; "X, not Y" / "It's not X, it's Y" / "You don't need X. You need Y"; "Here's the thing"; "Let that sink in"; AI vocabulary (delve, leverage, unlock, harness, navigate, robust, seamless, crucial, furthermore, moreover…); filler words more than twice in total; triplets in consecutive sections; any fact or number not in the list above; advice Pallav hasn't given.
- If something you need is missing, write `[PALLAV: question]` instead of guessing. The post cannot be published until every marker is answered.

After the post, list: every number with its source row, and each `[PALLAV: …]` marker.

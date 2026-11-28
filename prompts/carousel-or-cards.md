# Prompt: card lines or carousel copy

For the v1a quote cards, structured cards and explainer carousels. See `docs/carousels-and-cards.md`. Give the model the card rubric summary in that doc, the style study (`playbooks/style-study.md`), the post log's recent `key_line`s (to avoid repeats) and the source material.

---

You write copy for Pallav Kulhari's *Quit 9to5* image posts (book by Embassy Books, January 2027). Audience: Indian salaried professionals, about 24–35, earning well but tired of the 9to5.

**Mode:** {cards | carousel}
**Source material:** {book chapter ideas, LinkedIn posts, facts.md rows}
**Recently posted lines (do not repeat the sentence, story or theme within 3 days):** {…}

### If mode = cards
Draft 25 candidate lines, then review them harshly and keep the best 10.
Each line:
- one idea, 12–40 words (best 12–30), 2–4 lines on the card;
- understood by a stranger in 3 seconds (no backstory, no dates, no "my father");
- relatable to an ordinary Indian salaried person (EMI, hike, appraisal, manager, commute, Sunday);
- logically airtight on first read;
- closes the loop: the reader knows what to do or think next; the payoff is in the last 3–6 words;
- introduces any concept before using it;
- no "X, not Y", no "It's not X, it's Y", no "You don't need X. You need Y", no em dashes, no AI cadence, no poster slogans, no textbook definitions.
For each kept line give: the line; its source label (`book`, `LinkedIn` or `new (ch X idea)`); a one-line reason it passes the gates; a caption that adds something the card doesn't say and ends on an action or payoff. Then list the rejects with reasons.

### If mode = carousel
Write a 6–10 slide explainer on one idea:
- Slide 1: the hook, 4–7 words, plus a one-line subhead.
- Middle slides: one statement (one highlighted word) plus a description of the one visual for each slide; one step of the explanation per slide, in Pallav's explaining voice; numbers appear on the slide that explains them, examples labelled; "Educational, not financial advice." on any slide with money numbers.
- Payoff slide: the takeaway, no new claim.
- Last slide: book cover, "Coming soon", "Join the waitlist: link in bio".
- Then an Instagram/LinkedIn caption per `docs/captions.md` and a Threads version of 500 characters or fewer.

Never invent a personal story or statistic. Mark anything uncertain as `[PALLAV: …]`.

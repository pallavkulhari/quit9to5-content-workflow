# Cross-posting

How one piece of content moves between the blog, Substack, X Articles and social. The flow that exists on the box (post 8, "How Do You Tell Your Family You Want to Quit Your Job?", 14–16 Nov 2026) is the template.

## Map

| From | To | How | Approval |
|---|---|---|---|
| Blog post (beehiiv) | Substack post | Re-paste the post as a Substack post in the browser | **Needs Pallav's approval** |
| Blog post | X Article (draft) | Draft in X's Article editor with a 5:2 cover | Pallav approves the specific cover and publishes or OKs publishing; he signs in himself |
| Reel caption | Substack Note | Text-only Note at the matching slot | Needs his pick ([substack-notes.md](substack-notes.md)) |
| Reel or card | Instagram, LinkedIn, Threads | Buffer, same slot on all three | "schedule" ([scheduling-buffer.md](scheduling-buffer.md)) |
| Blog idea | Reel / card | New script from the same idea, citing the post | Normal reel gates |

Do not cross-post to X through Buffer, and do not post to Quora or Reddit.

## Blog → Substack post

Files on the box: `crosspost/postNN_substack.md` and `postNN_substack_paste.html`.
- Same title; a Substack subtitle.
- An opening that suits Substack readers. Post 8's Substack version opens with where things ended up (his mother's worries solved) before the original hook.
- UTMs switch to `utm_source=substack&utm_medium=post&utm_campaign=waitlist&utm_content=<slug>-top|end`.
- **No "Originally published at…" back-link.** Web only.
- Build the paste HTML the same way as the blog HTML (`scripts/blog/build_html.py`), check ₹ and quotes in the editor preview.
- Approval required before publishing. After it is live, notify the review bot.

## Blog → X Article

Files on the box: `crosspost/postNN_xarticle.md` (text), `postNN_xarticle_content_state.json` (the editor's block structure, used to paste reliably), `make_postNN_x_cover.py` (cover), and the `x-article-cover` skill.
- Text: the blog post with an X-friendly lead (post 8 opens with the one-paragraph answer), UTMs `utm_source=x`.
- **Cover: exactly 5:2**, 3000×1200 preferred (1500×600 minimum), JPG/PNG under 5 MB. Keep every word inside a 10% side / 12% top-bottom safe zone (the timeline card may crop to 2:1). Same look as the blog thumbs: notebook grid, ink and red, Josefin Sans two-line title. The cover must **name what is being quit** ("Job" or "9to5" visible), not only an abstract phrase.
- Generate with [scripts/crosspost/make_x_cover.py](../scripts/crosspost/make_x_cover.py) (copy and change the illustration and two lines). It writes the upload file, a PNG, a preview sheet (5:2 header, 2:1 card crop, phone width) and a safe-zone debug image; never upload the preview or the debug image.
- Articles need X Premium. Pallav logs in himself (Google SSO). Leave it as a draft and send him the draft link unless he has approved this specific cover and text for publishing. Never publish as a side effect of a cover swap.
- After it is live, check the article page and the timeline card crop, then notify the review bot.

## Reel → Substack Note and social

Covered in [docs/reels.md](reels.md) step 9 and [substack-notes.md](substack-notes.md). The same approved caption family is used everywhere: Instagram/LinkedIn caption, Threads text, Note.

## Consistency checks for any cross-post

- [ ] Same facts and numbers as the source; nothing new added without a source
- [ ] UTMs changed to the destination's `utm_source`
- [ ] CTA appropriate to the destination (reels: "in bio"; text platforms: quit9to5.in link)
- [ ] ₹, ÷ and quotes render correctly in the destination editor
- [ ] Approved by Pallav (except the beehiiv blog itself)
- [ ] Review bot notified once live

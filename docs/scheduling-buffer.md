# Scheduling with Buffer

Buffer schedules the Instagram, LinkedIn and Threads posts. Use the Buffer MCP connector (tools `get_account`, `list_channels`, `create_post`, `get_post`, `list_posts`, `edit_post`, `delete_post`) or the Buffer API with `BUFFER_ACCESS_TOKEN`.

**Gate:** never call `create_post` without Pallav's explicit pick of the item, the channels and the slot, and his word "schedule". See [rules/approval-gates.md](../rules/approval-gates.md).

## Account and channels

- Organisation: "Quit 9to5" (`BUFFER_ORG_ID`, from `get_account`). Tell the user which organisation you are using.
- Channels (IDs from `list_channels`; never guess or reuse IDs from memory):

| Channel | Placeholder | Scheduling |
|---|---|---|
| Instagram @quit9to5book | `BUFFER_CHANNEL_INSTAGRAM` | automatic Reels (since 21 Nov 2026: the voiceover is on the video, Pallav does not add music) |
| LinkedIn Page "Quit 9to5" | `BUFFER_CHANNEL_LINKEDIN` | automatic |
| Threads @quit9to5withpallav | `BUFFER_CHANNEL_THREADS` | automatic |

- **X is not a Buffer channel any more.** Do not schedule X through Buffer.
- There is no Substack channel in this workflow's Buffer; Substack Notes are scheduled in the browser ([substack-notes.md](substack-notes.md)).

## Limits

- **Free plan: 10 scheduled posts per channel** (not 10 in total; Pallav confirmed this on 22 Nov 2026). With two reels a day on three channels, that is about five days of queue per channel. Count each channel's queue before adding.
- **Threads: 500 characters** per post. Use the reel's `THREADS.txt`, which is written to fit; count characters, not bytes (₹ is one character).
- Instagram needs an image or video asset; a single video in the feed must be `type: "reel"`.
- Media URLs must be direct, publicly downloadable files (not share pages). Videos: the Drive download URL (see below). Card images: a public image host (the box uses iili.io).

## Cadence

- Two reel slots a day: **14:00 and 19:00 IST** (Asia/Calcutta, UTC+05:30). On some days a carousel replaces the 19:00 reel.
- Same slot on all three channels for a given item.
- Build `dueAt` with the `+05:30` offset, e.g. `2026-11-24T14:00:00+05:30`. Use `get_account`'s `currentTime` as "now"; `dueAt` must be in the future.
- Use `mode: "customScheduled"` with an explicit `dueAt` (the approved slot), not `addToQueue`.

## Payloads (reel)

Video URL for all three: `https://drive.usercontent.google.com/download?id=<DRIVE_FILE_ID>&export=download&confirm=t`, after you have verified with `curl` that its sha256 equals the local posting copy.

Instagram:
```json
{
  "channelId": "<BUFFER_CHANNEL_INSTAGRAM>",
  "schedulingType": "automatic",
  "mode": "customScheduled",
  "dueAt": "2026-11-24T14:00:00+05:30",
  "text": "<contents of CAPTION.txt>",
  "assets": [{ "video": { "url": "https://drive.usercontent.google.com/download?id=<DRIVE_FILE_ID>&export=download&confirm=t" } }],
  "metadata": { "instagram": { "type": "reel", "shouldShareToFeed": true, "isAiGenerated": false } }
}
```

LinkedIn: same `assets`, `text`, `dueAt`, `schedulingType: "automatic"`, `mode: "customScheduled"`, with `channelId` = `BUFFER_CHANNEL_LINKEDIN` and no Instagram metadata.

Threads: same `assets` and `dueAt`, `channelId` = `BUFFER_CHANNEL_THREADS`, `text` = contents of `THREADS.txt` (500 characters or fewer). Threads does not support the reel type; the video goes as a normal post.

Card or carousel image posts use `assets: [{ "image": { "url": "<public image URL>", "metadata": { "altText": "<what the card says>" } } }]`; on Instagram set `metadata.instagram.type` to `"post"` and `shouldShareToFeed: true`.

## After scheduling

1. `get_post` each new post: status `scheduled`, `dueAt` correct, the media URL correct, the text intact (₹ and line breaks).
2. Report to Pallav: item, channels, slot, and that all were re-read.
3. Log each item in the post log (`POST_LOG_CSV`, mirrored to the Google Sheet `POST_LOG_SHEET_ID`): `date_scheduled_IST, slot, template, card_file, key_line, caption, theme_tags, channels, buffer_post_ids, status, image_url, overlap_flags`. Note the link-in-5 counter state in `overlap_flags` (e.g. "NO waitlist link: post 2 of 5 after reset").
4. When the posts go live, update the status and notify the review bot.

## The no-repeat and link-in-5 gates

- Before proposing anything, search the post log's `key_line`, `caption` and `theme_tags`: the same sentence already sent or scheduled is out; the same theme within 3 days is out; the same personal story at most once per day.
- Link-in-5: every fifth post carries the waitlist link in its caption (plain `https://quit9to5.in` on LinkedIn and Threads); the counter then resets. Reels count as posts but never carry a URL (their CTA is "in bio").

## Daily runway check

The box runs a daily 8:02 PM IST check of the Buffer queue that flags empty slots. It reports; it never fills slots without picks. If you replicate it, keep it report-only.

## Undoing mistakes

Buffer posts publish automatically and cannot be unsent once live. If a scheduled post is wrong, tell Pallav, then `edit_post` or `delete_post` with his OK.

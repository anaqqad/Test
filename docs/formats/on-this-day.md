# Format: "On This Day in Black History" (Facebook posts) — added 2026-10-15 by the owner

A short Facebook post (photo post, not a reel) about one or two things that happened to Black people
on today's date in history. Quick to make, can go out daily next to the reels.

## Rules
- Pick 1–2 events that happened on **today's month and day** (any year). Prefer: a famous name with a
  surprising fact, or a forgotten event; a real photo of the person or event.
- Every fact needs **two independent reliable sources** (Library of Congress, National Archives, NPS,
  Smithsonian, universities, museums, Britannica, reputable newspapers). If the exact date is disputed,
  don't use the event.
- Images: public domain or CC0 only, credited at the end. No graphic violence.
- No unverified quotes. Label legends as legends.
- Same voice as the reels: short sentences, clear, respectful.

## Image
1080x1350 (4:5) for the feed: the archival photo, a dark band with "ON THIS DAY" + the date in gold
(e.g. "OCTOBER 16") and the year big, page name small at the bottom. One image per event (carousel if two).
Script to build it: to do (reuse `scripts/make_episode_cover.py` style).

## Post template
```
ON THIS DAY: [Month Day], [Year]

[Hook line: the surprising fact in one sentence.]

[2–4 short paragraphs: who, what happened, why it mattered.]

[Optional second event:]
Also on this day, [Year]: [one or two sentences].

Did you know this happened on [Month Day]?

Researching and editing these stories takes real time and effort. If you value these stories, please support our page so we can keep bringing them to light. Thank you!
https://ko-fi.com/theblackhistoryroom

Sources: [Source 1]; [Source 2].
Image: [title, year, collection], public domain.

#OnThisDay #BlackHistory #[Name] #HiddenHistory
```

## Files
`publish/onthisday/YYYY-MM-DD.md` (post text + sources) and `publish/onthisday/YYYY-MM-DD.jpg`.
The website's "This Week in Black History" section can reuse the same entries.

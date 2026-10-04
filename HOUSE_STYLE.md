# House style: "Darkroom & Ledger"

This is our own visual identity. `VIDEO_STYLE_BLUEPRINT.md` describes the *reference* channel's formula
(story structure, pacing, cut rhythm). Its colours, fonts and card layouts describe that channel and
must **not** be reused. Every new video uses the components below instead.

The idea: we are researchers working through an archive. **Photographs** are examined on a light
table as frames of film. **Facts** are written up in a field ledger. Both get marked up with the same
red grease pencil, so the pencil mark is the thread that ties the channel together.

## Tokens
| Token | Value | Use |
|---|---|---|
| Light table | `#121212`, glow `#202020` | photo card background |
| Film rebate | `#050505`, edge print `#8a7a58` | the strip around photos |
| Ledger paper | `#f1eee6`, grid `#d5dcd7` / `#b4c3bc` (24 px / 120 px) | all data and document cards |
| Ink | `#171717`, soft `#5f5b54` | text on paper |
| Grease pencil | `#e0442e` | **the only accent**: circles, crop corners, ticks, underlines, bars, routes |
| Light text | `#ece9e1`, soft `#9a968e` | text on dark |
| Headline font | Barlow Condensed 700, UPPERCASE | titles, figures, place names |
| Label font | IBM Plex Mono 400/500 | dates, captions, sources, file numbers, tags |
| Quote font | IBM Plex Serif | quoted words only |

Never: navy panels, gold rules, Baskerville/Inter (the reference's look), kraft tags, paper clips or
dark-wood desks (other channels' looks), emoji, stock icons, drop-shadowed glossy cards.

## 1. How we show a photograph: the contact frame (`remotion/src/photo.tsx`)
- A vertical 35 mm strip is pulled up across the dark light table (enters from below in ~0.7 s with a
  small overshoot) and stops on one frame. Sprocket holes run down both edges. Neighbouring frames are
  unexposed, and an edge print gives the frame number.
- Red crop corners draw on around the picture at about 0.7 s. An optional hand-drawn circle around one
  detail draws on at about 1.3 s, and should point at what the narration names.
- The photo pushes in slowly (1.00 to 1.07) toward a focus point.
- The caption column sits beside the strip: `FR. 07` in red, then the title (2–5 words, caps), the
  caption (where, when, what, in mono) and the source (photographer · archive · call number). The strip
  alternates sides (left/right) from one photo to the next.
- It exits by advancing the film upward. Back-to-back photos read as advancing frames of one roll.
- Hold 4–8 s. Use 8–12 photos per 8–9 minutes. Photos must be real archive images. If a photo stands
  in (a different place or date), the caption says exactly what it shows.

## 2. How we show data and documents: the field ledger (`remotion/src/ledger.tsx`)
Full-frame graph paper with a red double margin rule. A paper plate in the top-left carries the file
number (`FILE 04 — DARKNESS BY LAW`, mono) and the headline (caps, a claim not a label). The source
is always typed at the bottom.
- **LedgerBars**: comparisons. Hatched grease-pencil bars with a wobbly outline grow from the margin.
  The figure is set big in caps at the bar end, with a mono note (dates, units) under it. Use 2–3 bars.
- **LedgerTimeline**: dated rows, read top to bottom. The date is in mono and the event in caps. A red
  tick is drawn in the margin as each row appears. Use 3–5 rows.
- **LedgerQuote**: one quoted passage in serif, with the key words underlined in grease pencil and the
  speaker in mono. Quote only what the source says. Mark any cuts with `…`.
- **LedgerClipping**: a newspaper report as torn newsprint pinned slightly rotated on the ledger, with
  a red bracket in the margin. Label it "as quoted in …" when it is reconstructed from a book.
- **LedgerMap**: state lines in thin ink, with the region of interest hatched. The route is drawn in
  grease pencil, stops in caps, and distances or modes in red mono.
- Hold 7–12 s, never two ledger cards back to back. Use 5–7 per video.

## 3. On-footage overlays (`remotion/src/overlays.tsx`)
- **Slug**: dates, names and calls to action. A black tab wipes in from the left with a red square and
  caps title, and a light mono strip under it for the detail. Use it for dates that turn the story, an
  alias, the silent subscribe card (~36 % in) and the comment request (~20 s before the end).
- **ContextTag**: for stand-in or dated footage, typed on in mono:
  `● [ STAND-IN · BUS TRAVEL, UNITED STATES, 1950S ]`. Shown for 4.5 s at the start of a footage block.

## Rhythm (unchanged from the blueprint's measurements)
Footage cut on narration words every 3–5 s. A photo or ledger card every ~25–35 s. Cards and photos
are the only dissolves.

# LIFELINGS: channel bible v1

> **"Life as…" → a funny 60–90 s animated story → upload.**
> Tagline: **Every life is a little ridiculous.**

Contents
1. [Reference analysis](#1-reference-analysis)
2. [Channel positioning](#2-channel-positioning)
3. [30 channel names](#3-30-channel-names)
4. [Top 10 ranked](#4-top-10-ranked)
5. [Final name: Lifelings](#5-final-name-lifelings)
6. [Brand identity](#6-brand-identity)
7. [The characters](#7-the-characters)
8. [Profile picture](#8-profile-picture)
9. [The first five videos](#9-the-first-five-videos) (full scripts, storyboards, prompts → `episodes/`)
10. [Global animation and editing rules](#10-global-animation-and-editing-rules)
11. [Thumbnail and title strategy](#11-thumbnail-and-title-strategy)
12. [Repeatable production template](#12-repeatable-production-template)
13. [Idea bank: 60 future episodes](#13-idea-bank-60-future-episodes)

Brand files (already made, in `brand/`; regenerate with `python3 lifelings/brand/draw_cast.py`):

| File | What it is |
|---|---|
| `brand/character_sheet.png` | The cast built on one shared body: Nobo, Lulu, Mama, Mom (alt), Dad, Boss, Bestie, NPC |
| `brand/expressions.png` | The 8 faces |
| `brand/pfp.png` | Ready-to-upload profile picture (1024×1024). `pfp_small_test.png` shows it at 98/48/30 px |
| `brand/caption_style.png` | 9:16 style frame: title tag, caption style, Shorts safe zones |
| `brand/thumbnail_mock.png` | 16:9 thumbnail layout example |
| `brand/*.svg` | Vector sources. Every body part is its own `<g>`/path, so they double as a cut-out rig |
| `brand/fonts/` | Lilita One + Baloo 2 ExtraBold (both free, SIL Open Font License) |

---

## 1. Reference analysis

Source: *"Life as a Muslim girl."* (23.8 s, 854×480, 30 fps, stereo AAC). I watched it frame by frame and
measured the cuts and the audio.

### Shot list (measured)

| # | Time | On-screen text | Visual |
|---|---|---|---|
| 1 | 0.0–7.1 s | Title "Living in the **Middle east**" → small "As a Muslim girl that used to live there" → yellow stamp "NOT ALL MIDDLE EAST COUNTRIES" | Niqab-wearing character, centre, cropped at the waist, over a street photo with old cars |
| 2 | 7.1–10.2 | "Getting out alone feels like a crime even for strangers." + tiny "WHO ARE YOU GOING OUT WITH?!" | Same character, side-on, empty square; a hand-drawn squiggle "noise" mark appears |
| 3 | 10.2–13.4 | "Forced to only wear black which makes you feel like burning alive." | Eyes go wide → flame sprites appear on her → a real meme photo (screaming face in fire) is cut in over her |
| 4 | 13.4–16.7 | "Need a mahram just to get outside." | Man in a white thobe, outline-only, face cropped off the top of frame, standing next to her |
| 5 | 16.7–20.6 | "Some men will try to peek at your face when you try to take a breath." | She turns away, hand on veil, alley with graffiti |
| 6 | 20.6–23.8 | "Harassment, even when they can't see anything but your eyes and hand." | Narrow alley, she looks back over her shoulder |

### Breakdown

| Element | What the reference does |
|---|---|
| **Visual style** | Flat MS-Paint-style drawing pasted onto ordinary phone/stock street photos. No integration (no shadow, no colour match), which is part of the meme look. |
| **Character design** | Almost a silhouette: a black shape with a beige eye slit and Wojak-style heavy-lidded eyes. Flat beige hands. Readable because the silhouette is so simple. |
| **Animation** | Close to none. One static drawing per shot, a 2nd drawing for an expression change (tired eyes → wide eyes), overlay sprites (fire, squiggle) that pop on. No lip-sync, no walk cycles. |
| **Backgrounds** | Real, unremarkable, eye-level street photos (alleys, sidewalks, old cars). They set place cheaply and make the cartoon funnier by contrast. |
| **Editing pace** | Title holds 7 s (too long), then a new shot every 3.1–3.9 s, very regular. One idea per shot. |
| **Text** | Big white bold sans with a black outline for the title; small white top-left sentence captions for each point (hard to read on a phone); a yellow cartoon-font stamp as a disclaimer. |
| **Humour** | Dark irony plus literal visual exaggeration ("burning alive" → actual flames → a meme cut-in). A list of grievances more than jokes. |
| **Story structure** | Listicle: title + 5 bullet points. No arc, no payoff, no ending. It just stops, which makes it loop. |
| **Hook** | The identity title ("Living in the Middle East as a Muslim girl") does all the work: insiders feel seen, outsiders are curious, and some people want to argue. |
| **Scene duration** | ~3.3 s average after the title. |
| **Camera** | Static. No zooms or pans. |
| **Sound** | No voiceover. Three impact hits under the title (0–2.5 s), then a steady melancholic music loop (a pulse every ~0.68 s) for the rest. The text carries the content and the music carries the mood. |

### Why it works
1. **Identity in the title** = instant self-selection. "That's me" or "Is that true?" are both clicks.
2. **Comment bait.** The "NOT ALL…" stamp both defends and provokes, and debate in the comments feeds the algorithm.
3. **Under 24 s and no ending**, so it loops and the watch time can pass 100 %.
4. **Literal visual metaphors** (burning alive → fire) are the only real jokes, and they land.
5. **Zero friction to read**: one sentence per shot, held long enough.

### Why it's easy to produce at scale
One character drawing with 3–4 variants, free photos, one sentence per shot, one music track, no voice, no
animation. That's under an hour per video in CapCut.

### What we copy (format level) vs. what we make original

| Copy the *format* | Make it *ours* |
|---|---|
| Drawn character pasted on real photos | Our own cast (Nobo & co.), our own line/colour system, contact shadows, slightly softened photos so the cartoon pops |
| One idea per shot, 2–4 s rhythm | A real story arc with escalation and a punchline, 60–90 s, not a list that just stops |
| Identity in the title | A **"LIFE AS…" yellow name-tag** title that stays on screen all video and is the brand's signature |
| Literal visual metaphors + meme-style cut-ins | Our own drawn props/stickers instead of borrowed meme photos (copyright-safe, consistent) |
| Big readable text | Large centred word-chunk captions (not tiny top-left sentences) + a deadpan first-person voiceover |
| Minimal animation | Same minimalism, plus 6 cheap signature moves (tag slap, curl boing, pop-in, punch-in, slide, shake) |
| Loopable ending | Endings written to loop back into the first line on purpose |
| — | **Tone: relatable, affectionate, "laughing with, not at."** No grievance or shock framing. Better for ads, brand deals, sharing, and long-term trust |

Do **not** reuse: the niqab/thobe drawings, their fonts/caption layout, their photos, the meme cut-in image, or
their audio.

---

## 2. Channel positioning

**Lifelings is a short-form animated sketch channel where every episode drops you into someone else's life
for 60–90 seconds.** Promise to the viewer: *you'll see yourself, or someone you need to send this to.*

**Decisions**
- **Format:** 9:16 vertical, 1080×1920, 30 fps, 60–90 s. YouTube Shorts now allows up to 3 min, so these
  are Shorts and get Shorts distribution. Cross-post the same file to TikTok, Instagram Reels and Facebook Reels.
- **Language:** English VO + English captions first. Secondary characters "speak" in gibberish blips with
  their words in speech bubbles, so later dubs (Arabic, French, Spanish) only need one re-recorded voice
  track plus translated captions. YouTube's multi-language audio tracks make this cheap.
- **Voice:** one deadpan first-person narrator (the protagonist's inner voice). Recommended: record it
  yourself on a phone in a closet. It's authentic, free and can't be copied. AI TTS is a fallback; any paid
  voice service needs your sign-off first.
- **Cadence:** 3 videos/week (Mon/Wed/Fri), produced in weekly batches. After 30 videos, double down on the
  top 3 pillars by retention.
- **Monthly long-form:** a 16:9 "Life as… compilation" (8–10 episodes, 10–14 min) for watch-hours and
  long-form recommendations. Re-frame the vertical episodes on a branded 16:9 background with the tag on the left.

**Five content pillars** (rotate so the channel never feels one-note; ratio ~2 universal : 1 cultural)

| Pillar | Examples | Why |
|---|---|---|
| **Personality** | introvert, overthinker, people-pleaser, night owl | Largest audiences, extremely shareable |
| **Family roles** | eldest daughter, middle child, only child, kid of immigrant parents | "Tag your sibling", the biggest share driver |
| **Culture & place** | Ramadan in Europe, Moroccan abroad, tourist in Paris, Arab at a wedding | Built from insider knowledge you actually have. Loyal niche communities |
| **Life stage & money** | broke student, first job, new parent, 30 and single | Broad, timeless, evergreen |
| **Jobs** | waiter, nurse, teacher, IT guy, delivery rider | Every job has a community that shares |

**Tone rules**
1. Punch **up** or **inward**, never down. The joke is the *situation*, never the identity.
2. Every culture episode is written (or checked) by someone from that culture, with specific detail and no stereotypes.
3. The protagonist always gets the last laugh or a warm beat. People share things that make them feel seen, not things that make them feel mocked.
4. **Tragedy is not punchline material.** "Life as a kid in Gaza" doesn't fit the comedy engine. If you ever
   make it, make it a separate, sincere register: kids' football, school jokes, the humour people keep under
   pressure. Don't schedule it in the first 50 videos, and expect limited ads.

---

## 3. 30 channel names

Rejected on purpose: **Oddlings** (too close to TheOdd1sOut), anything with "Noggin" (Life Noggin), anything
with "Wojak", and "Life As" alone (unsearchable, ungoogleable).

| # | Name | Note |
|---|---|---|
| 1 | **Lifelings** | "Life" + "-lings" (little beings) |
| 2 | **Plainfolk** | Ordinary people, plain drawings |
| 3 | **Lifeslice** | Slice of life, literally |
| 4 | **Doodle Lives** | Describes the product |
| 5 | **Odd Lives** | Short, but generic |
| 6 | **Pocket Lives** | Tiny lives you carry around |
| 7 | **Beanfolk** | Our characters have bean heads |
| 8 | **Tiny Lives** | Cute, broad |
| 9 | **Lifestamp** | Echoes the name-tag device |
| 10 | **Tagged** | Name-tag device; hard to search |
| 11 | **Inkfolk** | Line-art people |
| 12 | **Livesketch** | Sketch = drawing + comedy sketch |
| 13 | **Wobbly Lives** | Matches the wobbly line |
| 14 | **Mundanes** | Everyday people; slightly negative |
| 15 | **AsLife** | Inverts "Life as"; awkward to say |
| 16 | **Lifeloop** | Loopable shorts; sounds like an app |
| 17 | **Being Bean** | Cute, close to "Mr. Bean" (risk) |
| 18 | **Paper Lives** | Cut-out look |
| 19 | **Every Life** | Mission statement; generic |
| 20 | **Lifeskits** | Life + skits |
| 21 | **Dotface** | Our pupils are dots; doesn't say "life" |
| 22 | **Humble Beans** | Warm, food-ish |
| 23 | **Side Lives** | "Side character" energy |
| 24 | **Daily Lore** | Gen-Z "lore" slang; may age |
| 25 | **Smallfolk** | Fantasy undertone (Game of Thrones term) |
| 26 | **Lifegag** | Clear, a bit cheap-sounding |
| 27 | **Okay Lives** | Deadpan; low energy |
| 28 | **Sketchy Lives** | Funny double meaning; "sketchy" is negative |
| 29 | **Livd** | Short, unpronounceable to some |
| 30 | **Nobo & Friends** | Character-led; locks the brand to one mascot |

## 4. Top 10 ranked

| Rank | Name | Memorable | International | Expandable | Searchable | Why it ranks here |
|---|---|---|---|---|---|---|
| 1 | **Lifelings** | ★★★★★ | ★★★★★ | ★★★★★ | ★★★★★ | Owns "life", names the characters and the fans, no existing major channel found |
| 2 | **Plainfolk** | ★★★★ | ★★★★ | ★★★★★ | ★★★★ | Strong but "folk" reads as music to some |
| 3 | **Lifeslice** | ★★★★ | ★★★★ | ★★★★ | ★★★ | Clear meaning; close to the generic phrase "slice of life" |
| 4 | **Doodle Lives** | ★★★★ | ★★★★★ | ★★★ | ★★★ | Describes the look, but two common words |
| 5 | **Pocket Lives** | ★★★★ | ★★★★ | ★★★★ | ★★★ | Lovely image, less punchy |
| 6 | **Beanfolk** | ★★★★ | ★★★ | ★★★★ | ★★★★ | Ties to the bean heads; "folk" again |
| 7 | **Livesketch** | ★★★ | ★★★★ | ★★★★ | ★★★★ | Clever double meaning; "live" vs "liv" pronunciation clash |
| 8 | **Lifestamp** | ★★★ | ★★★★ | ★★★★ | ★★★★ | Fits the tag device; sounds like a SaaS product |
| 9 | **Tiny Lives** | ★★★★ | ★★★★★ | ★★★ | ★★ | Very generic to search |
| 10 | **Odd Lives** | ★★★★ | ★★★★★ | ★★★ | ★★ | Short; too generic, and "odd" is near TheOdd1sOut |

## 5. Final name: **Lifelings**

**Handle:** `@lifelings` (fallbacks: `@lifelingstoons`, `@thelifelings`). Before you commit, check the
handle on YouTube, TikTok and Instagram, and check `lifelings.com/.tv`. My web search found no existing
animation channel by that name, but small or new accounts aren't always indexed.

Why it's #1:
1. **It contains the format.** "Life" is in the name, so "Life as… | Lifelings" reads like a series title.
2. **It names the characters.** Nobo, Lulu and Mama are *Lifelings*. "-ling" means a small creature, which matches small bean-headed people.
3. **It names the community.** Fans can be "Lifelings" ("Hi Lifelings, who should I be next?").
4. **It's culture-neutral and easy to say** in English, French, Arabic and Spanish. Three syllables, no tricky sounds.
5. **It scales**: spin-offs ("Lifelings Explain", "Lifelings at Work"), merch (a Nobo plush with a blank name
   tag you can write on), and a kids-friendly version if ever wanted.

---

## 6. Brand identity

### Signature device: the yellow name tag
Every Lifeling wears a small yellow name tag that says **who they are in this video** (ME, NEW, MAMA, BOSS,
FASTING…). The same yellow tag appears:
- **0:00 "tag slap":** a big tag **LIFE AS A ___** slaps onto the top of the frame with a *thwack* (6 frames, slight overshoot). It **stays on screen the whole video**, so a viewer who scrolls in mid-video knows what they're watching. The reference only shows its title for 7 s.
- **On the chest:** tags change mid-episode as a joke engine (episode 2 runs on it).
- **Thumbnails, channel banner, profile picture:** the tag is the logo.
- **End card:** Nobo's tag flips to **"?"**, with the VO line "Who should I be next?" pointing to the pinned comment.

### Palette

| Token | Hex | Use |
|---|---|---|
| Ink | `#151515` | All outlines, text outlines |
| Paper | `#FFF8EC` | Brand backgrounds, end card |
| Tag Yellow | `#FFD23F` | Name tags, title tag, highlighted caption words |
| Signal Blue | `#3D7BFF` | Profile picture background, banner, links |
| Nobo Coral | `#FF6B4A` | Nobo's hoodie, the brand's "hero" colour |
| NPC Grey | `#9AA0A6` | Extras / crowds |
| Skin S1–S5 | `#FFE0C7 #F2C29B #D9A273 #A86B45 #6B4329` | Flat skin tones, no shading |

### Type
- **Lilita One** for title tags, chest tags and thumbnails. Always on a yellow tag, black text, rotated −3° to −5°.
- **Baloo 2 ExtraBold** for captions: white, 16 px black outline, 70–80 px at 1080 wide, max 2 lines,
  2–5 words per chunk, one key word per caption in Tag Yellow.

### Backgrounds
Real photos (yours, Pexels/Unsplash, or AI-generated), shot at eye level and empty in the lower centre.
Treatment, always the same: **saturation −20 %, slight blur (2 px), contrast −5 %**. The cartoon stays the
sharpest, most saturated thing on screen. Characters always get a soft oval **contact shadow**, so they stand
*in* the photo rather than float on it.

### Sound identity

| Cue | Sound | When |
|---|---|---|
| Tag slap | Short paper/cardboard *thwack* | 0:00 every video, and every chest-tag change |
| Curl boing | Rubber-band *boing* | Nobo's curl straightens: shock |
| Curl droop | Descending slide-whistle (0.4 s) | Curl wilts: disappointment |
| Pop | Bubble *pop* | Captions/props/speech bubbles appearing |
| Gibberish | Pitched "blip-blop" voice | Any character except the narrator speaking |
| Record scratch | Vinyl scratch, then silence | Before the punchline |
| End sting | 3-note ukulele/kalimba motif | End card, every video |

**Music:** one quirky bed per episode (ukulele, pizzicato, lo-fi, light funk) from the **YouTube Audio
Library** or another royalty-free source you own a licence for. Avoid copyrighted/trending tracks. Shorts
over 1 minute that pick up a Content ID claim can be blocked, and ours are all over 1 minute.

---

## 7. The characters

See `brand/character_sheet.png` and `brand/expressions.png`.

### Main character: **Nobo**
"Nobo" (from *nobody*) is the everyman, and he plays the lead in most episodes. His tag changes with the
episode's identity.

| Trait | Spec |
|---|---|
| **Silhouette** | Big bean head + tiny sack body + one curly hair strand on top. Recognisable as a black silhouette at 30 px. |
| **Proportions** | 2.2 heads tall; the head is ~55 % of total height. Body as wide as the head's lower half. Stubby legs, black oval shoes. |
| **Head** | Bean/egg shape, slightly wider at the top, slightly lopsided. Bald except the curl. No ears, no nose. |
| **Eyes** | Two large white **saucer** ovals with small black dot pupils. This is the main difference from Wojak's narrow, baggy slits. Expression comes from the lids (a flat skin-coloured lid cutting across the eye) and pupil size and position. |
| **Mouth** | One line by default. Opens into a dark-red shape only for shock or laughter. |
| **The curl** | Nobo's emotion antenna, the signature gag: **straight up + boing** = shock; **drooped** = sad; **spinning** = overwhelmed; **heart-shaped** = in love (rare, save it). |
| **Clothing** | Coral hoodie (no logos), navy trousers, black shoes, yellow name tag on the chest. |
| **Line** | Uniform thick black outline (~2 % of character height), a slight hand-drawn wobble, flat colours, no gradients, no shading. |
| **Arms/hands** | Noodle arms with round mitten hands (no fingers). Any pose is just a new curve, so they're easy to animate. |

### Expression system (8 faces; only the eyes, brows and mouth swap)

| Face | Eyes | Mouth | Use |
|---|---|---|---|
| **Deadpan** (default) | 40 % lids, centred pupils | flat line | Narration, the "this is my life" look at camera |
| **Happy** | closed arcs + blush | open smile | Rare, so it means something |
| **Panic** | full eyes, tiny pupils, angry-worried brows | open oval + sweat drop | Escalation |
| **Side-eye** | 40 % lids, pupils hard right + sweat | wonky line | Awkward moments (the most-used face) |
| **Sad** | tilted lids, pupils low, tears | frown | Fake drama |
| **Shocked** | eyes enlarged 115 %, pin pupils | tiny "o" | Punchline reactions, plus curl boing |
| **Smug** | 50 % tilted lids, pupils side | crooked smirk | Small victories |
| **Dead inside** | no pupils, grey wash over the face | wobbly line | The bottom of the story arc |

### Pose library (draw once, reuse forever)
`P01 idle` · `P02 wave` · `P03 facepalm` · `P04 shrug` · `P05 point` · `P06 phone` (P01–P06 are already in
the SVG rig) · `P07 sit at desk (3/4)` · `P08 blanket burrito in bed` · `P09 walk (2 frames)` · `P10 hold
object with both hands` · `P11 arms up celebrate` · `P12 flopped face-down` · `P13 tiptoe sneak (2 frames)` ·
`P14 eating` · `P15 typing on phone (thumbs blur)`.

Any pose × any face × any character = thousands of combinations with no new drawing.

### Secondary cast (same body kit, different head piece and colours)

| Character | Look | Role / personality |
|---|---|---|
| **Lulu** | Black bob with side fringe, teal top, skin S3 | Default female lead. Dry wit, the competent one |
| **Mama** | Purple hijab, green top, skin S3, permanent smug face | The universal mum. Loving, loud, always has a task for you. **Likely breakout character; give her catchphrases** ("Just five minutes." "Are you eating well?") |
| **Mom (alt)** | Brown bun, pink top, skin S1 | Mum for non-Muslim family episodes |
| **Dad** | Three hairs, round glasses, mustache, white shirt, skin S4 | Shrugs, says "too much salt" about everything |
| **Boss** | Comb-over, grey suit, red tie | Speaks fluent corporate |
| **Bestie / "Bro"** | Blue cap, yellow top, skin S5 | Over-enthusiastic extrovert friend |
| **NPCs** | All grey, half-lid eyes, **no tag** | Crowds, strangers, coworkers. They react only with their eyes (sliding to look at the protagonist). An NPC who becomes important **gets a tag** (e.g. GARY in episode 4), which is a joke of its own |

**Situation rules:** at work, add a lanyard to the tag. Night scenes get a blue tint on the character (multiply
layer at 15 %). Characters keep the same face style with any headwear (hijab, cap, chef hat, graduation cap);
the body never changes.

---

## 8. Profile picture

**Already made:** `brand/pfp.png`: Nobo head-and-shoulders, side-eye, sweat drop, on a Signal Blue circle,
wearing a name tag that just says **"?"**. That means "who will I be next?", which is the whole "Life as…"
concept in one symbol. It's tested legible at 48 px (`brand/pfp_small_test.png`). Use this vector version:
it will match the videos exactly.

If you want an image-model variant (e.g. a painterly banner version), use this prompt:

```
Square 1:1 YouTube profile picture. A single simple hand-drawn cartoon character, head and shoulders,
centred, filling 80% of the frame: a large bald bean-shaped head (wider at the top) with one small curly
hair strand sticking straight up, two big round white "saucer" eyes with small black dot pupils looking
sideways with heavy half-closed eyelids (awkward side-eye), a tiny wobbly single-line mouth, no nose, no
ears, one light-blue sweat drop on the temple. Wearing a plain coral-orange hoodie (#FF6B4A) with a small
bright-yellow rectangular name tag on the chest showing only a black question mark "?". Thick uniform black
marker outlines, slightly wobbly hand-drawn line, completely flat colours, no shading, no gradients.
Solid flat royal-blue circular background (#3D7BFF). Funny, deadpan, meme-comic style, very readable at
tiny sizes. No other text, no logo, no watermark, no Wojak, no realistic features.
```

**Banner (2560×1440, safe area 1546×423 centred):** Paper background, the whole cast in a line
(`character_sheet` order), each with their tag, and a big yellow tag **"LIFE AS… EVERYONE."** with a
small "New episodes Mon · Wed · Fri" beneath.

---

## 9. The first five videos

Release order is chosen so the first three are the broadest; the culture episode lands once the channel
has a baseline audience; and the finale has the strongest loop.

| # | File | Title | Lead | Story engine |
|---|---|---|---|---|
| 1 | [`episodes/01-introvert.md`](episodes/01-introvert.md) | Life as an Introvert | Nobo | **One event spirals** (a party invite) |
| 2 | [`episodes/02-eldest-daughter.md`](episodes/02-eldest-daughter.md) | Life as the Eldest Daughter | Lulu | **Job titles** (the name tag keeps changing) |
| 3 | [`episodes/03-broke-student.md`](episodes/03-broke-student.md) | Life as a Broke Student | Nobo | **Survival game HUD** (money counter) |
| 4 | [`episodes/04-ramadan-in-europe.md`](episodes/04-ramadan-in-europe.md) | Life as a Muslim in Europe During Ramadan | Nobo | **Countdown clock** (iftar timer) |
| 5 | [`episodes/05-gen-z-first-job.md`](episodes/05-gen-z-first-job.md) | Life as a Gen Z at Their First Job | Nobo | **Translation subtitles** (corporate → real) |

Each episode file contains: title + alternates, hook, full script, scene-by-scene storyboard (duration,
action, background, expression, dialogue, on-screen text, camera, sound), image-generation prompts for
every background and special asset, animation instructions, editing instructions, thumbnail, and a
virality breakdown.

Shared across all five, so they feel like one channel: same cast and rig, tag slap at 0:00, persistent title
tag, the same caption style, deadpan VO, gibberish for other characters, the curl as the emotion meter, a
record scratch before the main punchline, a loop or warm-beat ending, and the "?" end card.

---

## 10. Global animation and editing rules

**Tools:** CapCut Desktop (free) is enough. DaVinci Resolve (free) if you want more control. Keep each
character as **separate PNG layers** (head, eyes, mouth, body, each arm) exported from the SVGs, or as
whole-pose PNGs if you prefer simplicity.

### The six moves (the whole animation vocabulary)
| Move | How | Frames @30 fps |
|---|---|---|
| **Breathe** | Character scale Y 100 → 101.5 → 100 %, anchored at the feet, looping | 36-frame loop |
| **Pop-in** | Scale 0 → 112 → 100 % (props, bubbles, captions) | 6 frames |
| **Tag slap** | Tag drops from 160 % scale + 15° rotation to 100 %/−4°, plus a 4-frame 6 px screen shake | 6 + 4 |
| **Punch-in** | Hard cut to 115–130 % scale on the character's face on every punchline | 0 (cut) |
| **Slide** | Character enters/exits from the frame edge, ease-out | 8 frames |
| **Shake** | ±8 px random position on panic/impact | 4–8 frames |

Plus **swaps** (the "animation" of faces): hard-cut expression changes on beats, and a **blink** (eyes →
lid-closed for 2 frames) every 3–4 s whenever a shot holds over 3 s. Mouths don't lip-sync: the narrator is
inner voice. Other characters get a 2-state mouth flap (open/closed every 4 frames) while their gibberish plays.

### Editing rules
1. **Nothing is static for more than 3 s.** Every 2–3 s something changes: cut, face swap, punch-in, prop pop, caption.
2. **The hook line starts at frame 1.** No intro, no logo; the tag slap *is* the intro.
3. **Captions:** word-chunk captions (2–5 words) synced to VO, centred in the upper-middle (y ≈ 480–700 at
   1080×1920), one yellow keyword per chunk. Speech-bubble text for other characters stays in bubbles.
4. **Safe zones:** nothing important below y = 1540 or in the right strip x > 920 (Shorts UI).
5. **Audio levels:** VO −14 LUFS integrated; music bed −28 to −24 LUFS (ducked 6 dB under VO); SFX peaks −6 dBFS.
6. **Transitions:** location change = **whip pan** (6-frame directional blur slide) or a **hard cut on a
   sound**. Never cross-dissolve.
7. **Punchline pattern:** record scratch → 0.4 s silence → punch-in on the face → line → SFX.
8. **End:** last line → 1.5 s end card (Paper background, Nobo with a "?" tag, VO: "Who should I be next?",
   end sting). Cut the end card from the TikTok version if the loop is the ending.

---

## 11. Thumbnail and title strategy

**Titles**
- Formula: **`Life as [identity]` + an optional `(specific twist)`**, ≤ 50 characters, sentence case, max one emoji.
  - "Life as an Introvert (someone actually invited me)"
  - "Life as the Eldest Daughter 😭"
- The identity must be the **first words**. That's the search term and the self-selection trigger.
- Pin a comment on every video: **"Who should Nobo be next? 👇"**. Topic requests from comments are your free idea pipeline, and the replies boost the video.
- Description: one line + three hashtags: `#lifeas #animation #[identity]`.

**Shorts first frame = thumbnail.** In the feed, the first frame is what people see. Frame 1 always has
the title tag, the character in a strong expression, and the hook bubble already visible. In the Shorts editor,
choose a mid-video thumbnail frame with the funniest face plus the tag.

**16:9 thumbnails (compilations and channel page)**: see `brand/thumbnail_mock.png`:
- Max **two characters**, the lead ≥ 50 % of frame height, in the most extreme face (panic/shocked/dead inside).
- **One yellow tag with 1–3 words** (the identity, not the title: "FIRST JOB", "ELDEST DAUGHTER").
- A plain, softened background so the silhouette reads instantly.
- Consistent placement: lead left, tag top-right. The channel page then looks like a series.

---

## 12. Repeatable production template

### Folder layout (one per episode)
```
EP###-slug/
  script.md          # filled-in template below
  bg/                # background photos, 1080x1920, already treated (sat -20, blur 2)
  props/             # one-off stickers (pizza with eyes, sun with sunglasses…)
  vo/vo.wav          # one take, cleaned
  project.capcut     # duplicated from the MASTER template project
  export/            # final .mp4 + thumbnail frame
```
Keep one **MASTER CapCut project** with: the tag-slap intro, a caption style preset, the end card, a
contact-shadow PNG, the SFX folder and the cast PNG library. Every episode starts by duplicating it.

### Script template (copy for each episode)
```
TITLE:            Life as ______ (twist)
IDENTITY TAG:     LIFE AS ______           CHEST TAG: ______
LEAD / CAST:      ______
STORY ENGINE:     one-event spiral | job titles | HUD/counter | countdown | translation | expectation vs reality | day-in-the-life | then vs now
AUDIENCE:         who sends this to whom? "_____ sends to _____"

0:00–0:03  HOOK           (one line + one visual. Must be understood with the sound off.)
0:03–0:15  SETUP          (the rule of this world, in two beats)
0:15–0:45  ESCALATION     (3–4 beats, each worse/weirder than the last; one joke every 5–7 s)
0:45–1:05  CLIMAX         (record scratch → the biggest absurdity)
1:05–1:20  BUTTON         (a twist, a warm beat, or a line that loops back to 0:00)

RECURRING ELEMENTS CHECK: [ ] tag slap  [ ] curl gag  [ ] NPC eye-slide  [ ] a chest-tag change or HUD
                          [ ] record scratch before punchline  [ ] loop/warm ending  [ ] "?" end card
```

### Prompt blocks (copy-paste)

**Background:** `Vertical 9:16 smartphone photo, [scene], eye-level, natural light, realistic and unremarkable, no people, no text, no logos, empty space in the lower centre of the frame for a character to stand, shallow depth of field, shot on iPhone`

**Character style block.** Use it only for poses the SVG rig doesn't have yet, and always attach
`brand/character_sheet.png` as the image reference (most current image models accept a reference image):
```
Simple hand-drawn cartoon character in the exact style of the reference sheet: large bald bean-shaped head
(55% of total height, slightly wider at the top), two big round white eyes with small black dot pupils,
flat skin-coloured eyelid cutting across the top of the eyes, tiny single-line mouth, no nose, no ears,
one small curly hair strand on top, short sack-shaped body in a plain coral-orange hoodie (#FF6B4A),
navy trousers, black oval shoes, noodle arms with round mitten hands (no fingers), small yellow rectangular
name tag on the chest. Thick uniform black marker outline, slightly wobbly line, completely flat colours,
no shading, no gradients. [POSE], [EXPRESSION]. Full body, centred, plain white background.
```

| Pose | `[POSE]` text |
|---|---|
| P07 sit at desk | sitting on an office chair in three-quarter view, hands on a keyboard |
| P08 burrito | lying in bed wrapped in a grey blanket up to the chin like a burrito, only the head showing, seen from the side |
| P09 walk | mid-step walking to the right, one arm forward one arm back (make a 2nd image with the limbs swapped) |
| P10 hold object | holding an object in front of the chest with both hands, arms bent |
| P11 celebrate | both arms straight up in the air, slight jump |
| P12 flop | lying face-down flat on the floor, arms limp |
| P13 tiptoe | sneaking on tiptoes to the left, knees bent, arms raised like a cartoon burglar (2 frames) |
| P14 eating | holding a snack to the mouth with one hand, cheeks puffed |
| P15 phone typing | holding a smartphone with both hands close to the face, thumbs on the screen |

After generating: remove the background, check the outline thickness against the sheet, and recolour to
the exact hex palette in an editor if the model drifted. Once a pose is approved, it joins the library forever.

### Writing rules
- **~2.5 words/s of VO.** 60 s ≈ 150 words, 90 s ≈ 225 words. Scripts in this repo are 160–200 words, with visual-only beats filling the rest.
- Every joke has a **specific number or noun** ("11 minutes", "Gary", "a fry from 2021"). Specific = funny.
- **Rule of three, break the third** ("a seminar on tax law, a chess club, and a dentists' conference. I am not a dentist.").
- The protagonist must want something (silence, money, iftar, leaving at 5) and the world must block it.
- Read the hook to someone who doesn't know the identity. If they don't get it in 3 s, rewrite it.

### Anti-repetition rules (for hundreds of videos)
1. Never run the same **story engine** twice in a row (8 engines listed in the template).
2. Never the same **pillar** twice in a row.
3. A recurring cast member's big moment at most every 3rd video (Mama, Gary, Bro). Scarcity builds fans.
4. Change **one** of these every video: time of day, location type (home/work/street/transport), weather.
5. Every 10th video: an event episode (a crossover, "Life as Nobo" meta episode, or a collab with a fan's idea).

### Time budget once the library exists (per video)
| Step | Time |
|---|---|
| Script + punch-up | 60 min |
| Backgrounds (shoot/source/generate + treat) | 45 min |
| New props/poses (usually 0–2) | 30 min |
| VO record + clean | 20 min |
| Edit (duplicate master, place, captions, SFX) | 90 min |
| Export, thumbnail frame, upload, pinned comment | 15 min |
| **Total** | **~4.5 h → 3 videos/week = 1.5 workdays** |

### Weekly batch schedule
**Mon:** write 3 scripts · **Tue:** VO + backgrounds for all 3 · **Wed–Thu:** edit · **Fri:** export and schedule the next week. Publish Mon/Wed/Fri, 17:00 in your main audience's time zone.

### What to measure (after each 10 videos)
- **Swipe-away rate / "viewed vs swiped"** (Shorts): if below ~70 % viewed, fix the hooks first.
- **Average % viewed**: target > 80 % on 75 s videos; check where the retention graph drops and cut that beat type.
- **Shares per 1,000 views**: the real signal of "relatable". Double down on the pillar with the most shares.
- **Comments asking for topics**: put them in the idea bank.

---

## 13. Idea bank: 60 future episodes

**Personality:** introvert at a wedding · overthinker sending one text · people-pleaser at a restaurant ·
night owl with a 7 a.m. class · procrastinator with a deadline · someone with no sense of direction ·
clumsy person · person who replies "lol" with a straight face · chronic over-packer · someone who cries at
every movie · the friend who's always late · the one who always plans the trip

**Family:** middle child · youngest sibling · only child · kid of immigrant parents · cousin who "studies
medicine" (the comparison) · dad on WhatsApp family group · moving back in with your parents · first
grandchild · twin · the family's "tech person" · having a strict mum · the kid at the adults' table

**Culture & place:** Moroccan abroad (summer back home) · Arab at a European wedding vs an Arab wedding ·
tourist in Paris · Indian in Paris · Eid morning · someone with an unpronounceable name · first winter in
Canada · Arab mum at a parent-teacher meeting · bilingual brain mid-sentence · going to the Moroccan bank
office · trying to explain your country to foreigners · coming home from abroad (the airport family welcome)

**Life stage & money:** Gen Z at a family dinner · 30 and single at a wedding · new dad · new mum · first
apartment · moving cities · job interview · freelancer · paying taxes for the first time · getting your
driver's licence · flat-sharing with strangers · graduate looking for a job

**Jobs:** waiter · nurse on night shift · primary school teacher · IT support · delivery rider · call centre
agent · barista · pharmacist · taxi driver · content creator · intern · supermarket cashier

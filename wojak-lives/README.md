# WOJAK LIVES: channel bible v2

> **"Life as…" → a funny 60–90 s animated story → upload.**
> Tagline: **Every life is a little ridiculous.**

Contents
1. [Reference analysis](#1-reference-analysis)
2. [Channel positioning](#2-channel-positioning)
3. [30 channel names](#3-30-channel-names)
4. [Top 10 ranked](#4-top-10-ranked)
5. [Final name: Wojak Lives](#5-final-name-wojak-lives)
6. [Brand identity](#6-brand-identity)
7. [The characters (Wojak style)](#7-the-characters-wojak-style)
8. [Profile picture](#8-profile-picture)
9. [The first five videos](#9-the-first-five-videos) (full scripts, storyboards, prompts → `episodes/`)
10. [Global animation and editing rules](#10-global-animation-and-editing-rules)
11. [Thumbnail and title strategy](#11-thumbnail-and-title-strategy)
12. [Repeatable production template](#12-repeatable-production-template)
13. [Idea bank: 60 future episodes](#13-idea-bank-60-future-episodes)

Brand files (already made, in `brand/`; regenerate with `python3 wojak-lives/brand/draw_cast.py`):

| File | What it is |
|---|---|
| `brand/character_sheet.png` | The Wojak cast built on one shared head and body: Nobo, Lulu, Mama, Dad, Boss, Bro, Zoomer, NPC |
| `brand/expressions.png` | The 8 Wojak faces (feels, bloomer, crying, rage, soy, smug, side-eye, doomer) |
| `brand/pfp.png` | Ready-to-upload profile picture: Nobo's Wojak face (1024×1024). `pfp_small_test.png` shows it at 98/48/30 px |
| `brand/caption_style.png` | 9:16 style frame: title tag, caption style, Shorts safe zones |
| `brand/thumbnail_mock.png` | 16:9 thumbnail layout example |
| `brand/*.svg` | Vector sources. Every body part is its own `<g>`/path, so they double as a cut-out rig |
| `brand/fonts/` | Lilita One + Baloo 2 ExtraBold (both free, SIL Open Font License) |
| **`chatgpt_prompts.md`** | **The final character art: ChatGPT prompts for the detailed "badass" doomer-style Wojak cast, profile picture, thumbnails and props** |

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
| Wojak-style character pasted on real photos | Our own hand-built Wojak cast (Nobo & co.) with names, the coral hoodie, the face flash, slightly softened photos so the cartoon pops |
| One idea per shot, 2–4 s rhythm | A real story arc with escalation and a punchline, 60–90 s, not a list that just stops |
| Identity in the title | A **"LIFE AS…" yellow tag** title that stays on screen all video and is the brand's signature |
| Literal visual metaphors + meme-style cut-ins | Our own drawn props/stickers instead of borrowed meme photos (copyright-safe, consistent) |
| Big readable text | Large centred word-chunk captions (not tiny top-left sentences) + a deadpan first-person voiceover |
| Minimal animation | Same minimalism, plus 6 cheap signature moves (tag slap, face flash, pop-in, punch-in, slide, shake) |
| Loopable ending | Endings written to loop back into the first line on purpose |
| — | **Tone: relatable, affectionate, "laughing with, not at."** No grievance or shock framing. Better for ads, brand deals, sharing, and long-term trust |

Do **not** reuse: their specific niqab/thobe Wojak drawings (or any downloaded Wojak edits), their fonts/caption layout, their photos, the meme cut-in image, or
their audio.

### Reference channels (saved)

**Broke & Famous**: https://www.youtube.com/@brokeandfamous22 (saved Oct 2026). **The closest competitor and the art target.**
- 3.75K subscribers, 20 videos, ~43K views in the past week. One recurring doomer Wojak (black beanie,
  black tank top, stippled stubble, black-and-white) who "battles greedy bosses, bizarre customers and the
  endless struggle to make rent". Weekly uploads.
- **Long-form, not Shorts:** 16:9, 5–10 minutes each (e.g. 8:14, 8:07, 8:46).
- Topics/titles (newest first): Living In A Tent (30K views, 1 day) · Living In A Car (96K, 2 weeks) ·
  Inflation In 2026 (61K) · Job Interviews · Rent In 2026 · Pre Ordering GTA 6 Be Like · Unemployment ·
  Job Hunting In 2026 · Life Of A Truck Driver · Living With Your Parents · Life Of A Night Shift Worker ·
  Life Of A Fast Food Employee · Life Of A Retail Employee · Applying For A Job · Wojaks Night Out ·
  Being An Introvert Be Like · Being A Gym Rat Be Like · When You Forget Your Anniversary · Wojak Becomes
  Unemployed · Buying Your First House Be Like.
- Thumbnails: the Wojak's face huge on one side (gritted teeth, eye bags), a blurred real photo behind,
  one big prop (tent, car, a "GROCERIES $2500" sign), and almost no text.
- **Take:** the detailed "badass" doomer-Wojak art quality, blurred-photo thumbnails, a money/jobs topic
  pillar, and a long-form version of our episodes.
- **Don't take:** their character design (beanie + tank top), titles or thumbnails 1:1. Our differences:
  the coral hoodie on a bald, scarred Wojak, a named family cast, culture episodes, and the "Life as…" brand.
- Overlap to manage: their "Being An Introvert" and money episodes overlap our EP001 and EP003. Ours need
  different jokes and our own angle.

**Wojak Lore**: https://www.youtube.com/@WOJAKLORE77: archetype Shorts ("Types of Girlfriends", "Mandarin"), detailed coloured Wojak girls.

---

## 2. Channel positioning

**Wojak Lives is a short-form Wojak-animation sketch channel where every episode drops you into someone else's life
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

The name says **Wojak** up front, like *Wojak Lore*: Wojak fans search for it, and it tells a scroller
exactly what the videos look like.

**The Wojak space today** (web search, Oct 2026): *Lord Wojak* (~226K subs, Doomer/Boomer/Chad meme
stories), *Wojak Explainer* (~63K, explains topics), *Low Budget Stories* (everyday situations), *Pointless
Fiction* ("Life of a tram driver" style; one video ~3.7M views, now dormant), *Wojak Lore* (archetypes), and
small new ones like *Wojak Story Hall*. The "Life in/of X" Wojak format is proven, and nobody owns
**"Life as…" + a named recurring cast + voiced mini-stories**. That's our lane.

Rejected on purpose: anything already taken or too close (*Wojak Lore*, *Lord Wojak*, *Wojak Explainer*,
*Wojak World* (an NFT collection), *Wojak Reality*), and bare "Wojak" (unsearchable).

| # | Name | Note |
|---|---|---|
| 1 | **Wojak Lives** | Every episode is a different life, and it reads as "Wojak lives!" |
| 2 | **Life as Wojak** | The format in the name; a bit long |
| 3 | **Wojak Diaries** | Story-time feel |
| 4 | **Wojak IRL** | Wojaks pasted into real photos = "in real life" |
| 5 | **Wojak POV** | Trendy; "POV" may age |
| 6 | **Wojak Tales** | Warm, story-led |
| 7 | **Wojak Daily** | Promises frequent uploads |
| 8 | **Wojak Files** | "Case files" of different lives |
| 9 | **Wojak Chronicles** | Epic; long |
| 10 | **Wojak Simulator** | Game-y; fits HUD episodes |
| 11 | **Wojak Life** | Plain; very generic |
| 12 | **Wojakverse** | Universe of characters; crypto/NFT vibe |
| 13 | **Wojak Saga** | Serial feel |
| 14 | **Wojak Society** | Archetypes of society |
| 15 | **Wojak Town** | A place with recurring residents |
| 16 | **Wojak Hours** | Late-night meme energy |
| 17 | **Wojak Mode** | "Entering Wojak mode" |
| 18 | **Wojak Shorts** | Literal; ungoogleable |
| 19 | **Just Wojak** | Casual |
| 20 | **Wojak Feels** | Nods to the original "Feels Guy" |
| 21 | **Feels Guy Stories** | Deep-cut name for meme insiders |
| 22 | **Wojak Episodes** | Literal |
| 23 | **Wojak Experience** | "The ___ experience" meme |
| 24 | **Wojak Unfiltered** | Edgy; sets a darker tone than we want |
| 25 | **Every Wojak** | "Every type of…" archetype energy |
| 26 | **Wojak Again** | Running gag potential; weak meaning |
| 27 | **Wojak Moments** | Clip-channel feel |
| 28 | **The Wojak Show** | Sitcom feel |
| 29 | **Wojak & Friends** | Kid-show feel |
| 30 | **Wojak Logs** | Vlog parody; flat |

## 4. Top 10 ranked

| Rank | Name | Memorable | Says the format | Expandable | Searchable | Why it ranks here |
|---|---|---|---|---|---|---|
| 1 | **Wojak Lives** | ★★★★★ | ★★★★★ | ★★★★★ | ★★★★ | Two words, double meaning, every "Life as…" episode fits under it; no channel found with this name |
| 2 | **Life as Wojak** | ★★★★ | ★★★★★ | ★★★ | ★★★★★ | Matches every title exactly, but locks the channel to one format |
| 3 | **Wojak Diaries** | ★★★★ | ★★★★ | ★★★★ | ★★★★ | Story-time feel; no channel found |
| 4 | **Wojak IRL** | ★★★★ | ★★★ | ★★★★ | ★★★ | Clever (photo backgrounds); "IRL" means little to non-English speakers |
| 5 | **Wojak POV** | ★★★★ | ★★★★ | ★★★ | ★★★ | Trendy now, may age |
| 6 | **Wojak Tales** | ★★★★ | ★★★ | ★★★★ | ★★★ | Warm, a little soft |
| 7 | **Wojak Daily** | ★★★ | ★★ | ★★★★ | ★★★ | Pressure to post daily |
| 8 | **Wojak Files** | ★★★ | ★★★ | ★★★★ | ★★★ | Good series feel, less funny |
| 9 | **Wojak Chronicles** | ★★★ | ★★★ | ★★★★ | ★★★ | Too long for a handle |
| 10 | **Wojak Simulator** | ★★★★ | ★★★ | ★★ | ★★★ | Funny, but implies games |

## 5. Final name: **Wojak Lives**

**Handle:** `@wojaklives` (fallbacks: `@wojak.lives`, `@wojaklivestv`). My searches found no channel with
this name, but small or new accounts aren't always indexed, so check the handle on YouTube, TikTok and
Instagram before you commit.

Why it's #1:
1. **"Wojak" up front.** Instantly tells the viewer the style, and catches people who search "wojak".
2. **"Lives" is the format.** Every episode is a different life: "Life as an Introvert | Wojak Lives" reads like a series.
3. **Double meaning.** "Wojak lives!", i.e. the meme is still alive. Good for the channel trailer and the pinned post.
4. **Short and easy to say** in English, French, Arabic and Spanish.
5. **It scales**: "Wojak Lives at Work", "Wojak Lives: Ramadan Special", country-language channels
   ("Wojak Lives FR", "Wojak Lives عربي").

**Brand note:** nobody owns "Wojak", so you can't stop copycats using the word. What you *can* own is the
whole package: the exact name and handle, your own drawings, the named cast (Nobo, Lulu, Mama, Gary), the
yellow "LIFE AS…" title tag and your voice. Build recognition on those.

---

## 6. Brand identity

### Signature device: the yellow "LIFE AS…" tag
The characters themselves are **Wojak faces only**: no logos or badges on them. The brand lives around them:
- **0:00 "tag slap":** a big yellow tag **LIFE AS A ___** slaps onto the top of the frame with a *thwack* (6 frames, slight overshoot). It **stays on screen the whole video**, so a viewer who scrolls in mid-video knows what they're watching. The reference only shows its title for 7 s.
- **Label stickers:** small yellow labels that slap on screen *next to* a character for a gag: the job titles in episode 2, an NPC suddenly getting a name ("GARY"), the "SAFE ZONE" arrow.
- **Thumbnails and banner:** the yellow tag carries the 1–3 words.
- **End card:** Nobo in feels face beside a yellow tag **"WHO'S NEXT?"**, with the VO line "Who should I be next?" pointing to the pinned comment.

### Palette

| Token | Hex | Use |
|---|---|---|
| Ink | `#151515` | All outlines, text outlines |
| Paper | `#FFF8EC` | Brand backgrounds, end card |
| Tag Yellow | `#FFD23F` | Title tag, label stickers, highlighted caption words |
| Signal Blue | `#3D7BFF` | Profile picture background, banner, links |
| Nobo Coral | `#FF6B4A` | Nobo's hoodie, the brand's "hero" colour |
| NPC Grey | `#A9AEB4` | Extras / crowds |
| Wojak skin | `#FBF7F1` | Nobo and the classic pale Wojaks |
| Skin S1–S5 | `#FBDCC4 #EDBF98 #D29E73 #A86B45 #6B4329` | Flat skin tones for other characters |
| Face flash | red `#F0625A` · pink `#F7A8C4` · grey `#B9BEC3` · green `#B5D98A` | One-beat emotion recolour of the whole face |

### Type
- **Lilita One** for the title tag, label stickers and thumbnails. Always on a yellow tag, black text, rotated −3° to −5°.
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
| Tag slap | Short paper/cardboard *thwack* | 0:00 every video, and every label sticker |
| Eye pop | Rubber-band *boing* | Face swaps to Soy: shock |
| Face flash | Red: kettle whistle · Pink: "awkward" cricket · Grey: descending slide-whistle (0.4 s) · Green: cartoon gulp | Whole face recolours for one beat |
| Pop | Bubble *pop* | Captions/props/speech bubbles appearing |
| Gibberish | Pitched "blip-blop" voice | Any character except the narrator speaking |
| Record scratch | Vinyl scratch, then silence | Before the punchline |
| End sting | 3-note ukulele/kalimba motif | End card, every video |

**Music:** one quirky bed per episode (ukulele, pizzicato, lo-fi, light funk) from the **YouTube Audio
Library** or another royalty-free source you own a licence for. Avoid copyrighted/trending tracks. Shorts
over 1 minute that pick up a Content ID claim can be blocked, and ours are all over 1 minute.

---

## 7. The characters (Wojak style)

**Art direction (updated):** the final art is the detailed doomer-Wojak style (ink lines, stipple stubble,
hatching, dark eye bags), generated in ChatGPT with `chatgpt_prompts.md`. Nobo is now bald with a buzz-cut,
has a scar through his eyebrow and heavy stubble, and wears the coral hoodie. The flat SVG cast in `brand/`
is only for layouts and animatics.

See `brand/character_sheet.png` and `brand/expressions.png` for the layout versions. **The whole cast is Wojak-style**: the meme
face audiences already know and read instantly. **We draw every Wojak ourselves** (the rig in
`brand/draw_cast.py`) and never download Wojak PNGs from the web. Those are other artists' edits, and
re-using them is the fastest way to look like every other Wojak channel. What makes ours recognisable is
in the faces themselves (the classic creases, the **face flash**), Nobo's **coral hoodie**, and a fixed cast
with names. The characters carry **no badges or logos**: Wojak faces only.

### Main character: **Nobo**
"Nobo" (from *nobody*) is the classic bald, sad-eyed Wojak, the everyman. He plays the lead in most
episodes; the yellow title tag says who he is this time.

| Trait | Spec |
|---|---|
| **Framing** | **Half-body, cropped at the waist** (the meme's natural framing, same as the reference). Full-body drawings only for special shots (walking, lying in bed). |
| **Head** | Bald Wojak skull in 3/4 view **facing right**: rounded back of the head, flat forehead, jaw sloping to a small chin, ear on the left. Head ≈ 50 % of the visible height. |
| **Eyes** | Heavy-lidded almond eyes with a thick upper lid line, thin lower line and **eye bags**. The near eye is larger than the far one. Small black pupils. |
| **Brows / nose / mouth** | Thin worried brows (inner ends up), the hooked one-line Wojak nose, a short slightly downturned mouth line. |
| **Classic creases** | Two forehead worry lines, a cheek line beside the far eye, a chin crease, and soft grey shading on the back of the skull and under the jaw. These make it read as Wojak rather than a generic cartoon. |
| **Skin** | Classic near-white Wojak `#FBF7F1` for Nobo; other characters use S1–S5 flat skin tones. |
| **Clothing** | Coral hoodie (`#FF6B4A`) with drawstrings, no logos, no badges. |
| **Line** | Thin, slightly wobbly MS-Paint-style black line (6 px outline, 4–5 px features at sheet scale). Flat colours, no shading. |
| **Hands** | Simple rounded hands with a thumb bump, on thick sleeve "noodles". Gestures in the rig: idle, point, phone, facepalm, raise. |

### Signature gag: the **face flash**
Instead of animating emotion, the whole face is recoloured for one beat: **red** = rage, **pink** = cringe
or embarrassment, **grey** = dead inside, **green** = jealous or sick. It's a 2-frame swap with a sound
(see section 6), it reads instantly even at phone size, and it's what makes Wojak Lives Wojaks feel like *ours*.

### Expression system (8 Wojak faces; only the eyes, brows and mouth swap)

| Face | Meme it comes from | Eyes | Mouth | Use |
|---|---|---|---|---|
| **Feels** (default) | the original sad Wojak | heavy lids, bags, sad brows | slight frown | Narration, the "this is my life" look |
| **Bloomer** | Bloomer | closed happy arcs, blush | wide smile | Rare joy, so it means something |
| **Crying** | Crying Wojak | wet eyes, sad brows, tear streams | wobbly line | Fake drama, defeat |
| **Rage** | Angry/red Wojak | wide, tiny pupils, V brows, **red flash** | open, teeth | Explosions of frustration |
| **Soy** | open-mouth "soyjak" reaction | huge eyes, raised brows | huge open mouth | Shock, panic, hype (our panic/shocked face) |
| **Smug** | Smug Wojak | half-closed, looking back | smirk | Small victories, bosses, mums |
| **Side-eye** | — | heavy lids, pupils to the side, sweat drop | flat wonky line | Awkward moments (the most-used face) |
| **Doomer** | Doomer | very heavy lids, dark bags, **grey flash** | flat line | The bottom of the story arc |

### Pose library (draw once, reuse forever)
`P01 idle` · `P02 raise/wave` · `P03 facepalm` · `P05 point` · `P06 phone` (all in the SVG rig) ·
`P04 shrug` · `P07 sit at desk (3/4)` · `P08 blanket burrito in bed` · `P09 walk (2 frames)` · `P10 hold
object with both hands` · `P11 arms up celebrate` · `P12 flopped face-down` · `P13 tiptoe sneak (2 frames)` ·
`P14 eating` · `P15 typing on phone`. P04 and P07–P15 still need drawing (or generating with the style
block in section 12); P08, P09, P12 and P13 are full-body.

Any pose × any face × any character = thousands of combinations with no new drawing.

### Secondary cast (same head and body kit, different hair, headwear and colours)

| Character | Wojak type | Look | Role / personality |
|---|---|---|---|
| **Lulu** | Wojak girl | Long dark hair with fringe, eyelashes, no bags, teal top, skin S3 | Default female lead. Dry wit, the competent one |
| **Mama** | Hijabi Wojak mum | Purple hijab framing the face, green top, skin S2, smug | The universal mum. Loving, loud, always has a task for you. **Likely breakout character; give her catchphrases** ("Just five minutes." "Are you eating well?") |
| **Dad** | Boomer | Black sunglasses, grey side hair, mustache, white polo, skin S4 | Says "too much salt" about everything |
| **Boss** | Smug corporate Wojak | Comb-over, grey suit, red tie | Speaks fluent corporate |
| **Bro** | Chad-ish | Blond swept hair, yellow top, bloomer smile | Over-enthusiastic extrovert friend |
| **Zoomer** | Zoomer | Black beanie, headphones, purple hoodie, phone, doomer stubble | The new intern in episode 5's twist; Gen Z lead in future episodes |
| **NPCs** | NPC Wojak | All grey, dot eyes, triangle nose, flat mouth, **no name** | Crowds, strangers, coworkers. They react only with their eyes (pupils slide to look at the protagonist). An NPC who becomes important **gets a yellow name label** popped next to them (e.g. GARY in episode 4), which is a joke of its own |

A "Mom (alt)" with a bun for non-Muslim family episodes: reuse Lulu's long-hair piece pinned up (to draw when needed).

**Situation rules:** at work, add a plain lanyard. Night scenes get a blue tint on the character (multiply
layer at 15 %). Any headwear works (hijab, cap, beanie, chef hat, graduation cap); the face style never changes.

**Wojak rules (brand safety):**
- No ethnic-caricature Wojaks. Many circulating Wojak variants exaggerate a nationality or race; none of
  ours do. Characters from any culture get the same face, a different skin tone and their own clothing.
- No politically coded variants (the specific "nordic gamer", "groyper" and similar edits). Stick to the
  everyday emotional set above.
- "Wojak" is in the channel name, but keep it out of individual video titles (titles lead with "Life as…"),
  and remember nobody owns the word: the exact name, the cast, the drawings and the tag are what's yours.
- YouTube can demonetise channels as "reused content" when they're mostly templates. Original scripts, your
  own voice and our own drawings keep this channel clearly original.

---

## 8. Profile picture

**Already made:** `brand/pfp.png`: Nobo, the classic sad Wojak, head-and-shoulders on a Signal Blue circle,
in his coral hoodie: a Wojak face only, nothing else, like the big Wojak channels. The sad feels face is
the most recognisable Wojak there is, and the blue + coral colours make it ours. It's tested at 98/48/30 px (`brand/pfp_small_test.png`). Use this
vector version so it matches the videos exactly.

If you want an image-model variant (e.g. a painterly banner version), use this prompt:

```
Square 1:1 YouTube profile picture. One original Wojak-style meme character, head and shoulders, centred,
filling 80% of the frame: bald near-white head (#FBF7F1) in three-quarter view facing right, ear on the left
side, heavy-lidded sad almond eyes with eye bags and small black pupils, thin worried eyebrows with two
forehead worry lines, the classic hooked one-line nose, a cheek crease, a short slightly downturned mouth,
a chin crease, soft grey shading on the back of the head. Wearing a plain coral-orange hoodie (#FF6B4A)
with drawstrings. Thin slightly wobbly black MS-Paint style outlines, completely flat colours, no shading, no gradients.
Solid flat royal-blue circular background (#3D7BFF). Deadpan, melancholic, funny, very readable at tiny sizes.
No text, no logo, no watermark, no realistic features.
```

**Banner (2560×1440, safe area 1546×423 centred):** Paper background, the whole cast in a line
(`character_sheet` order), each with a small yellow name label under them, and a big yellow tag **"LIFE AS… EVERYONE."** with a
small "New episodes Mon · Wed · Fri" beneath.

---

## 9. The first five videos

Release order is chosen so the first three are the broadest; the culture episode lands once the channel
has a baseline audience; and the finale has the strongest loop.

| # | File | Title | Lead | Story engine |
|---|---|---|---|---|
| 1 | [`episodes/01-introvert.md`](episodes/01-introvert.md) | Life as an Introvert | Nobo | **One event spirals** (a party invite) |
| 2 | [`episodes/02-eldest-daughter.md`](episodes/02-eldest-daughter.md) | Life as the Eldest Daughter | Lulu | **Job titles** (a new yellow job-title label slaps next to her every scene) |
| 3 | [`episodes/03-broke-student.md`](episodes/03-broke-student.md) | Life as a Broke Student | Nobo | **Survival game HUD** (money counter) |
| 4 | [`episodes/04-ramadan-in-europe.md`](episodes/04-ramadan-in-europe.md) | Life as a Muslim in Europe During Ramadan | Nobo | **Countdown clock** (iftar timer) |
| 5 | [`episodes/05-gen-z-first-job.md`](episodes/05-gen-z-first-job.md) | Life as a Gen Z at Their First Job | Nobo | **Translation subtitles** (corporate → real) |

Each episode file contains: title + alternates, hook, full script, scene-by-scene storyboard (duration,
action, background, expression, dialogue, on-screen text, camera, sound), image-generation prompts for
every background and special asset, animation instructions, editing instructions, thumbnail, and a
virality breakdown.

Shared across all five, so they feel like one channel: same cast and rig, tag slap at 0:00, persistent title
tag, the same caption style, deadpan VO, gibberish for other characters, the face flash as the emotion meter, a
record scratch before the main punchline, a loop or warm-beat ending, and the "WHO'S NEXT?" end card.

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
8. **End:** last line → 1.5 s end card (Paper background, Nobo in feels face beside a yellow "WHO'S NEXT?" tag, VO: "Who should I be next?",
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
- Max **two characters**, the lead ≥ 50 % of frame height, in the most extreme face (soy/rage/doomer).
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
TITLE TAG:        LIFE AS ______           LABEL GAGS: ______
LEAD / CAST:      ______
STORY ENGINE:     one-event spiral | job titles | HUD/counter | countdown | translation | expectation vs reality | day-in-the-life | then vs now
AUDIENCE:         who sends this to whom? "_____ sends to _____"

0:00–0:03  HOOK           (one line + one visual. Must be understood with the sound off.)
0:03–0:15  SETUP          (the rule of this world, in two beats)
0:15–0:45  ESCALATION     (3–4 beats, each worse/weirder than the last; one joke every 5–7 s)
0:45–1:05  CLIMAX         (record scratch → the biggest absurdity)
1:05–1:20  BUTTON         (a twist, a warm beat, or a line that loops back to 0:00)

RECURRING ELEMENTS CHECK: [ ] tag slap  [ ] face flash  [ ] NPC eye-slide  [ ] a label sticker or HUD
                          [ ] record scratch before punchline  [ ] loop/warm ending  [ ] "WHO'S NEXT?" end card
```

### Prompt blocks (copy-paste)

**Background:** `Vertical 9:16 smartphone photo, [scene], eye-level, natural light, realistic and unremarkable, no people, no text, no logos, empty space in the lower centre of the frame for a character to stand, shallow depth of field, shot on iPhone`

**Character style block.** Use it only for poses the SVG rig doesn't have yet, and always attach
`brand/character_sheet.png` as the image reference (most current image models accept a reference image):
```
Original Wojak-style meme character in the exact style of the reference sheet: bald near-white head
(#FBF7F1) in three-quarter view facing right, ear on the left, heavy-lidded almond eyes with eye bags and
small black pupils, thin worried eyebrows, forehead worry lines, the classic hooked one-line Wojak nose,
cheek crease, short mouth line, chin crease, soft grey shading on the back of the head. Plain coral-orange
hoodie (#FF6B4A) with drawstrings, dark jeans, simple rounded hands with a thumb. Thin slightly wobbly black
MS-Paint style outline, completely flat colours, no badges, no logos. [POSE], [EXPRESSION].
Centred, plain white background.
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

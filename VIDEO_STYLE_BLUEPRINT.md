# VIDEO STYLE BLUEPRINT: "Documented Wartime History" micro-documentary

Reverse-engineered from the reference video *"German POWs Thought America Staged the Cars. Then the Train
Kept Moving."* (channel name on screen: **WWII Box: Documented Wartime Histories**). The reference is 9:20 long,
640x360 source (published at 1080p or higher), 30 fps, with about 1,450 narrated words.

This file describes the **formula**, not that video. Use it to make original videos on new topics.

> **Visual identity:** sections 4–5 and 7 record how the *reference* looks so the formula is understood.
> Do not reuse its colours, fonts or card designs. Our own look is defined in **`HOUSE_STYLE.md`**
> (contact frames for photos, field-ledger cards for data). Keep the structure, pacing and narration
> rules from this file, and take the look from the house style.

---

## 0. How the reference was measured

| Metric | Value | How |
|---|---|---|
| Runtime | 560 s | ffprobe |
| Narration | ~1,450 words, **~155 wpm**, near-continuous (pauses of 0.5-1 s between paragraphs) | Whisper transcript |
| Shots | ~95-135 visual changes | ffmpeg scene detection (thresholds 0.25 / 0.15) |
| Shot length | **median 3.3-4.9 s, mean 4-6 s**, 10th pct ~1-3 s, 90th pct ~8-12 s | cut intervals |
| Overlay cards | ~14 graphic moments (document, portrait, date, timeline, bar chart, subscribe, comment CTA) | contact sheets |
| Audio | voice at about -17 dB mean, with a quiet music/ambience bed under it (gaps sit around -26 to -32 dB, never silent) | volumedetect |

---

## 1. The video formula

**One small, true, sourced human anecdote → used as a lens on a big historical truth.**

> *A specific person saw a specific, slightly absurd thing → the official/propaganda story said X → the evidence
> in front of them kept saying Y → follow them through the system that produced Y → the human consequences
> (some changed their minds, some doubled down, someone died) → a quiet, ironic closing line that echoes the hook.*

Core ingredients:
1. **A named eyewitness** with a verifiable source (memoir, oral history, magazine interview). The whole video
   hangs on them; they show up at the start, the middle and the end.
2. **A contradiction**: a belief vs. the reality the person can see. The title states it as a mini-mystery
   ("X thought Y. Then Z kept happening.").
3. **Scale-up**: zoom out from the anecdote to the system (economy, logistics, law, camps) with 2-3 hard
   numbers.
4. **Nuance, not triumph**: the narrator always qualifies ("The numbers were not proof of an effortless
   system", "None of this caused an instant political conversion. Evidence rarely works that neatly.").
5. **Documentary credibility**: every claim card shows a source line; reused generic footage is labeled honestly
   ("SMALLTOWN AMERICA CONTEXT: NOT CAMP CONCORDIA").
6. **Archival-only visuals**: black-and-white newsreel footage + scanned print sources + a few clean
   data cards. **No** memes, cartoon characters, AI faces, flashy SVG, emojis, or on-screen captions of the
   narration.

**Niche and audience**: WWII and 20th-century social history for adult viewers (mostly men 35+, history buffs,
fans of "Timeline" / "WWII in Color" / "Fall of Civilizations"-style channels). They want *untold* angles (POWs,
home front, logistics, ordinary people), dislike sensationalism and errors, and reward sourcing. Watched on TV
or desktop and often listened to like a podcast, so **the narration must carry the whole story on its own**.

**Title pattern**: `[Group] Thought [false belief]. Then [ongoing evidence].` Other forms that fit:
`Why [Group] Couldn't Believe [Thing]`, `The [Object] That Convinced [Group] [Truth]`,
`What [Person] Saw From [Place] in [Year]`.

---

## 2. Script structure

Target 1,300-1,700 words for an 8-11 min video at ~155 wpm. Paragraphs of 3-6 sentences, one idea each.
The percentages are of total runtime.

| # | Act | % | Reference timing | What it does |
|---|---|---|---|---|
| 1 | **Cold-open hook** | 0-7% | 0:00-0:40 | Drop into one vivid moment with date + place + who ("One morning in 1943, German prisoners crowded the windows of an American train."). State the expectation ("It should have been empty."), the contradicting image, the absurd rationalisation, then a short beat line ("Then the train moved on."). |
| 2 | **Witness + thesis** | 7-11% | 0:40-1:00 | Introduce the named witness and the source ("remembered the remarks 60 years later"). Give the thesis in one line ("A staged row of cars might explain one factory. It was harder to explain the next town, and the one after that."). |
| 3 | **Rewind / backstory** | 11-22% | 1:00-2:00 | "Two months earlier..." Who the witness was, how they got here. Dense in dates, units and places. End on a striking sensory memory (Statue of Liberty). |
| 4 | **The contradiction, explained** | 22-38% | 2:00-3:35 | Explain the propaganda claim *fairly* ("contained just enough truth to travel well"), then the real facts (rationing rules, stickers, speed limits). Turn on the key distinction ("rationing by need was not the same as national paralysis"). |
| 5 | **Scale-up to the system** | 38-52% | 3:35-5:00 | Leave the window and go inside the factories and networks. 1-2 hard statistics with an official source. A qualifier ("The numbers were not proof of an effortless system"). Return to the witnesses ("The prisoners did not have those totals... They had something harder to dismiss."). |
| 6 | **Arrival / second piece of evidence** | 52-68% | 5:00-6:47 | New setting, new kind of evidence (rural Kansas, the camp, the food). Concrete numbers (acres, buildings, headcount). One humanising or funny detail with a name ("the Victory Wedge"), immediately turned serious ("funny because the conclusion underneath it was not"). |
| 7 | **Complication / dark turn** | 68-82% | 6:47-7:45 | Not everyone changed their mind. A named victim or villain, a death, institutional failure. Two contrasting reactions stated as parallel sentences. |
| 8 | **Resolution of the witness** | 82-95% | 7:45-9:00 | How change really happened (slowly, through newspapers and classes). What became of the witness later in life (dates, institutions). Insert the **comment CTA** here, in the narrator's voice, about 20 s before the end. |
| 9 | **Echo close** | last 15-20 s | 9:00-9:20 | Callback to the hook image, phrased as an aphorism ("One staged explanation could not survive the next parking lot."). No outro, no "thanks for watching". |

**Mid-roll subscribe**: one silent on-screen card around 35-40% (reference: 3:20, "Subscribe to WWII Box /
DOCUMENTED WARTIME HISTORIES"). It is never spoken.

### Narration style rules
- Third person, past tense, calm, authoritative, a little dry. British-neutral documentary register. No "guys",
  no "insane", no rhetorical "but here's the thing".
- **Specificity in every sentence**: dates ("May 12"), units ("10th Panzer Division"), places ("Cap Bon"), objects
  ("A white shirt had been tied to the end of a carbine."), numbers ("158 acres", "about 300 buildings").
- **Short sentences hit hard** after long ones: "It should have been empty." / "Then the train moved on." /
  "That distinction mattered."
- **Lists of three or four concrete nouns** for montage ("Sidings, houses, roads, factory walls, people going to
  work"; "barracks, mess halls, a hospital, recreation rooms, and guard towers").
- **Metaphor sparingly, one per section**: "the windows kept editing it without asking permission", "the next
  contradiction arrived on a plate", "The cars outside Akron opened a crack."
- **Fair to the "other side"**: explain why the false belief was plausible before knocking it down.
- **Qualify every big claim** ("The numbers were not proof...", "Evidence rarely works that neatly").
- **Callbacks**: reuse the hook object (cars, parking lot, the train) 3-4 times through the script.
- Attribute memory claims: "He remembered...", "one man believed...".
- Spell out numbers the way they are spoken; never write "1.2M".

---

## 3. Scene structure

A **scene** = one narration paragraph (15-60 s). Each scene is built from **shots** (2-8 s) plus at most **one
graphic card**.

Typical scene recipe (repeat it for every paragraph):
```
[establishing archival shot 4-8 s] → [2-5 detail shots 2-5 s each, one per concrete noun]
→ [optional graphic card 8-14 s, placed on the paragraph's key fact] → [transition shot back into footage]
```

Reference card rhythm: cards appeared at 0:08, 0:59, 1:23, 1:48, 2:29, 3:20, 4:08, 5:26, 6:10, 6:36, 7:28,
7:58, 8:45 and 9:02. That is **one card every 30-45 s**, never two in a row. Between cards it is 100% footage.

---

## 4. Visual rules

### Footage
- **Black-and-white archival film only** (1930s-40s newsreels, government films, public-domain stock such as
  Prelinger Archives, US National Archives, Library of Congress, Wikimedia Commons). Colour appears only in
  printed sources and late-life photos, which marks them as "document/present", not "period".
- Grain, scratches, dust and soft focus are kept. Don't over-sharpen or colourise.
- Mixed aspect ratios are fine: 4:3 clips sit pillarboxed on black, with no blurred side fill.
- **Literal-but-generic matching**: when no footage of the exact event exists, show the closest generic
  equivalent (any train interior with soldiers, any factory gate, any Kansas-like town) and add a
  **context label** saying so.

### Context label (recurring, very small)
- Bottom-left, ~11 px at 720p (~16 px at 1080p), uppercase, letter-spaced, white at 60-70% opacity, no box.
- Format: `SUBJECT CONTEXT — PLACE, YEAR(S)` or `PLACE/EVENT, YEAR`. Examples from the reference:
  `FACTORY AND TRAIN CONTEXT — UNITED STATES, 1942-43`, `AXIS DEFEAT IN NORTH AFRICA — 1943`,
  `WILLOW RUN B-24 PLANT, MICHIGAN, 1943`, `SMALLTOWN AMERICA CONTEXT — NOT CAMP CONCORDIA`,
  `HORST VON OPPENFELD IN LATER LIFE`.
- Shown for 3-6 s at the start of a new footage block, about every 45-90 s.

### Graphic design system (the cards)
| Token | Value |
|---|---|
| Panel background | deep navy `#141c2e` at ~92% opacity (footage faintly visible behind) |
| Accent | muted gold `#d4a537` (title underline, timeline dots/line, bars, highlight boxes) |
| Title font | Serif: Georgia / Libre Baskerville / Source Serif, regular weight, cream white `#f2efe6` |
| Body font | Sans: Inter / Source Sans / DejaVu Sans, light grey `#c9ccd3`, ~60% of title size |
| Source line | Sans, ~40% of title size, grey `#9aa0aa` |
| Title underline | 2 px gold line under the title text only (text width) |
| Corners | square (0-2 px radius), no drop shadows, no gradients, no icons |
| Safe margins | 5% left/right, card left edge at x ≈ 4.5% |

**Never**: emojis, meme images, cartoon characters, bright saturated colours, animated stickers, kinetic
typography, word-by-word subtitles, maps with flashy arrows. (The reference contains **no maps, SVG
characters, memes or screenshots of the web**. A restrained map in the same navy/gold style is acceptable when
geography is the point. See the `RouteMapCard` component below.)

---

## 5. Editing and animation rules

- **Cuts**: hard cuts between footage shots, on sentence or clause boundaries, ideally on a stressed noun.
- **Crossfades**: 0.3-0.5 s dissolves only **into and out of graphic cards / document stills**, and at act
  boundaries.
- **Card entrance**: panel fades in (opacity 0→1, 10-12 frames) while the full-screen document/photo
  dissolves over the footage. The title underline draws left→right over ~15 frames. Timeline dots and the line
  draw in sequence. Bars grow from 0 to value with ease-out (~20 frames, staggered ~6 frames).
- **Document highlight**: a thin gold rectangle draws around the quoted paragraph about 1 s after the document
  appears (stroke-dashoffset animation, ~20 frames).
- **Movement**: footage plays at native speed with its own camera motion. Stills (portraits, documents) get a
  very slow push-in (scale 1.00→1.04 over the hold) or stay static. Never fast zooms, whip pans, shakes,
  glitches or light leaks.
- **Document/portrait layout**: the scan sits centered at ~45-55% of the frame width, full height minus ~2%,
  over a **blurred, darkened, enlarged copy of itself** as the background (blur ~30 px, brightness ~0.55).
- **Lower-third** (name/date) sits on top of the still or footage: navy box at bottom-left, serif title with
  gold underline, sans subtitle, and a source line bottom-right in tiny text.
- **Music**: one low, slow ambient/orchestral bed (strings and piano, no drums) at roughly -24 to -30 dB under
  the voice, continuous across the whole video. No sound effects, no stingers.
- The video starts on footage plus narration at frame 0 (no logo, no title card) and ends on the last
  narration line plus about 1 s of footage, then a hard stop.

---

## 6. Typical timing and pacing

| Element | Duration |
|---|---|
| Footage shot | 2-8 s (target median **4 s**). Fast montage of listed nouns: 1.5-2.5 s per shot |
| Long hold (landscape, establishing) | 6-12 s, max one per minute |
| Document card | 10-14 s (covers 2-3 sentences that paraphrase the document) |
| Portrait card | 8-12 s (first time a person is named) |
| Date lower-third | 4-6 s, over footage |
| Timeline card | 9-11 s |
| Bar-chart card | 10-12 s |
| Subscribe card | 4-5 s, over footage, at about 35-40% of the runtime |
| Comment CTA | 6-8 s, spoken + lower-third, about 20 s before the end |
| Visual change frequency | a new shot every **3-5 s** on average; nothing static for more than 14 s |
| Graphic density | 1 card every 30-45 s, ~12-15 per 9 minutes |
| Speech | ~155 wpm, 0.5-1.0 s pause between paragraphs, ~0.3 s between sentences |

Runtime formula: `seconds ≈ words / 2.6 + paragraphs × 0.7`.

---

## 7. Reusable scene types / components

Each component is a Remotion `<Sequence>`. Props are in TypeScript-ish notation.

1. **`ArchivalClip`**: `{src, startFrom, durationInFrames, contextLabel?, pushIn?: boolean, fit: 'contain'}`.
   Plays B&W footage, letterboxed or pillarboxed on black. Optional context label in the first 4 s.
2. **`DocumentCard`**: `{image, highlight: {x,y,w,h} (fractions), title, subtitle, source}`. Scanned
   magazine/newspaper/letter page over a blurred self-background, gold highlight box drawn on, plus a lower-third.
   *Use when narration paraphrases or quotes a primary/secondary source.*
3. **`PortraitCard`**: `{image, name, descriptor, source}`. Same layout as DocumentCard with a photo of the person.
   *Use on the first mention of the key witness and for their "later life" photo.*
4. **`DateLowerThird`**: `{date: "May 12, 1943", caption: "Surrender on Cap Bon, Tunisia"}` over footage.
   *Use when the narration names an exact date that is a turning point.*
5. **`TimelineCard`**: `{title, points: [{label, sub}] (3, max 4), source}`. Horizontal gold line, dots, label
   above, sub-label below. *Use for journeys (A → B → C) or a sequence of rules/stages.*
6. **`BarCompareCard`**: `{title, bars: [{label, value, unit}] (2-3), source}`. **Format numbers for humans**
   (`123,000 aircraft`, `1.2 million trucks`). The reference printed `1.233e+06 units`, which is a bug to avoid.
   *Use for any "X vs Y" or growth number.*
7. **`SubscribeCard`**: `{channel, tagline}`. Small navy lower-third, silent.
8. **`CommentCTA`**: `{text}`. Lower-third with the spoken line ("If you know another ... put it in the comments.").
9. **`RouteMapCard`** (optional, not in the reference): muted grey-blue land on navy sea, gold dashed route
   drawn with stroke-dashoffset, serif place labels. Keep it static apart from the route draw.
10. **`QuoteCard`** (optional): a short witness quote in serif on navy, with attribution. Use at most once per
    video.

---

## 8. Rules for turning narration into visuals

Go through the script sentence by sentence and tag every sentence with one **visual intent**:

| Sentence type | Visual |
|---|---|
| Specific moment/action ("crowded the windows of a train") | Literal archival clip of that action (generic is fine), cut on the verb |
| List of concrete nouns | Rapid montage, one shot per noun (1.5-2.5 s each) |
| Named person, first mention | `PortraitCard` (if a photo exists), otherwise footage of their unit/setting + context label |
| "X remembered / recalled / wrote" | `DocumentCard` of the source with the relevant paragraph highlighted |
| Exact date that turns the story | `DateLowerThird` over the matching footage |
| Journey or sequence | `TimelineCard` (3 points) |
| Hard number / comparison | `BarCompareCard` |
| Abstract idea ("propaganda had offered them a country...") | Symbolic footage: crowds, wide streets, machines, sky. Never text on screen |
| Place establishing ("Concordia was a farming town") | Wide landscape/town footage, long hold, context label if generic |
| Dark event (death, violence) | Darker, blurrier footage (troops in snow, a handwritten diary), no graphic card, slower cuts |
| Callback / closing aphorism | Footage of the hook subject (cars, crowds, a train), held a little longer |

Hard rules:
- **Visuals illustrate, they don't caption.** Never put the narration's words on screen except in card titles,
  which are 3-6 word headline paraphrases ("The cars were staged", "Rationing did not mean paralysis",
  "Reading was itself a risk").
- **Card title = the claim, subtitle = the specific fact, source = the citation.**
- The visual changes **on** the noun it illustrates (±0.3 s), using word timestamps.
- Never repeat the same clip within 60 s. Reusing a clip later as a callback is fine (the reference reuses the
  overpass and the tower).
- If footage would be misleading (a different place or event), add a "CONTEXT / NOT X" label.

---

## 9. Production workflow (automated, Remotion-based)

### Folder layout
```
video/<slug>/
  research/sources.md          # every fact → citation (title, author, publication, date, URL)
  script.md                    # final narration, one paragraph per scene
  audio/narration.wav          # TTS or recorded voice
  audio/words.json             # word-level timestamps (Whisper)
  assets/footage/*.mp4         # public-domain archival clips + licence notes
  assets/stills/*.jpg          # documents, portraits
  storyboard.json              # generated scene/shot plan (schema below)
  remotion/                    # Remotion project (components from section 7)
  out/<slug>.mp4
```

### Pipeline
1. **Topic & source** (manual/AI research): find a named eyewitness account with a citable source plus 2-3
   official statistics. Write `research/sources.md`. *No source, no video.*
2. **Script**: write to the section 2 structure, 1,300-1,700 words. Check every number against sources.md. Generate
   the title with the section 1 pattern.
3. **Voice**: TTS (calm male or female documentary voice, ~155 wpm, slightly slower than default) or a human
   recording. *Paid TTS APIs need the owner's approval first (see CLAUDE.md). Keys come from environment
   variables only.* Export at 48 kHz.
4. **Timestamps**: `faster-whisper` with `word_timestamps=True` → `words.json`. (Running `small.en` on CPU took a
   few minutes for 9 minutes of audio.)
5. **Shot plan**: split the script into sentences and tag each with a visual intent (section 8). Choose card placements
   (one per 30-45 s, on the strongest fact of the paragraph). Write `storyboard.json`:
   ```json
   {
     "fps": 30, "width": 1920, "height": 1080,
     "audio": "audio/narration.wav", "music": "audio/bed.mp3", "musicGainDb": -26,
     "shots": [
       {"type": "ArchivalClip", "start": 0.0, "end": 4.6, "src": "footage/train_window.mp4",
        "srcIn": 12.0, "contextLabel": "FACTORY AND TRAIN CONTEXT — UNITED STATES, 1942-43"},
       {"type": "DocumentCard", "start": 8.0, "end": 18.6, "image": "stills/wapo_2004_p1.jpg",
        "highlight": [0.55, 0.42, 0.40, 0.20], "title": "The cars were staged",
        "subtitle": "Horst von Oppenfeld recalled the argument sixty years later",
        "source": "Lynn Ermann, Learning Freedom in Captivity, The Washington Post Magazine, 18 January 2004"},
       {"type": "SubscribeCard", "start": 200.0, "end": 204.5, "channel": "...", "tagline": "DOCUMENTED WARTIME HISTORIES"}
     ]
   }
   ```
   Shot boundaries snap to word starts from `words.json`. Shots must tile the timeline with no gaps; cards are
   full shots, while lower-thirds/labels are overlays with their own start/end.
6. **Footage sourcing**: search public-domain archives by the shot's keywords (e.g. Prelinger on archive.org,
   NARA, Wikimedia Commons, British Pathé only with a licence). Store the licence/source per clip. Convert to
   B&W if needed (`hue=s=0`), add light grain for consistency, and trim with ffmpeg.
7. **Render**: a Remotion composition reads `storyboard.json` and maps each shot to its component (`<Sequence
   from={start*fps} durationInFrames={(end-start)*fps}>`). Wrap card entries/exits in 10-15 frame opacity
   crossfades. Then `npx remotion render Main out/<slug>.mp4 --codec h264 --crf 18`.
8. **QC checklist** (automate where possible):
   - median shot length 3-5 s, no shot over 14 s, cards every 30-45 s, none adjacent;
   - every card has a source line; numbers human-formatted;
   - generic footage carries context labels; no clip repeated within 60 s;
   - voice peaks around -1 dB, mean around -17 dB; music bed 10+ dB under the voice;
   - frame 0 is footage + voice; last line echoes the hook; comment CTA ~20 s before the end;
   - contact sheet (`ffmpeg -vf "fps=1/2,scale=384:-1,tile=5x4"`) reviewed before upload.

### Where Blender fits (this repo)
For moments archival footage can't show (e.g. a route across a globe, an empire's spread), render a short
clip with the scripted Blender approach in `blender/` (see `globe_mongols.py`). Keep it **desaturated or
navy/gold** so it matches the card palette, and drop it in as an `ArchivalClip`. Use it sparingly, at most
1-2 per video.

---

## Quick-start checklist for a new episode
1. Pick a named witness + a contradiction. Write the title.
2. Write the 9-act script (~1,500 words), with every fact sourced.
3. Generate the voice → word timestamps.
4. Tag sentences → `storyboard.json` (footage every 3-5 s, a card every 30-45 s).
5. Source the B&W footage and scans; write the context labels.
6. Render with Remotion using the navy/gold/serif card system.
7. Run QC, review a contact sheet, export.

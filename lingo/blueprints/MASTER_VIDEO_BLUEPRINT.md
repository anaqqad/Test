# MASTER VIDEO BLUEPRINT: "Map Tour" format

Reverse-engineered from the reference video `FIFA_Would_Cup_Winner_1930_-_2026.mp4` (1280×720, 30 fps, H.264/AAC 44.1 kHz stereo, 1:43.13).

**How this was analysed.** Frames were extracted every 0.5–2 s and at full resolution for the key moments. A scene-change detector ran at threshold 0.3. Audio was measured as loudness and spectral centroid per 0.25 s, plus spectral flatness. Whisper speech recognition was run on the audio.

**Labels used in this document.**
- **[Observed]**: measured or seen directly in the file.
- **[Inferred]**: a reasonable conclusion that is not directly visible.
- **[Unknown]**: cannot be determined from the file.

> **No production blueprint was supplied with the video**, only the video itself. Section 2 therefore says "not available" wherever a comparison against a blueprint was requested. It describes the workflow that can be inferred instead, without naming tools the creator may or may not have used.

---

## 1. Reverse engineering (Phase 1)

### 1.1 Structure at a glance [Observed]

| Time | Segment | Content |
|---|---|---|
| 0:00–0:04.7 | Title | World map. Title text pops in one line at a time: "FIFA WORLD CUP" (white, pink outline), then "WINNER" (white, orange outline), then "1930 - 2026" (white, red outline). By about 0:04 the text is gone and the map is clean. |
| 0:04.7–0:16.4 | Block 1 | Uruguay: 2 trophies; chips 1930, 1950 |
| 0:16.4–0:28.1 | Block 2 | England: 1 trophy; chip 1966 |
| 0:28.1–0:39.8 | Block 3 | Brazil: 5 trophies; chips 1958, 1962, 1970, 1994, 2002 |
| 0:39.8–0:51.4 | Block 4 | Italy: 4; chips 1934, 1938, 1982, 2006 |
| 0:51.4–1:03.1 | Block 5 | Germany: 4; chips 1954, 1974, 1990, 2014 |
| 1:03.1–1:14.8 | Block 6 | France: 2; chips 1998, 2018 |
| 1:14.8–1:26.4 | Block 7 | Argentina: 3; chips 1978, 1986, 2022 |
| 1:26.4–1:38.1 | Block 8 | Spain: 2; chips 2010, 2026. This is the only block with fireworks. |
| 1:38.1–1:43.1 | Outro | Fully zoomed-out world map showing all 8 characters. No text, no call to action. |

- **One continuous virtual camera.** The scene detector found **0 hard cuts** at threshold 0.3 [Observed]. Every change is a camera move, a pop-in or a fade.
- **Strict block length of 11.67 s.** That's 350 frames at 30 fps, measured from the repeating audio pattern [Observed]. The blocks are mechanically identical, which suggests a template or keyframe preset reused per country [Inferred].
- **Order is not chronological by first title.** England (1966) comes before Brazil (1958) and Italy (1934). What is clear: the newest result (2026) is held back for the last block [Observed]. The reason for the rest of the order is [Unknown].

### 1.2 Hook (0:00–0:05)
- **Title promise:** the text "1930 - 2026" promises the newest result. The curiosity gap is "who won in 2026?", and it's only answered in the last 15 s (Spain, at about 1:31) [Observed placement; Inferred intent].
- **Instant clarity:** the world map tells the viewer "this is about countries" before any text is read [Inferred].
- **Speed:** the first zoom starts at about 0:05, so there's no slow intro [Observed].

### 1.3 Storytelling
- **The narrative is a collection.** Each block adds one more personified winner to the map. These characters **stay on the map** for the rest of the video:
  - England is visible next to Germany.
  - Uruguay sits beside Argentina.
  - France, Germany and Italy appear in the edges of the Spain shot.
  - The outro shows all 8 together.
  
  So the map "fills up" as a visible reward [Observed].
- **Emotional curve:** calm (map) → small surprise (reveal hit) → satisfaction (trophies stacking). The peak comes at Brazil's 5 trophies in block 3 (the most titles), and the finale is fireworks for the newest winner in block 8 [Observed: trophy counts, fireworks only in block 8].
- **Humour:** purely visual and gentle. The country characters blink, wink and glance around. In France's reveal the eyes are closed, then open (a "waking up" beat) [Observed]. There are no jokes, text gags or dialogue [Observed].
- **Payoff:** the final world shot with every winner together [Observed].

### 1.4 Script
- **No narration and no dialogue.** Whisper found no speech at all [Observed].
- **On-screen text** is limited to:
  - the title card (3 lines)
  - one country name per block
  - result chips containing a year, two flags, two team names and a score [Observed]
- Result-chip grammar [Observed]:
  - the **loser's flag is on the left with its score in red**
  - the **winner's flag is on the right with its score in green**
  - the year sits above the score
  - team names in small caps sit under each flag
  
  Example: `1930 ARGENTINA 2 – 4 URUGUAY`.
- Chips run left to right in chronological order. With 2 chips they sit bottom-left and bottom-right; with 4–5 they form a full-width row [Observed].

### 1.5 Visuals [Observed]
- **Style:** flat 2D cartoon map.
  - **Land** is a saturated lime green (about #22dd22), with **thick black borders**. Border thickness grows with zoom, so close-ups look like chunky cartoon outlines.
  - **Ocean** is a blue vertical gradient (teal at the top, deep blue lower down) with lighter horizontal "wave" bands.
  - **Clouds:** white cartoon clouds with soft shadows drift over the map. Large foreground clouds pass the camera during zooms, acting as a natural wipe.
- **Character, "the country face":**
  - The country's real outline is filled with its **flag**, clipped to the shape, with a white inner edge and a black outer line.
  - It has **two big googly eyes**: white sclera, cyan iris and a black pupil with a highlight.
  - There is no mouth and there are no limbs.
  - The **trophies** stand in a row on the lower half of the shape: golden World Cup trophy icons, one per title.
- **Consistency rules:**
  - the same eye design for every country
  - eyes always in the upper-middle of the shape
  - trophies always in the lower half
  - characters remain on the map at small scale after their block
- **Layout:**
  - Character centre-left.
  - **Flag card** in the top-right corner: a large flag with the country name in white bold capitals and a dark outline under it.
  - **Result chips** along the bottom edge.
- **Particles:** white streaks or confetti drifting in every close-up. **Fireworks** only for the finale (Spain).
- **Lighting:** none (flat colour). No depth of field. No colour grading changes.

### 1.6 Editing and motion (block anatomy, t = 0 at block start) [Observed from 0.5 s frames; ±0.25 s]

| t (s) | Event |
|---|---|
| 0.0–0.3 | World map holds |
| 0.3–1.8 | Zoom in on the country (an ease-in-out zoom of about 8–15×). Foreground clouds sweep past at about 1.0 s. |
| 1.8–2.5 | Close-up of the green map with black borders. The camera has settled. |
| 2.5–3.0 | A "ghost" flag fades into the country shape (semi-transparent) |
| ~3.2 | **Reveal:** the flag becomes solid and the eyes pop in, on the impact sound |
| 3.3–3.8 | The flag card slides in from the top-right |
| 3.5–4.5 | Trophies pop in one by one (about 0.25 s apart). The name label appears under the card. |
| ~4.3 | Result chips fade or pop in |
| 4.3–9.0 | **Hold** (about 4.5–5 s). Eyes blink or wink once or twice, particles drift. |
| ~9.0 | The card slides out and the chips fade |
| 9.5–11.0 | Zoom out to the world (with foreground clouds) |
| 11.0–11.67 | World map hold. The character stays, now tiny. |

The total is **one camera move in and one out per block**, with a **hold of about 5 s** in between. Average "shot" length, counting each held composition, is about 5 s. Motion is constant: clouds and particles never stop.

### 1.7 Audio [Observed: timing and levels; Unknown: exact content]

| t in block | Sound |
|---|---|
| 0.3–1.8 | **Whoosh** (swells to about −30 dB, then decays) |
| 1.8–2.4 | **Silence** (near-total) |
| ~3.2 | **Impact hit**, the loudest moment (peaks around −7 dB), synced to the reveal |
| 3.3–9.0 | A **country-specific bed** at about −22 to −32 dB. Its tonality varies by country: Brazil's is tonal and music-like (flatness 0.09), Argentina's and Spain's are noisy (flatness 0.36–0.42), possibly crowd or fireworks. Whether these are anthems, chants or crowd noise is **[Unknown]**, because the analysis could not listen. |
| 9.3–10.8 | **Whoosh out**, decaying |
| 10.8–11.67 | Silence |

There's no voice and no continuous music track across blocks [Observed]. Every block starts from silence, so the impact hit stands out [Observed].

### 1.8 Retention
- **Curiosity gap:** the title promises 2026, and 2026 is shown last [Observed].
- **Predictable rhythm:** viewers learn the 11.7 s pattern by block 2 and anticipate the next reveal ("who's next?") [Inferred].
- **Pattern interrupts inside the template:**
  - the trophy count changes (1 to 5)
  - the chip row layout changes with the count
  - blinks and winks differ per country
  - France's eyes "wake up"
  - only the finale has fireworks [Observed]
- **Accumulation:** earlier winners appear in later shots, which rewards continued watching [Observed].
- **Short length** (1:43) and no wasted seconds [Observed].

### 1.9 Ending
- **Payoff:** every winner together on the world map [Observed].
- **Loop:** the last frame is the same zoomed-out world as the first frame, minus the title. That makes the video loop seamlessly, which suits Shorts and autoplay [Observed composition; Inferred intent].
- **No outro card, no call to action, no end screen** in the file [Observed]. YouTube end screens could still be added in Studio [Unknown].

---

## 2. Blueprint comparison (Phase 2)

**The reference blueprint was not provided.** No instruction-to-result comparison is possible. Below is the workflow that is **inferred** from the output. It names no tools, because the creator's tools are [Unknown].

1. **Dataset:** a list of winners, with each final's year, opponent and score.
2. **Map asset:** a vector world map with country boundaries, styled flat (green land, black borders, blue ocean).
3. **Character template:** a flag texture clipped to each country outline, plus a shared eye rig with blink keys and a trophy icon repeated N times.
4. **Camera template:** one zoom-in/hold/zoom-out keyframe set, duplicated per country and retargeted to that country's centre and zoom level.
5. **Overlay templates:** the flag card and the result chip, filled from the dataset.
6. **Persistent layer:** each character stays visible after its block.
7. **Audio template:** whoosh, silence, hit, bed, whoosh, placed at fixed offsets per block.
8. **Export:** 1280×720, 30 fps.

Details the reference leaves out, which **any reproduction needs**:
- the exact font
- easing curves
- eye-rig timing
- the source of the beds (licensing!)
- the rule for ordering blocks
- whether the map projection changes during zooms
- how to fact-check the dataset

These are specified in sections 3–9.

---

## 3. The formula (Phase 3)

**Storytelling DNA**
1. One clear question in the title. Answer the newest or most surprising part **last**.
2. One block per item, all the same length. Each block is a mini reveal with a sound hit.
3. Items **accumulate** visibly. The final shot shows them all.
4. Numbers drive emotion: a bigger count means a bigger stack. One finale effect, used only once.
5. No narration. Text only where data must be read.

**Visual identity**
- Flat map.
- One-colour land.
- Heavy outlines.
- Personified shapes with a shared, simple face.
- A collectible icon repeated N times.
- Corner card plus bottom chips.

**Cinematic language**
- One continuous camera.
- Zoom in, hold, zoom out.
- Foreground elements wipe the transitions.

**Pacing**
- Title under 5 s.
- Blocks of 10–12 s, with a hold of about 5 s.
- Total 1:30–3:00.

**Humour and emotion**
- Micro-acting only: blink, wink, glance, eyes open late, a sweat drop.
- Never mean.

**Rules for building scenes:** see sections 6 and 8.

---

## 4. Rules for original episodes (Phase 4)

- **Same skeleton, new data.** Use different events, collectibles, faces and colours.
- **Do not copy the reference's character face design,** meaning its cyan googly-eye style plus flag fill on a green map. Choose your own eye style, land colour and collectible icon.
- **Do not reuse the reference's title art or chip graphics.**
- **Facts:** every number must come from a source listed in the description. If a fact can't be verified (for example, an event after your knowledge or data cutoff), label it or leave it out.

---

## 5. Production rules

**5.1 Recommended pipeline (this repo, programmatic, no AI video model needed).** These are existing tools in this repository:
- `d3-geo` and `world-atlas` for the map and country outlines
- `flag-icons` SVGs for flags
- HTML/SVG pages rendered frame by frame with Playwright/Chromium
- `ffmpeg` for encoding and audio mixing (see `lingo/render.mjs`)

A map-tour renderer would:
- draw the world in SVG with `d3.geoNaturalEarth1()`, or keep `geoMercator()` for close-ups
- animate the projection's `scale` and `translate` per frame towards the country's bounding box
- clip a flag `<image>` to the country path
- overlay the eye rig and icons

**5.2 AI-assisted pipeline (alternative).** Generate static assets with an image model: the map style plate, the characters and the icons. Animate with simple 2D moves in any editor. Image-to-video models aren't needed for this format, and they risk distorting map outlines.

**5.3 Technical specs**
- 1920×1080 (or 1280×720 to match the reference), 30 fps.
- Shorts version: 1080×1920. Use the same blocks with the map cropped and the chips stacked.
- Loudness about −14 LUFS integrated, peaks below −1 dBTP.

---

## 6. Story and script templates

**6.1 Title**
`[EVENT/CATEGORY] [WINNERS/HOLDERS] [START YEAR] - [END YEAR]`, or a question: `Which countries have [X]?`

**6.2 Episode sheet** (fill this in for each episode)
```
Topic:
Question the title promises:
Dataset (item, country, count, list of {year, detail}):  -> source URL for every row
Order rule: (e.g. by count ascending, newest last) - finale item = most surprising/newest
Collectible icon (replaces the trophy):
Chip format: [year] [left element] [value] [right element]
Finale effect (used once):
Persistent characters: yes
Length: title 4.7 s + N × 11.67 s + outro 5 s
```

**6.3 Text rules**
- At most 3 title lines.
- Country names in caps.
- Chips: year plus no more than 2 short labels plus 1 value.
- No sentences on screen.

---

## 7. Characters

- **Base:**
  - the country's real outline (from the map data)
  - filled with its flag, or a single brand colour for non-country items
  - a white inner stroke of about 3 px and a black outer stroke whose width depends on zoom
- **Face:** two eyes only.
  - Pick one series style and never change it. Examples: half-closed "sleepy" eyes, round black dot eyes, or Wojak-style tired eyes. This channel already owns Wojak characters in `lingo/wojaks/`.
  - Place the eyes at 40% of the height of the shape's bounding box, centred on the visual centroid (not the bounding-box centre). Example: Chile needs its centroid, Italy needs a manual offset.
  - Eye size is 18% of the shape's width, clamped to a minimum on screen of 40 px.
- **Micro-acting library:**
  - blink (3 frames closed)
  - wink
  - glance left or right
  - eyes open late
  - sweat drop
  - stars in the eyes (finale only)
- **Collectible:** one icon per count. Arrange in a row; if there are more than 5, use two rows. Drop in at 0.25 s intervals.
- **Persistence:** after its block the character stays on the map. Eyes stay visible down to a shape size of 30 px, then hide.

---

## 8. Storyboard method (per block, frame-exact at 30 fps; total 350 frames)

| Frames | Camera | Elements | Audio |
|---|---|---|---|
| 0–9 | world hold | previous characters visible | silence |
| 10–54 | zoom in (ease-in-out cubic) to the country's bounding box with 35% padding | foreground cloud crosses at frames 25–45 | whoosh-in starts at frame 10 |
| 55–74 | hold | plain map | silence |
| 75–89 | hold | flag fades in at 40% opacity | (silence) |
| 90–96 | small 4% push-in | flag at 100%, eyes pop (scale 0 → 110% → 100%) | **impact hit at frame 96** |
| 97–112 | – | flag card slides in from the top-right | bed starts |
| 105+ | – | collectibles pop, 8 frames apart | soft "pop" per item (optional) |
| 128–140 | – | chips fade in, left to right | – |
| 140–270 | hold | blink at about 160 and 230, a glance at about 200 | bed continues |
| 270–285 | – | card slides out, chips fade | bed fades |
| 285–330 | zoom out (ease-in-out) | foreground cloud | whoosh-out |
| 330–349 | world hold | the character is now persistent | silence |

**Title** (141 frames):
- line 1 pops in at frame 0
- line 2 at frame 20
- line 3 at frame 40
- each pop is a scale overshoot from 0.6 to 1.08 to 1.0 over 10 frames
- all lines fade out by frame 120

**Outro** (150 frames): world hold. Optionally a 2% slow zoom-out.

---

## 9. Prompt templates

**9.1 Image model (style plates and characters)**
- **World map:** `Flat 2D cartoon world map, saturated single-colour land with thick black country borders, ocean as a vertical blue gradient with soft lighter horizontal wave bands, a few white cartoon clouds with soft grey shadows, no text, no labels, 16:9, clean vector look.`
- **Character:** `The outline of [COUNTRY] as a flat cartoon character filled with the [COUNTRY] flag, white inner outline, thick black outer outline, two [SERIES EYE STYLE] eyes in the upper middle, no mouth, no limbs, transparent background, flat vector style.`
- **Collectible:** `A single [ICON, e.g. golden olympic torch] icon, flat cartoon, thick dark outline, transparent background.`

**9.2 Animation (if you use an editor or an AI animator instead of code)**
`Keep the map outlines rigid. Do not morph shapes. Only move the camera (zoom/pan), blink the eyes (closed for 3 frames), and pop icons with a scale overshoot. Clouds drift slowly from left to right at a constant speed. No camera shake, except a 4% push-in on the reveal frame.`

---

## 10. Voice-over and sound

- **Default:** no voice-over, as in the reference.
- **Sound kit, per block:**
  - whoosh in (about 1.5 s)
  - silence (about 0.6 s)
  - impact or hit (short, punchy, the loudest event)
  - a bed of about 5.5 s
  - whoosh out (about 1.5 s)
- **Beds must be licensed or self-made.** Never use national anthems or chants from unknown sources. Use public-domain anthem recordings only if their licence is verified.
- **Mix levels:** hit at −8 dBFS peak, bed at −22 to −28 dBFS, whooshes at −28 dBFS.
- **Finale:** add a fireworks or crowd layer, used once.

---

## 11. Quality-control checklist

- [ ] Every data row has a source. Future or unverifiable items are labelled.
- [ ] Block length is exactly identical (±1 frame).
- [ ] The impact hit lands on the reveal frame (±1 frame).
- [ ] Eyes sit inside the shape for oddly shaped countries (Chile, Norway, Italy, Indonesia).
- [ ] Chips: winner on the right, colours consistent, years in order.
- [ ] Persistent characters are visible in later blocks and in the outro.
- [ ] The finale effect is used exactly once.
- [ ] Text is readable on a phone (minimum cap height of about 28 px at 1080p).
- [ ] Audio is licensed. Loudness is about −14 LUFS.
- [ ] The first and last frames match (loopable).
- [ ] The title promises the newest or most surprising item, and it really comes last.

---

## 12. Episode workflow

1. Pick a topic with 5–12 items and a countable value. Write the episode sheet (section 6.2) with sources.
2. Decide the order. The finale is the newest or most surprising item.
3. Generate or prepare the assets: map style, the character per item, the collectible icon, and the flags.
4. Build the timeline from the frame table in section 8. Place the sound kit at fixed offsets.
5. Render a test: frames at the reveal and hold of the first block and the last block.
6. Run the QC checklist. Render the full video, a 16:9 thumbnail (finale character, big number, flag) and the Shorts crop.
7. Description: sources, audio credits, and a "data as of [date]" note.

---

## 13. Validation (Phase 6)

### Three original concepts
1. **"Every Summer Olympics Host 1896–2032"**
   - Collectible: torch icons.
   - Count: hostings per country.
   - Finale: Australia, with Brisbane 2032 (a future host, labelled "upcoming").
2. **"Countries That Drive on the Left"**
   - Collectible: steering wheels.
   - Not a count. Use a chip per fact (the year each switched or kept left-hand driving). Data needs careful sourcing.
3. **"Every Country That Has Won the Eurovision Song Contest"**
   - Collectible: microphones.
   - Count: wins.
   - Data and the latest year need verification at production time.

**Strongest: Concept 1.** The facts are stable and well known. It has a natural "future" finale, mirroring the reference's 2026 hook. The collectible count varies (1–5), which gives the same "stack grows" payoff.

### Full blueprint: "Every Summer Olympics Host Country 1896 – 2032"

**Dataset.** Summer Games hosts, standard list; verify against olympics.com before publishing.

| Country | Count | Chips (year, city) |
|---|---|---|
| Greece | 2 | 1896 Athens, 2004 Athens |
| France | 3 | 1900 Paris, 1924 Paris, 2024 Paris |
| United States | 5 | 1904 St. Louis, 1932 Los Angeles, 1984 Los Angeles, 1996 Atlanta, 2028 Los Angeles (upcoming) |
| United Kingdom | 3 | 1908 London, 1948 London, 2012 London |
| Sweden | 1 | 1912 Stockholm |
| Belgium | 1 | 1920 Antwerp |
| Netherlands | 1 | 1928 Amsterdam |
| Germany | 2 | 1936 Berlin, 1972 Munich (West Germany) |
| Finland | 1 | 1952 Helsinki |
| Italy | 1 | 1960 Rome |
| Japan | 2 | 1964 Tokyo, 2020 Tokyo (held 2021) |
| Mexico | 1 | 1968 Mexico City |
| Canada | 1 | 1976 Montreal |
| Soviet Union (shown as Russia's outline, labelled USSR) | 1 | 1980 Moscow |
| South Korea | 1 | 1988 Seoul |
| Spain | 1 | 1992 Barcelona |
| China | 1 | 2008 Beijing |
| Brazil | 1 | 2016 Rio de Janeiro |
| Australia | 3 | 1956 Melbourne, 2000 Sydney, 2032 Brisbane (upcoming) |

**The video uses 9 blocks.** At 19 blocks it would run about 3:50, too long for the format, so the 10 single-host countries are combined into one "everyone else" sweep:
- Greece, France, United Kingdom, United States, Germany, Japan
- block 7: the "one-timers" sweep (10 countries pop in a fast chain, 0.4 s each)
- block 8: the US with 2028
- finale: Australia with 2032

**Script and on-screen text**

| Time | Scene | Camera | On screen | Audio |
|---|---|---|---|---|
| 0:00–0:04.7 | Title | world | "SUMMER OLYMPICS / HOSTS / 1896 - 2032" (pop, 3 lines) | soft rising tone |
| 0:04.7–0:16.4 | Greece | zoom to Greece | character + 2 torches; card GREECE; chips 1896 ATHENS, 2004 ATHENS | whoosh, hit, bed (self-made light strings) |
| 0:16.4–0:28.1 | France | zoom | 3 torches; chips 1900, 1924, 2024 (all PARIS) | same kit |
| 0:28.1–0:39.8 | United Kingdom | zoom | 3 torches; chips 1908, 1948, 2012 (LONDON) | same |
| 0:39.8–0:51.4 | Germany | zoom (UK and France characters visible at the edges) | 2 torches; 1936 BERLIN, 1972 MUNICH | same |
| 0:51.4–1:03.1 | Japan | zoom | 2 torches; 1964 TOKYO, 2020 TOKYO, with a small "held 2021" tag | same |
| 1:03.1–1:20.0 | One-timers (16.9 s) | slow pan around the globe | 10 characters pop with 1 torch each; chip ticker along the bottom | hit per pop (quieter) |
| 1:20.0–1:31.7 | United States | zoom | 5 torches (the biggest stack); chips 1904, 1932, 1984, 1996, 2028; the "2028" chip gets an UPCOMING tag | same, bigger bed |
| 1:31.7–1:43.4 | **Australia (finale)** | zoom | 3 torches; chips 1956 MELBOURNE, 2000 SYDNEY, 2032 BRISBANE (UPCOMING); **fireworks** | hit, fireworks |
| 1:43.4–1:48.4 | Outro | world | all characters | silence and soft tail |

**Visual prompts**
- Map plate: as in 9.1, but with **sandy-orange land** (not green) to separate the look from the reference.
- Characters: flag-filled outlines with **round black dot eyes and white highlights** (the series eye style). No googly cyan eyes.
- Collectible: `flat cartoon olympic-style torch with orange flame, thick dark outline`. Avoid the official Olympic rings, which are trademarked.

**Animation:** follow section 8 exactly. Torches drop in with a small flame flicker loop (2 frames). For the one-timers sweep, the camera pans along a great-circle path; each character pops in when the camera passes it.

**Audio**
- A self-made or royalty-free whoosh, hit and fireworks kit.
- The bed is one short royalty-free orchestral loop, transposed per block to keep it fresh.
- No anthems.

**Why it follows the formula and stays original**
- Same skeleton:
  - the title promises the future
  - fixed 11.67 s blocks
  - a reveal hit
  - a growing stack of collectibles
  - persistent characters
  - a single fireworks finale
  - a loopable world outro
- New:
  - the event
  - the collectible
  - land colour, eye style and chips (city instead of score)
  - the "one-timers" sweep, which changes the rhythm once as a deliberate pattern interrupt

# BLUEPRINT 04: Long-form language map explainer (8–12 min)

**Reverse-engineered from TheLanguageMap (@TheLanguageMap).** Written for LingoDude on 2026-11-20.

The goal: a future session can take **one title** and produce a full video in this style. The video must keep
LingoDude's own rules:
- real recordings only;
- every recording credited;
- our own maps, art and wording;
- the red-hook thumbnail rule applies to channel-look thumbnails (see §9.3 for how the two styles meet).

Earlier blueprints, for comparison:
- 01: `MASTER_VIDEO_BLUEPRINT.md`, the map tour;
- 02: `LANGUAGE_VIDEO_BLUEPRINT.md`;
- 03: `DISCORD_CHAT_COMEDY_BLUEPRINT.md`.

**Labels used throughout.**
- **[Observed]**: seen or measured directly in the file.
- **[Catalog]**: from the channel page or RSS feed.
- **[Inferred]**: a reasonable conclusion, not directly visible.
- **[Unverified]**: could not be checked.

**Evidence.**
- Supporting files are in `blueprints/img/tlm/`:
  - contact sheets every 2 s (`sheet0/2/6.jpg`);
  - key stills (`hiA.jpg`, `hiB.jpg`);
  - every thumbnail on the channel (`thumbs_grid.jpg`).
- The Whisper transcript is in `ideas/ref/thelanguagemap_6aRVKEfEjN4_transcript.txt`.

---

## 0. What was analysed, and how

| Source | What it supports |
|---|---|
| **MP4 uploaded by the owner**: "Why Did Spain Rule the Philippines for 300 Years but Leave Almost No Spanish Behind?" (6aRVKEfEjN4). 1280×720, 30 fps, 8:25.4. | Everything shot by shot: frames every 2 s, key stills at full size, a visual-change signal at 10 fps, a Whisper medium transcript with word timings, EBU R128 loudness, a pause map, the stereo side channel, spectrograms. |
| **Channel page + RSS feed** (fetched 2026-11-20 00:38 UTC). | All 11 uploads with title, views, upload date and length, plus every thumbnail. YouTube blocked the watch pages with a captcha, so **no transcripts, descriptions or chapters for the other videos**. |
| **"Why Did the Dutch Rule Indonesia for 350 Years but Leave Almost No Dutch Behind?"** (1OqPZhXFpow, 12:33, the longest and the second-best performer). | Title, thumbnail, length and views only. Editing claims about it are **[Inferred]** from the shared template. |
| **"Why Do Most Paraguayans Speak Guaraní When Only 2% Are Indigenous?"** (h3RUHXBYM6k, 10:21, a typical recent upload). | Title, thumbnail, length and views only. Same limits as the row above. |

To finish the three-video shot-by-shot study, upload the MP4s of the Dutch and the Paraguay videos to chat. The
same measurements can then be run on them, and §2.2 and §2.3 updated.

---

## 1. The channel catalog [Catalog]

- **Basics:** channel id UCQJ2AyxeqI4FSNnDTsx5hCw. Created 2026-10-19. 5.28K subscribers. 11 uploads in 31 days.
- **Cadence:** one long video every 3–4 days, plus one vertical Short.

| Upload date | Title | Length | Views (2026-11-20) |
|---|---|---|---|
| 10-19 | Why Did Spain Rule the Philippines for 300 Years but Leave Almost No Spanish Behind? | 8:26 | **1,020,005** |
| 10-20 | Why the Philippines doesn't speak Spanish (vertical Short re-cut) | Short | 1,698 |
| 10-22 | Why Did the Dutch Rule Indonesia for 350 Years but Leave Almost No Dutch Behind? | 12:33 | **217,106** |
| 10-26 | Why Did Brazil Nearly End Up Speaking a Native Language Instead of Portuguese? | 11:23 | 87,560 |
| 10-29 | India Gave English an Expiry Date. Why Is It Still Here? | 12:17 | **208,852** |
| 11-02 | Why Doesn't America Speak German? | 11:16 | 106,572 |
| 11-05 | Why Doesn't Louisiana Speak French? | 9:17 | 89,719 |
| 11-08 | Irish Is Ireland's First Official Language. So Why Does Almost Nobody Speak It? | 9:23 | 37,113 |
| 11-13 | Why Did Rome Wipe Out Every Language in Spain and France Except Basque? | 11:23 | 62,716 |
| 11-16 | Why Do Most Paraguayans Speak Guaraní When Only 2% Are Indigenous? | 10:21 | 39,961 |
| 11-19 | Why Does Madagascar Speak A Language From Borneo? | 10:37 | 7,817 (13 h old) |

### 1.1 Recurring topics

Every video asks why a place does or doesn't speak a language its history says it should.

- **Colonial language that didn't stick:** Philippines, Indonesia, India. These are the top three, together about 1.45M views.
- **Immigrant or colonial language that faded:** German in America, French in Louisiana.
- **The native language that survived or won:** Paraguay, Brazil, Basque.
- **Official language nobody speaks:** Irish.
- **Language far from home:** Madagascar.

The strongest topic so far is **"a big power ruled for centuries, yet its language is missing"**. The paradox is a
number (years of rule) against an outcome (almost no speakers).

### 1.2 Title formulas

| Formula | Examples | Views |
|---|---|---|
| A. *Why did [power] rule [place] for [N] years but leave almost no [language] behind?* | Philippines, Indonesia | 1M, 217K |
| B. *[Place] did [official act]. So why [opposite]?* | India "expiry date", Irish | 208K, 37K |
| C. *Why doesn't [place] speak [expected language]?* | America German, Louisiana French | 106K, 89K |
| D. *Why did [place] nearly end up speaking [X] instead of [Y]?* | Brazil | 87K |
| E. *Why did [power] wipe out every [X] except [one]?* | Basque | 62K |
| F. *Why do most [people] speak [X] when only [small %] are [Y]?* | Paraguay | 40K |
| G. *Why does [place] speak a language from [far place]?* | Madagascar | (new) |

- 10 of the 11 titles are a question.
- 9 of the 11 start with "Why".
- Every title holds **two facts that seem to contradict each other**.
- Titles that carry a **number** (300 years, 350 years, an expiry date) did best.

### 1.3 Thumbnail composition

`img/tlm/thumbs_grid.jpg`, looked at directly. Every thumbnail uses the same template:

- **Background:** a textured paper map (beige land, deep teal-blue sea, vignette), seen at an angle that shows the region.
- **The subject:** one country raised in 3D with a hard drop shadow, filled with one flat colour. The colours seen so far are red, orange, blue, purple, magenta, green and gold.
- **The tag:** a small uppercase pill in the same colour, with the paradox number or context: "333 YEARS OF SPAIN", "350 YEARS OF DUTCH RULE", "INDIA, 1950", "AMERICA, 1918", "270 YEARS OF SPAIN".
- **The headline:** 2–3 lines in a heavy cream serif, 3–5 words, on the left half. It states the **gap, not the topic**: "So where's the Spanish?", "English had 15 years left", "Then they banned it", "It nearly won", "All gone. Except one.", "3 million → 72,000".
- **One language object:** a speech bubble written in that language ("¿Habla español?", "Spreekt u Nederlands?", "Dia duit?", "Mba'éichapa?"); or a word card ("Deutsch" crossed out, "língua geral", "telo"); or a big yellow "?".
- **What is left out:** no faces, no photos, no arrows, no logo.

### 1.4 Runtimes

- Range 8:26–12:33; median 11:16.
- The breakout is the **shortest** upload (8:26).
- [Inferred] The later videos grew longer as the channel added more evidence per act, not more filler.

---

## 2. Shot-by-shot analysis

### 2.1 Breakout hit: Philippines (MP4, 8:25.4) [Observed]

#### Technical facts
- **Video:** 1280×720, 30 fps.
- **Speech:**
  - Narration runs to 8:13 (1,460 words). The brand end card follows.
  - Average speed **178 words per minute**. Every minute falls between 166 and 187.
- **Sentences:** 98 in total.
  - Average 14.8 words, median 15, longest 34.
  - 12 sentences have 6 words or fewer. They are used as punches: "Then there's the Philippines." "It worked fast." "Then came the Second World War."
- **Loudness:** −14.6 LUFS integrated, loudness range only 1.8 LU (very even).
  - **Every pause between sentences falls to digital silence** (black gaps in the spectrogram).
  - The stereo side channel sits at −66.6 dB, so the mix is mono, voice-led.
- **Music:**
  - **No music bed was found** [Observed]: if there were one, the pauses would not be silent.
  - [Inferred] There are few sound effects or none. Faint stereo blips sit only at about 2:58, 7:00 and 7:39, at −44 dB.
  - [Inferred] Hard silence after every sentence suggests the voice was recorded or generated one sentence at a time and laid end to end. The voice could not be identified as human or synthetic. [Unverified]
- **Cuts and visual changes:**
  - **Hard cuts: 0.** The scene detector at 0.15 found none. The whole video is one continuous map camera, with cross-fades only at the title card and the end card.
  - **Visual change** (frame difference at 10 fps): a new on-screen event **every 2.9 s on average** (median 2.4 s), 170 events in total. Events per minute: 25, 22, 22, 14, 21, 17, 21, 23, then 5 in the outro.
  - The share of each minute where the frame is still: 32 %, 42 %, 60 %, **87 %** (minute 3, the friar section, which holds one close-up), 65 %, 74 %, 69 %, 69 %.
  - The longest fully still stretch is 6.4 s (8:02–8:09, the recap).

#### Opening 60 seconds (word timings from Whisper)

| Time | Narration | Picture | Job |
|---|---|---|---|
| 0:00 | "Spain ruled Mexico for 300 years and today Mexico speaks Spanish." | **First shot**: world map, Spain and Mexico already red. A dashed route draws from Spain to Mexico. A "¡Hola!" bubble pops on Mexico. | Sets up the **pattern** in under 5 s. The first line names the subject and the rule. |
| 0:05 | "It ruled Peru for nearly as long and Peru speaks Spanish." | Peru fills red, labelled. | Pattern ×2. |
| 0:08 | "Same with Colombia, Cuba, Chile and most of the continent." | The fill sweeps across Latin America. | Pattern ×3, sped up: one sentence covers a continent. |
| 0:12 | "Then there's the Philippines." | The camera pans west across the Pacific. The Philippines sit tiny and red on the left; the Americas stay red on the right. | **Breaks the pattern.** A 5-word sentence. |
| 0:14 | "…333 years, which is longer than it held Mexico…" | A white card counts up from **0 to 333 "YEARS OF SPANISH RULE"**. | The paradox number, made concrete. |
| 0:19 | "…land in Manila… blank looks." | Zoom to the Philippines. "¿Habla español?" bubble, then "?" bubbles pop over several islands. | Shows the confusion. This is the thumbnail's bubble. |
| 0:24 | "Fewer than half a percent of Filipinos speak it well." | Stat card "SPEAK SPANISH WELL <0.5%" with a nearly empty bar. | Hard number number 2. |
| 0:27 | "I'd always assumed the Americans took over in 1898 and swapped it for English." | Route line to the USA; year chip "1898"; word chips "español → English"; the islands turn blue. | **States the viewer's likely answer**, so it can be overturned. |
| 0:31 | "That's part of it, but when I started digging I found Spanish was barely spoken there even while Spain was in charge…" | Islands go grey; a red glow on Manila; subtitle-style caption "Even under Spain, Spanish barely left Manila". | **Twist number 1**: the easy answer is wrong. |
| 0:37 | "…and some of the people who stopped it spreading were Spanish themselves." | A **mystery portrait card**, a silhouette with "?": "Spain's own people — MORE ON THEM SOON". | **Plants the question that keeps people watching.** It pays off at 2:34 and 3:46. |
| 0:41 | "To understand why…" | **Title card**: cream panel, small red kicker "THE LANGUAGE MAP", serif title "Why Did Spain Leave Almost No Spanish in the Philippines?" Fades in and out over the map (0:41–0:45). | The title lands at **0:41** (8 % of the runtime), after the hook, never before it. The on-screen title is a shorter, plainer version of the upload title. |
| 0:45 | "…look at where the Philippines sits on the map. From Madrid it's about as far away as you can get." | Kicker "A COLONY OF A COLONY" top left. The map pulls out to Madrid and Manila; counter "≈7,447 KM, MADRID TO MANILA". | Into the story. The first act begins with geography. |
| 0:48–1:00 | "In 1565… Legazpi… Cebu… sailed from Mexico, and that detail ends up mattering a lot." | Year chip "1565" top right. Portrait card (line-drawn face, name, role "LED THE EXPEDITION"). A route draws from Cebu to Mexico. Caption: "He sailed from Mexico". | A person, a date and a route: the three building blocks of every later beat. Ends on a mini-hook ("ends up mattering"). |

**When the promise is delivered:**
- The thumbnail's question ("So where's the Spanish?") is answered **in part at 0:31**: it was never there.
- The full answer comes in four causes, at 1:26, 1:57, 2:33 and 4:46.

#### Story map (the 8 sections, each opened by a top-left kicker)

| Time | Section kicker [Observed] | New information | Stakes / payoff | Reset device |
|---|---|---|---|---|
| 0:00–0:45 | *(cold open)* | Pattern, broken pattern, 333, <0.5 %, the 1898 assumption | Twist: "Spaniards stopped it" (planted) | Title card |
| 0:45–1:26 | A COLONY OF A COLONY | Legazpi 1565, Urdaneta's return route, the Manila Galleon (250 years, 1–2 ships a year, 4 months per crossing), run from Mexico City | "a very long rope" | Galleon route arcs, chain chip "Madrid → Mexico City → Manila" |
| 1:26–1:57 | HARDLY ANYONE WENT | 15,600 settlers from Mexico and Peru, 600 from Spain, against 667,000 locals | Contrast with Mexico, where settlers spread everywhere | **Dot chart** card (1 dot = 1,000 people), the third row explodes |
| 1:57–2:33 | SEVEN THOUSAND ISLANDS | 6,978+ islands, 33+ then 100+ languages; a valley-by-valley close-up of Luzon; "Good morning" six ways | The Crown orders Spanish: 1600, 1737, 1800… | A red **"IGNORED" stamp** over the year chips |
| 2:33–3:54 | THE FRIARS | Augustinians, Franciscans, Dominicans, Jesuits; often the only Spaniard in town; the bilingual Doctrina Christiana of 1593 | **The middle payoff of the planted question** (3:46): "Spain's own missionaries held Spanish back" | A mechanism animation: complaint and order bubbles routed **through** the friar; chips "derechos", "igualdad" |
| 3:54–4:46 | THE PEOPLE AT THE TOP | Schools of 1863; under 3 %, then 3–10 %; Rizal and the ilustrados; Aguinaldo, Kawit, 12 June 1898 | **Near reversal**: "Spanish was becoming a national language" | Islands turn red again (Spanish rising) |
| 4:46–5:59 | THE AMERICANS | Manila Bay; the Philippine–American War (a sombre card); the Thomas: about 500, then over 1,000 teachers | Clergy against teachers comparison; English as the way into government jobs | Islands turn blue as the years tick 1903 → 1940 |
| 5:59–6:56 | FEBRUARY 1945 | Old Manila families; the Battle of Manila, about 100,000 civilians killed, "second most destroyed after Warsaw"; Intramuros, Ermita, Malate; a quote card from the historian Florentino Rodao | **The final blow**: the last Spanish-speaking neighbourhoods were destroyed | **The palette drains** to grey-brown (the only colour-mood change); then 1987: "≈400,000 speak it well" |
| 6:56–7:56 | IT'S STILL THERE | "a las dos" → "alas dos", "dose", 6 of the 7 weekdays, thousands of loanwords (mesa, kotse, pamilya), Clavería's 1849 surname catalogue (Santos, Reyes, Dela Cruz), the Chavacano creole | **Twist ending**: the language lost, the words won | Rows of word chips; a definition card "WHAT IS A CREOLE?" |
| 7:56–8:25 | (recap) | The 333 card returns; chips "alas dos, Lunes, mesa, Santos"; a personal last line | "used a dozen Spanish words before lunch" | Lower-third "Subscribe for more stories like this"; end card "The Language Map / NEXT: Brazil was only supposed to be this big" |

**Pacing pattern.**
- A section kicker or a big counter arrives every **30–80 s**.
- Inside each section, something appears every 2–3 s: a chip, a pin, a route, a card or a caption.
- Each section ends with a short punch sentence or a planted question:
  - "Those orders mostly went nowhere."
  - "To see why you need to meet the people who actually ran the islands."
  - "Then the Americans showed up."
- The narrator speaks in the first person **4 times**: 0:27, 0:31, 3:46 and 8:07. Each one marks a surprise ("I think that's the bit that surprised me most").

### 2.2 Longer video: Dutch / Indonesia (12:33) [Catalog + Inferred]

**Packaging:**
- Title formula A, the twin of the breakout, made three days later. The topic is chosen to reuse a proven hook.
- Thumbnail: orange archipelago, the bubble "Spreekt u Nederlands?", tag "350 YEARS OF DUTCH RULE", headline "So where's the Dutch?". It is the **same layout** as the breakout, with a different colour, number and language.

**What 4 extra minutes would carry [Inferred]:**
- Indonesia has far more islands and languages, and a company state (the VOC) with its own language policy (Malay as the trade language).
- The Japanese occupation and the choice of Indonesian at independence. These are more acts, not slower pacing.
- Confirm with the MP4.

**Lesson:** a hit becomes a **franchise template**. Same question, new empire, more acts if the history has them.

### 2.3 Typical recent upload: Paraguay / Guaraní (10:21) [Catalog + Inferred]

**Packaging:**
- Formula F: a majority against a tiny minority ("most… when only 2 %…").
- Thumbnail: magenta Paraguay, the bubble "Mba'éichapa?", tag "270 YEARS OF SPAIN", headline "Still speaking Guaraní".
- [Inferred] It flips the breakout. There, the colonial language failed; here, the native language won.
- [Inferred] It uses the same tag ("N YEARS OF SPAIN") so viewers of the Philippines video recognise the series.

**Performance:** 40K views in 4 days, about the channel's normal level once the novelty of the breakout passed.

---

## 3. Visual system (what to rebuild)

### 3.1 Look [Observed]

**Map:**
- Land: warm beige paper texture with a soft grain.
- Sea: deep teal-blue, a radial vignette darker at the edges, and a subtle paper grain.
- Coastlines: no outline stroke. Land is set apart by colour and a soft shadow on the sea.

**Highlighted regions:**
- Extruded in "3D": the same shape stacked 4–8 px down and to the right in a darker shade, plus a soft drop shadow.
- Flat fills:
  - red: the coloniser's language;
  - blue: the US and English;
  - teal, green, gold, orange: local languages.
- Grey with low saturation: "not this language".

**Cards:**
- Cream (#f6f1e6-ish), with 4–6 px rounded corners and a soft shadow.
- A tiny uppercase letter-spaced kicker in red or teal.
- The value in a heavy serif. Numbers are red, at a large size.

**Typography:**
- **Heavy display serif** for titles, numbers and word chips. Word chips are italic.
- A small sans-serif for captions and kickers. Captions are white pill boxes, bold sans, at the bottom centre.

**Other elements:**
- **Year chip:** top right, white box, black serif year. It updates whenever the narration names a year.
- **Portrait cards:** a line-drawn bust in an oval, with name and role (for example "FRIAR AND NAVIGATOR"). The mystery version is a silhouette with "?" and "MORE ON THEM SOON" / "NEXT".
- **Icons:** circular pins (house, church, school, book, clock), outlined in red or teal.

### 3.2 Camera [Observed]

- One continuous virtual camera. Pans and zooms are eased (slow in, slow out), about 1–2 s per move.
- No cuts. A topic change is made by moving the camera.
- The camera holds still while cards animate (minute 3 is 87 % still).
- Movement is spent on new geography; animated detail is spent on explanation.

---

## 4. Technique library

Each technique has: where it appears in the reference, when to use it, and how to build it with tools already in
this repo:
- the Playwright frame renderer plus ffmpeg (`render.mjs`, `maptour.mjs`);
- `d3-geo` + `topojson-client` + `world-atlas` (installed in `lingo/node_modules`);
- the Remotion map engine on branch `ccr-9383248a-do6ckh`: `channel/src/components/MapView.tsx`, `lib/camera.ts`, `GlobeIntro.tsx`, `Thumbnail.tsx`.

### 4.1 Maps

| Name | Seen at | Use it when | Build it |
|---|---|---|---|
| **Pattern Sweep** | 0:00–0:12 | Opening on "everyone else did X" | Countries fill red one after another (0.4 s fill each, 0.6 s apart); a dashed route draws from the coloniser; one native-language bubble. SVG paths from `world-atlas` 50m; animate `fill` and `stroke-dashoffset` per frame. |
| **Pattern Break Pan** | 0:12 | The exception enters | A 1.5 s eased pan from the pattern region to the exception, with both visible mid-move. Camera = `d3.geoNaturalEarth1()` scale and translate interpolated per frame (or `lib/camera.ts`). |
| **3D Extrude Country** | the whole video | Any highlighted country or region | Draw the path 6 times, offset +1 px x/y each, darker shade, then the top face; add `filter: drop-shadow(6px 8px 10px rgba(0,0,0,.35))`. Small islands get the same treatment. |
| **Recolour by Era** | 0:31, 4:31, 5:53, 6:00 | Who held the language changes (red → grey → blue) | Cross-fade the fill colour over 0.8 s, synced to the year chip. |
| **Route Line** | 0:00, 0:52, 1:10, 4:20, 5:16 | Ships, people, ideas moving | A curved great-circle path (`d3.geoInterpolate` → line); a dashed pattern for planned routes, solid with a moving dot for real voyages; the label is drawn along the curve. |
| **Region Patchwork** | 2:04–2:20 | "Many languages here" | Fill sub-national language regions with 5–6 muted hues. Needs language-area polygons: draw them by hand from a cited map (Glottolog or Ethnologue map, traced in SVG), or use Natural Earth admin-1 as an approximation. Say which on screen. |
| **Valley Close-up** | 2:10–2:16 | Showing density at a small scale | A 2.5× zoom on one region; ethnic and language labels as small serif italics. |
| **Pin Swarm** | 1:51, 2:42–2:50, 5:34 | "These were everywhere / nowhere" | Icon pins pop in with a 60 ms stagger (scale 0 → 1.1 → 1); each pin is a circle with an outline and a glyph. |
| **Mood Desaturation** | 6:09–6:46 | A tragedy section (war, epidemic, ban) | Shift land to grey-brown and the sea darker (CSS `filter: saturate(.25) sepia(.3)` on the map layer) over 1.5 s; restore it after the section. Use it at most once per video. |

### 4.2 Typography and cards

| Name | Seen at | Use it when | Build it |
|---|---|---|---|
| **Number Roll Card** | 0:14 (0 → 333), 2:00 (6,978+), 5:18 (≈500), 6:52 (≈400,000) | The paradox number or a key statistic | A cream card, red heavy-serif number counting up over 1.0 s with ease-out, small uppercase caption below. |
| **Stat Gauge Card** | 0:24 (<0.5 %), 4:02 (<3 %), 4:06 (3–10 %) | Percentages | Card, number on the right, a thin bar filling to the percentage. |
| **Dot Chart Card** | 1:32–1:44 | Comparing populations | Rows of dots, 1 dot = 1,000 people; red rows, then a big teal row that overflows. Dots pop in by row at 300 dots/s. |
| **Mystery Portrait** | 0:37, 2:34 | Plant a question for later | A silhouette card with "?" and "MORE ON THEM SOON"; repeat it with "NEXT" just before the payoff. |
| **Portrait Card** | 0:52, 1:00, 4:20, 4:30, 7:30 | Every named person | A line-drawn bust in an oval, name, role. For us: **a Wojak in an oval, drawn calm, matching the person's era** (our channel's face), or a public-domain portrait cut out and turned to line art (ffmpeg `edgedetect` + threshold). |
| **Word Chip** | 0:28, 2:22, 4:25, 4:33, 7:04–7:44 | Any word in the target language | A cream chip, a tiny coloured pill naming the language (SPANISH, TAGALOG), the word in italic serif, the gloss in quotes below. Arrow pairs ("a las dos → alas dos") show borrowing. |
| **Chip Row** | 7:14 (days of the week), 7:28 (surnames), 8:08 (recap) | Lists of loanwords | 4–7 chips in a bottom row, staggered 120 ms. |
| **Definition Card** | 7:14 "WHAT IS TAGALOG?", 7:50 "WHAT IS A CREOLE?" | Explain a term without stopping the story | A left-side card: kicker question, one-sentence answer, one context line. |
| **Document Card** | 3:08 (Doctrina Christiana, 1593), 7:34 (catalogue of 1849) | A primary source | A card with the title and year, two short labelled quotes (SPANISH / TAGALOG), a one-line note. For us: add a scan thumbnail from Commons if it is public domain. |
| **Quote Card** | 6:30 | An expert claim | A small card: kicker "HISTORIAN [NAME]", the claim in italic serif. Always name the source. |
| **Year Chip** | top right, whenever a year is spoken | Keep the timeline readable | A white box, heavy serif year; swap the value on the spoken word, using the word timing. |
| **Section Kicker** | 0:46, 1:28, 1:58, 2:38, 4:14, 4:46, 6:08, 6:56 | A new act | Top left, white pill, uppercase letter-spaced sans; slides in from the left at the act start. |
| **Caption Pill** | about 30 times | One-line takeaway of the sentence | Bottom centre, white pill, bold sans, 5–9 words. Never a full subtitle. |
| **Stamp** | 2:32 "IGNORED" | A verdict | Red outlined uppercase stamp, rotated −8°, punched in (scale 1.4 → 1 in 120 ms). |
| **Title Card** | 0:41–0:45 | After the hook | A cream panel in the centre, red kicker (channel name), 3-line serif title; fade in 0.4 s, hold 2.5 s, fade out 0.6 s. |

### 4.3 Photos and footage

- **[Observed] None.** The reference uses no photos, no film and no screenshots. Everything is vector map and cards.
- **For LingoDude:**
  - Optionally add one **Document Card with a real scan** per act, from public-domain Commons scans.
  - Optionally add **"Hear it" recording cards**. That is our edge; see §4.5.
  - No stock footage.

### 4.4 Transitions

| Name | Seen at | Build it |
|---|---|---|
| **Camera Move as Cut** | everywhere | Interpolate the projection between two framings over 1–2 s; overlays fade out 0.3 s before the move. |
| **Card Swap** | 1:32 → 1:44 | The old card fades and slides out 0.25 s; the new one pops in, scale 0.92 → 1, over 0.3 s. |
| **Recolour Wipe** | 4:31, 5:53 | Fill colour change spreading north to south (a delay proportional to latitude). |
| **Brand End Card** | 8:16 | Darken the final frame to 60 %; channel name in large serif; pill "NEXT: [next title]". |

### 4.5 Sound

| Name | Reference | LingoDude version |
|---|---|---|
| **Dry Narration** | [Observed] voice only, about 178 wpm, digital silence between sentences, −14.6 LUFS, mono | Narration at −16 LUFS (our loudness only goes down, never up), 160–175 wpm. |
| **No Music Bed** | [Observed] pauses are silent | Default: no music under narration. Optional: a very quiet bed (≤ −30 dB under the voice) only in the cold open and the outro. The owner has said loud music hurts. |
| **Breath Gap** | [Observed] 0.3–0.86 s gaps; 50 gaps over 0.4 s | Insert 0.35 s after normal sentences and 0.7 s after punch sentences or before a section kicker. |
| **Hear-It Moment** (ours, not in the reference) | n/a | When a word or phrase in the language appears, play the **real recording** (Lingua Libre / Commons) with the chip; narration pauses; the clip is levelled to the voice; credit it in the description. 3–6 per video. |
| **Soft UI ticks** (optional) | [Inferred] near-inaudible | If used: card pops at −28 dB, routes silent. No meme sounds (the owner's ban list applies). |

---

## 5. Repeatable structure (8–12 min)

**Rules for the runtime:**
- Every extra minute must come from **an extra cause, an extra piece of evidence or an extra payoff**, never a slower read.
- Word counts assume 165 wpm (LingoDude narration) and account for 4–8 s of Hear-It recordings per act.

| # | Section | 8 min | 10 min | 12 min | Words (10 min) | Job |
|---|---|---|---|---|---|---|
| 0 | **Cold open** | 0:00–0:42 | 0:00–0:45 | 0:00–0:50 | 115 | Pattern ×3 → break → paradox number → second number → the viewer's assumed answer → "but when I dug in" twist → Mystery Portrait plant → **Title Card** |
| 1 | **Setup: how they got there** | 0:42–1:40 | 0:45–2:00 | 0:50–2:20 | 200 | Geography, first arrival (person, date, route), why distance or structure matters. End on a mini-hook. |
| 2 | **Cause 1: who actually came** | 1:40–2:20 | 2:00–3:00 | 2:20–3:30 | 160 | Numbers (Dot Chart), the contrast country, "most people never met a speaker". |
| 3 | **Cause 2: the local reality** | 2:20–3:00 | 3:00–4:00 | 3:30–4:50 | 150 + 1 Hear-It | Local languages (Region Patchwork, greeting bubbles with **real recordings**), the rulers' failed fix (Stamp). |
| 4 | **Cause 3: the hidden cause (pays off the plant)** | 3:00–4:20 | 4:00–5:30 | 4:50–6:40 | 240 | The surprising actor or mechanism, shown as a flow animation. **Mid-video payoff at about 45 %.** First-person line ("this surprised me most"). |
| 5 | **Near reversal** | 4:20–5:10 | 5:30–6:30 | 6:40–7:50 | 160 | It almost worked: a group adopts the language, a milestone. Raises the stakes before the blow. |
| 6 | **Outside blow** | 5:10–6:20 | 6:30–7:50 | 7:50–9:30 | 210 | A new power, war or policy. Comparison cards (A against B), a recolour by era. |
| 7 | **Final blow and today's number** | 6:20–7:00 | 7:50–8:40 | 9:30–10:30 | 130 | The last stronghold falls (Mood Desaturation if tragic), the official end date, today's speaker count (Number Roll). |
| 8 | **"It's still there" twist** | 7:00–7:45 | 8:40–9:30 | 10:30–11:30 | 120 + 2–3 Hear-It | Loanwords, names, a creole or dialect, with **real recordings** of the words. |
| 9 | **Recap and outro** | 7:45–8:10 | 9:30–10:00 | 11:30–12:00 | 70 | The paradox number returns; a recap Chip Row; one personal closing line; End Card with NEXT. |

**Totals:**
- 10 min ≈ **1,550 narration words** plus about 40 s of recordings.
- 8 min ≈ 1,250 words.
- 12 min ≈ 1,850 words.

**Attention rules (measured from the reference):**
- A new visual event every **2–3 s**.
- A Section Kicker or a Number Roll every **30–80 s**.
- A short punch sentence (6 words or fewer) about every 40 s.
- The title lands at **7–9 %** of the runtime.
- The planted mystery pays off at **about 45 %**.
- A first-person surprise line 3–4 times.

---

## 6. Script and shot-list template

Write the script as a table, one row per narration sentence. Then turn it into `lingo/longform/<key>.json` (the
renderer contract in §7).

| # | Time | Narration (one sentence) | Visual | Motion | Audio | Assets needed |
|---|---|---|---|---|---|---|
| 1 | 0:00.0 | "…" | world map, [countries] filled | Pattern Sweep, 0.4 s per country | narration; Breath Gap 0.35 s | `world-atlas` ids |
| 2 | 0:04.8 | "…" | Route Line A→B, bubble "…" | dash draw 1.2 s | Hear-It: [file] 1.4 s | Commons recording + credit |
| … | | | | | | |

**Columns:**
- **Time:** taken from the narration word timings after recording (Whisper word timestamps, as in this analysis), never guessed.
- **Visual:** name the technique from §4 plus its content.
- **Motion:** duration and easing.
- **Audio:** narration, gap, Hear-It clip, optional tick.
- **Assets:** map ids, region polygons, portrait (Wojak prompt or Commons file), document scan, recordings, and the source for every number.

---

## 7. Production workflow

### 1. Research (day 1)
- Write the **paradox sentence** first: "[Power] did [X] for [N years], yet [outcome]".
- List 4–6 causes. Keep only those with a source.
- Keep a `research.md` per video: every number with its source URL and the exact wording. Prefer historians, censuses and Glottolog/Ethnologue to blogs.
- Mark ranges honestly ("3 to 10 percent, depending on who you ask"), as the reference does.

### 2. Script
- Fill §5 with real beats; write one sentence per row (§6).
- Read it aloud at 165 wpm and check the section lengths against §5.
- Plant one mystery in the cold open and pay it off at about 45 %.

### 3. Narration (owner decision, see §10)
- Record sentence by sentence. Trim to the speech and put a Breath Gap between sentences.
- Run `faster-whisper` with word timestamps to get the timing file.

### 4. Asset sourcing
- **Recordings:**
  - Lingua Libre / Commons for every word or phrase, with Whisper checks as in the other LingoDude builds.
  - Use the Playwright `getbig.js` workaround for Commons 429s.
  - Credits go to `out/<key>_credits.txt`.
- **Maps:** `world-atlas` 50m (countries) and 10m (small islands). Language regions are traced from a cited source.
- **Portraits:** calm Wojaks in ovals (Codex `gen.sh`), or line art from public-domain portraits.

### 5. Edit and render
- Build `longform.mjs` once by extending the `maptour.mjs` pattern (Playwright frames → ffmpeg, 1920×1080, 30 fps).
- Alternatively, port `MapView` and `camera` from the Remotion branch.
- Episode JSON:
  ```
  { title, key, beats:[{ t, say, camera:{center:[lon,lat], zoom}, fills:{ISO:color}, routes:[], cards:[], chips:[], kicker, year, hear:{file,at} }] }
  ```
  - `t` comes from the Whisper timing.
- Check stills with `--still` at each section start before the full render.

### 6. Review (quality checklist)
- [ ] Every number on screen has a source in `research.md`; ranges are shown as ranges.
- [ ] The title lands before 9 % of the runtime; the hook states the paradox number in the first 20 s.
- [ ] The planted mystery pays off; the "It's still there" twist exists or something stronger replaces it.
- [ ] A visual event every 2–3 s; no static stretch over 7 s, except the recap.
- [ ] Every foreign word on screen is in the right script, spelling and gloss; Hear-It clips are checked by Whisper or by ear.
- [ ] All recordings are credited (`<key>_credits.txt` → description); no synthesized speech unless the owner approved it, and labelled if so.
- [ ] Narration at −16 LUFS; no music bed over speech, or ≤ −30 dB under it; no banned sounds.
- [ ] Phone check: captions and chips readable on a 6" screen (review sheet).
- [ ] The thumbnail tells the gap, not the topic (§9.3); the title holds two contradicting facts.
- [ ] Description: sources list, recording credits, no `<` or `>`; metadata pasted in chat for the owner.

---

## 8. Worked example: opening (0:00–0:55) on an original topic

**Title:** "Arab Rule in Malta Ended in 1091. So Why Is Maltese Still Arabic at Its Core?"

**Facts to verify before final script:**
- Arab rule from 870; Norman conquest 1091. Sources: Wikipedia "Arabs in Malta", to be checked against a scholarly history of Malta.
- Gilberto Abbate's report of about 1240/41: 836 Muslim families, 250 Christian.
- Maltese descends from Siculo-Arabic.
- The Semitic share of the dictionary is 32–41 % (Brincat). Basic words are mostly Semitic.
- Maltese is the only Semitic official language of the EU and the only one written in Latin script.

**Recordings in the repo** (Lingua Libre, speaker GħawdxiVeru, CC BY-SA 4.0): aħna, ktieb, gżira, belt, ħobża,
aħmar, llejla.

| Time | Narration (165 wpm) | Visual | Motion | Audio |
|---|---|---|---|---|
| 0:00.0 | "When the Normans took Sicily from the Arabs, Sicily went back to speaking a Romance language." | Mediterranean map; Sicily green with a gold Arab-era tint fading to red | Pattern Sweep: tint fades over 0.8 s | narration |
| 0:05.0 | "Spain did the same after the Reconquista." | Iberia recolours north to south | Recolour Wipe 1.2 s; Year Chip "1492" | Breath Gap 0.35 |
| 0:08.0 | "So did Crete and the Balearic Islands." | Crete (Arab emirate 824–961) and the Balearics (Arab rule until the 1200s) flash once each | 2 pops, 0.3 s apart | |
| 0:11.0 | "Then there's Malta." | Camera pushes into a tiny dot south of Sicily; Malta extrudes in 3D, red | Pattern Break Pan 1.6 s | **Breath Gap 0.7** |
| 0:13.5 | "Arab rule there ended in 1091. That's more than nine hundred years ago." | Number Roll Card "0 → 1091 · ARAB RULE ENDED"; then a second line "935 YEARS AGO" | count over 1.0 s | |
| 0:18.5 | "And yet listen to how a Maltese speaker says 'island'." | Word Chip "MALTESE · gżira · 'island'" next to the island | chip pop 0.3 s | **Hear-It: `gżira`** (Lingua Libre) |
| 0:22.0 | "Arabic says jazīra." | Second chip "ARABIC · جزيرة · jazīra" with an arrow between the chips | chip pop | (no Arabic recording unless a real one is found; otherwise text only) |
| 0:24.5 | "Bread, book, red, tonight: the everyday words are Arabic at the root." | Chip Row: ħobża, ktieb, aħmar, llejla | stagger 120 ms | **Hear-It: ħobża, ktieb** (0.8 s each) |
| 0:30.5 | "I assumed it was just leftovers: a few words that survived, like Arabic words in Spanish." | Islands go grey; Caption Pill "Just a few leftover words?" | Recolour 0.8 s | |
| 0:35.5 | "It isn't. The grammar is Semitic too. And for 150 years after the Normans arrived, most families on the islands were still Muslim." | Document Card "GOVERNOR ABBATE'S REPORT · c. 1241 · 836 Muslim families · 250 Christian" | Card Swap | |
| 0:44.0 | "The people who saved the language, though, weren't Arabs at all." | **Mystery Portrait** "Who kept it alive? · MORE ON THEM SOON" | pop + slight wobble | **Breath Gap 0.7** |
| 0:48.5 | "To understand how, you have to look at where Malta sits on the map." | **Title Card** "LINGODUDE · Why Is Maltese Still Arabic at Its Core?" | fade 0.4, hold 2.5, fade 0.6 | |
| 0:52.0 | — | Kicker "AN ISLAND BETWEEN TWO WORLDS"; camera pulls out to show Tunisia 290 km away, Sicily 90 km away | Camera Move 1.5 s, two distance labels | |

**Planted mystery (pays off at about 45 %):** the Christian Maltese themselves kept speaking it after the Muslim
families were expelled, and it was the language of ordinary people. Italian served as the prestige language for
centuries, until the "Language Question" made Maltese official (1934, to verify).

---

## 9. Packaging rules

### 9.1 Titles
- Two contradicting facts in one question, with a number where possible.
- Use formulas A–G (§1.2) as **structures only**.
- Never reuse a TheLanguageMap title or topic word for word. Pick topics they haven't done; see `long-form-video-ideas.md`.

### 9.2 When the promise is delivered
- The thumbnail gap ("So where's the Spanish?") must be answered **in part within 35 s** and fully by the mid-video payoff.

### 9.3 Thumbnail for LingoDude long-form (`thumb_map.mjs`, to build)
- Their template: textured map, 3D country in one colour, a tag pill with the number, a 2–3 line serif headline that states the gap, and one bubble in the language.
- **LingoDude version:**
  - the same map composition, built with our own renderer;
  - the hook headline **in red with a white outline** (the owner's channel rule) instead of cream;
  - the white LingoDude name strip;
  - optionally one calm Wojak, small, looking at the country.
- One language object: a speech bubble in the language, or a word chip.

---

## 10. Open decisions for the owner

1. **The narrator.** LingoDude has had no narration so far. Options:
   - (a) the owner records the voice-over: real, and the best fit for the rules;
   - (b) local Piper TTS: free, but synthetic, so it needs the owner's OK and YouTube's altered-content box;
   - (c) a paid TTS: needs approval before any paid use.
2. **Thumbnail colour.** Keep the red hook (channel rule) on a TheLanguageMap-style map, or allow a cream headline for long-form only.
3. **Wojak portraits or line-art portraits** for historical figures.

# Handover: WWII Frontlines video pipeline → local session

Repo `anaqqad/Test`, branch **`claude/video-style-blueprint-589r90`** (all work is there; check it out first).
Owner PC: Windows, RTX 3090 Ti (24 GB). Read `CLAUDE.md` for the owner's rules: ask before any paid API,
never commit or print keys (use environment variables), commit Blender/video work to this repo only.

## The channel
- **WWII Frontlines** (@WWIIFrontlines-p3e). Reference/competitor channel: **WWII Box** (@wwiibox).
- Published so far:
  1. "A German POW Escaped in 1945. Then He Saw Chicago at Night." (`video/chicago-lights/`), 4 Oct 2026, 122 views
  2. "Japanese POWs Were Told to Die. Then America Gave Them Baseball." (`video/mccoy-baseball/`), 6 Oct 2026, 285 views
- Analytics after 3 weeks: 407 views, 15.8 h watch time, CTR 4.7–5.4 %, average view duration 41 % (good), 65–67 % still
  watching at 0:30. Views dropped to 0 because only 2 videos were posted. **Main lever now: post consistently (3–7 per week).**
  The Japanese angle beat the German one. Keep the "X Were Told … Then …" titles, under ~70 characters.

## Key docs (read these first)
- `VIDEO_STYLE_BLUEPRINT.md`: the reference format (script structure, pacing, narration rules). Do not copy its look.
- `HOUSE_STYLE.md`: **our** look ("Darkroom & Ledger"): photos as 35 mm contact frames with red grease-pencil marks, data and
  documents on graph-paper "field ledger" cards, black slug tabs, `[ STAND-IN · … ]` tags on footage that is not literal.
- `CHANNEL_ANALYSIS.md`: which titles and subjects work.
- `video/chicago-lights/README.md`: the full pipeline. `video/mccoy-baseball/` is the newest, cleanest copy to clone from.

## Pipeline (per episode, in `video/<slug>/`)
```
cp -r video/mccoy-baseball video/<new-slug>     # then clear script.md, audio/, build/, out/, assets/stills/, research/
# 1. research/sources.md  — every fact with a citation. No source, no video.
# 2. script.md            — ~1,250–1,450 words, one paragraph per scene, "## n. Act" markers (blueprint section 2)
python tools/tts_kokoro.py bm_george 1.2         # draft voice; final: tools/tts_cosyvoice.py (see chicago README, ~1–3 min on GPU)
python tools/align.py                            # word timings (faster-whisper)
bash tools/fetch_footage.sh && bash tools/shots.sh
python tools/sheet.py assets/footage/<film>.mp4 build/sheets/<film>.png 36   # contact sheets to pick shots
# 3. tools/plan.py: edit F (films), P (per-paragraph shots anchored to spoken words, cards, tags) and PHOTOS
python tools/plan.py                             # -> build/storyboard.json; target median shot ~4 s, card every 25–35 s
cd remotion && npm install && node render.mjs && cd ..       # overlays (needs a Chromium; set the path in render.mjs/remotion.config.ts)
python tools/assemble.py                         # -> out/<slug>.mp4 (1080p)
```
- Anchors in `plan.py` must match the **spoken** text (years are spelled out: "nineteen forty-three").
- Subscribe slug text: `CHANNEL` in `plan.py` ("Subscribe to WWII Frontlines").
- Washed-out films: add an entry to `GRADE` in `assemble.py`.
- QC before upload: `ffmpeg -i out/<slug>.mp4 -vf "fps=1/6,scale=320:180,tile=10x9" -frames:v 1 qc.png` and look at it.
  **Check for Nazi symbols in any German footage.** One slipped into McCoy and had to be replaced.
- Captions: see the SRT snippet in `video/mccoy-baseball/` (built from `audio/words.json`).
- Thumbnail: the owner generates the base image in ChatGPT (prompt in each `youtube.md`). Then run
  `python tools/thumbnail.py <image>`, or call `from_image(...)` from it, to add the caps question, red arrow and tag.
  Example: `video/mccoy-baseball/thumbnail/thumbnail_A.jpg`.
- Sources for footage and photos: archive.org (Prelinger, NARA `gov.archives.*`, Navy `NPC-*`) and Library of Congress
  (`loc.gov/pictures/...?fo=json`; download `…v.jpg`; only "No known restrictions"). Credit everything in `research/footage_credits.md`.

## Uploading (not built yet)
The cloud session had no YouTube access. To upload from the PC, use the YouTube Data API v3 (`videos.insert`,
`thumbnails.set`, `captions.insert`) with an OAuth client the owner creates in Google Cloud Console. The API is free (quota),
but keep the client secret and token in environment variables or a git-ignored file and **never commit them**. Alternatively
the owner uploads by hand using `youtube.md` (title, description with chapters, tags, pinned comment, "altered/synthetic
content = No": the owner's rule, since nothing shows realistic AI-generated people).

## Next episode (researched, not built): the secret interrogation camp
**Working title:** "Japanese POWs Were Sure They'd Be Tortured. Then They Were Served Sukiyaki."
(alternative: "Japanese POWs Expected Torture. America Served Them Sukiyaki.")

**Main source:** Arnold Krammer, "Japanese Prisoners of War in America," *Pacific Historical Review* 52, no. 1 (1983): 67–91.
Free copy: https://archive.org/details/JapanesePrisonersOfWarInAmerica (download the `_djvu.txt`). Supporting source:
Wikipedia, "Byron Hot Springs".

**Facts to use (all from Krammer unless noted):**
- Only 604 Japanese were taken prisoner in all the battles from the Java Sea to Tarawa and Makin. On Guadalcanal (1 Jan–15 Feb 1943)
  the XIV Corps took 84, 33 of them too sick or wounded to walk. An Army memo admitted it took "the promise of three days leave
  and some ice cream" to get U.S. soldiers to bring in the first live prisoner.
- From Sept 1942 most captives were handed to Australia. Those shipped to the U.S. were picked for intelligence value.
- Arrival at Angel Island (a former immigration quarantine station): deloused, numbered, examined. Nearly all asked that their
  families **not** be told they were alive ("better they be considered dead than dishonored").
- Angel Island menu, **16 September 1944** (Red Cross / State Dept inspection report): breakfast of sausages, rice, apples,
  coffee; **lunch of sukiyaki, cabbage salad, rice, caramel pudding**; dinner of spaghetti and hash, baked tomatoes, cakes, cocoa.
  "Better fed in captivity than in their own army."
- They played Mah-Jong and cards and listened to the gramophone, "whispering among themselves as they strove to understand the
  ulterior motives of their captors."
- **The three phases** (Army intelligence): 0–48 h, sure of torture and death, useless as sources. After several days, fear turns
  to gratitude and they talk freely for 10–14 days. Then they grow used to the food and kindness, get annoyed, and shut down.
- The most effective lever was not violence but the threat of **sending his name to his relatives in Japan**.
- After their requests to kill themselves were refused, many became model prisoners. A U.S. official (via Ruth Benedict,
  *The Chrysanthemum and the Sword*): old Army hands "located ammunition dumps… wrote our propaganda and flew with our bombing
  pilots to guide them to military targets… as if they had turned over a new page." One group said they had been "badly misled by
  the Emperor… and wished to fight back to Japan side by side with Allied soldiers" (NYT, 8 July 1945).
- Older prisoners told new arrivals to tell the truth, and some came back the next day to correct their own answers.
- Two secret interrogation centers: **Fort Hunt** near Washington ("P.O. Box 1142") and **Byron Hot Springs near Tracy, CA**
  ("P.O. Box 541"; also called Camp Tracy). Plans were labelled "Officers' School". Eight-foot fences, **hidden microphones in the
  cells**, barred windows. The camp's existence was revealed to the public only in mid-1947 (NYT, 11 July 1947).
- **45 interrogators**, many Japanese American (Nisei) linguists from the Army's Military Intelligence Service Language School
  in **Minnesota**. Each was assigned to one prisoner: sessions of 45–60 minutes, 2–3 a day, for a week or more. Reports every ~4 days,
  covering everything from clothing quality to the number of boiler rooms on the carrier *Hiryu*.
- **1,077** Japanese prisoners were interrogated at Tracy in 1944 (monthly figures in Krammer). Wikipedia: over 3,500 over the war.
- Byron Hot Springs itself (Wikipedia): a luxury resort from 1889, rebuilt in brick in 1913–14 and once a playground of movie
  stars and athletes. It closed in 1938, was leased by the government in 1941 as Camp Tracy and dismantled in 1945. The Greek
  Orthodox Church bought it in 1947. It stands abandoned today.
- The work program, if needed: Gen. Styer's "work like piss ants" order (needs a bleep or rephrasing); 15–20 % refused to work.

**Story arc:** cold open on a captured prisoner certain he'll be tortured, landing at Angel Island → he asks that his family not be
told → the meal (sukiyaki, caramel pudding) → the hidden purpose: the War Department wanted them to talk → the secret luxury-hotel
interrogation camp with hidden microphones → Nisei interrogators, one per prisoner → the three phases → the threat that worked
(writing to his family) → prisoners who turned and flew with U.S. bombers → the secret kept until 1947 → close: the empty hotel today.

**Footage and photos already downloaded in `video/mccoy-baseball/assets/` (re-fetch with its `tools/fetch_footage.sh`):** Japanese
POWs at Noumea (NPC-740/744), Iwo Jima Nisei capture (NPC-8680), Saipan prisoners (NPC-4511), *Know Your Enemy: Japan*,
*December 7th*, surrender on the Missouri, train and Pacific stills. Still to look for: Angel Island, San Francisco Bay, Nisei
MIS language school (Camp Savage/Fort Snelling) film or photos, Byron Hot Springs photos (check rights), bombers (B-24/B-29 film on archive.org).

**Thumbnail idea (ChatGPT):** a Japanese prisoner in "PW" fatigues at a table, staring at a steaming bowl of sukiyaki, with an
American officer in shadow behind him. Text: "WHY ARE THEY FEEDING ME?"

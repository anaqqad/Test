# Noor Channel Blueprint
### What "Max And Minni World" does, and an original series built on its mechanics

Prepared 8 Oct 2026. The frame sheets (`frames_*.jpg`) sit next to this file and back up the scene breakdowns.

---

## 0. How I analysed the videos, and what I could not check

- **You uploaded 4 files, but 2 are the same video.** The two "Ep 04" files have the same MD5 hash (`44d2c4c6…`). So there are **3 unique videos**: EP 03 (keys), Ep 04 (no trouble) and the cooking video.
- **Method:**
  - `ffprobe` for the technical specs.
  - `ffmpeg` scene-cut detection at thresholds 0.25 and 0.12 for shot boundaries.
  - Frames sampled every 0.5 s on timestamped contact sheets, plus some full-size key frames.
  - Audio spectrograms.
  - Automatic speech transcription with word timestamps (Whisper "small").
- **Limits:**
  - I read the videos frame by frame at 2 fps, not at every frame. Very short actions between samples could be missed.
  - Speech-to-text heard the girl's name as "Manny". It is almost certainly "Mini". Who speaks each line is my inference from voice pitch and what is on screen.
  - In the cooking video, the transcriber produced *"I'll see you in the next video, bye!"* over the last 3 s. That is a known Whisper error on music-only audio, so I treat that video as **having no confirmed dialogue**.
  - I cannot measure lip-sync accuracy from 0.5 s samples. I only note whether mouths move when lines are spoken.
  - The files are platform re-encodes (720p). Native generation resolution and model fingerprints are gone, so **all tool attributions below are inferences, not facts**.

Below, **[O]** means directly observable and **[I]** means inferred.

---

## 1. Analysis of the videos

### Video A: "EP 03 · Mini stole Papa's keys. BIG mistake. Or was it Papa's mistake for leaving them where…"

- **Specs [O]:**
  - 18.25 s, 720×1280 (9:16), 30 fps, AAC stereo.
  - 11 shots plus a black tail frame, so about **1.6 s per shot**.
- **Story:** Mini grabs Papa's car keys and runs. Papa chases her. She slides under a table and jumps into a pink toy Mercedes. She crashes through cushions and flowers. Papa looms over her, angry. She kisses him, and his anger melts.
- **Structure:** cold open mid-action → chase → escape → mess → confrontation → affection payoff.

| Time | Shot | What happens [O] | Camera [O] | Audio [O] |
|---|---|---|---|---|
| 0.00–~0.3 | 1a | Mini peeks around a gilded door frame holding keys, smirking | static, child height | rhythmic percussion starts |
| ~0.3–2.53 | 1b | Mini sprints toward camera down a sunlit marble hall; Papa appears behind her, chasing | tracking backward in front of her, low | footsteps/beat |
| 2.53–3.40 | 2 | Mini dives under an ornate gold table; Papa is blocked at the table | low angle through the table legs | — |
| 3.40–4.03 | 3 | Mini grins past the table edge with keys in hand (foreground blurred) | low close-up, shallow focus | — |
| 4.03–6.07 | 4 | Wide hall with staircase: Mini runs to a pink toy Mercedes and climbs in, Papa far behind | static wide | **Papa: "Mini, don't you dare!"** (4.3–5.6) |
| 6.07–7.27 | 5 | Close-up: Mini laughing at the wheel, Papa's legs and fist behind her | close-up, slight shake | **Mini: "Bye Papa!"** (6.1–6.4), mouth open/moving |
| 7.27–8.07 | 6 | Wide: Papa lunges, the car pulls away | wide | — |
| 8.07–9.97 | 7 | Car smashes through a low table of cushions and flowers; Papa chasing | tracking side-on | crash sounds |
| 9.97–14.00 | 8 | Low angle: Mini in the car at Papa's feet; camera reveals the giant Papa, who crosses his arms | low angle, tilt up / pull back | **Mini: "Wasn't me."** (9.9) · **Papa: "Mini."** (11.6) · **Mini: "Papa angry?"** (12.3) |
| 14.00–15.03 | 9 | Extreme close-up of Papa, furious | ECU, static | **Papa: "Very."** (14.3) |
| 15.03–16.10 | 10 | Papa bends down and lifts Mini out of the car | wide | — |
| 16.10–17.77 | 11 | Two-shot: Mini kisses Papa's cheek; his frown breaks into a reluctant smile | close-up | **"Mwah!"** (16.1) · **"Again!"** (16.9, speaker unclear [I]) |
| 17.77–18.25 | — | black | — | — |

- **Hook (0–2 s):** stolen keys plus a smirk, then a full sprint toward the lens. The "she's up to something" question comes before any context.
- **Characters [O]:**
  - **Mini:** about 4 years old, black hair in a long braid, pink salwar kameez with dupatta, gold jhumka earrings.
  - **Papa:** huge, exaggeratedly muscular Sikh man in a black turban, full black beard and black suit.
  - **Relationship [I]:** a doting but strict father and a fearless daughter who knows she wins.
- **Style [O]:**
  - Stylized 3D in the style of a feature-length animated film. Warm golden-hour light through tall windows.
  - Cream and gold marble palace interiors. Pink is the hero colour against a beige/gold world.
- **Expressions:** smirk, open-mouth laugh, "innocent" big eyes; Papa's thunderous ECU; the melt into a smile.
- **Humour, conflict, payoff:**
  - The size contrast: giant bodyguard dad versus tiny daughter.
  - A 4-year-old driving a toy Mercedes away from him.
  - "Wasn't me" while surrounded by destruction.
  - Payoff: affection beats authority.
- **Works without dialogue?** Mostly yes. Lines like "Wasn't me" and "Papa angry? / Very." add a joke but aren't needed to follow the story.
- **Ending and loop:** a warm end; "Again!" implies it will happen again. Medium loop potential, because the black tail breaks the loop.
- **Why share or follow [I]:**
  - It tags the "daddy's girl" experience ("this is my husband with our daughter").
  - It shows Punjabi/Sikh identity, which a big diaspora shares.
  - "EP 03" signals a series.

### Video B: "Ep 04 · Papa said 'No trouble.' Mini heard 'Challenge accepted.' To be continued…"

- **Specs [O]:**
  - 18.29 s, 720×1280 (9:16), 24 fps.
  - About 8 shots. One long final hold of 6.1 s, so about **2.3 s per shot**.
- **Story:** Papa, late for a meeting, tells Mini to go play. She promises "no trouble". As soon as he turns away she smirks. She takes heart stickers from a jewellery box, runs to his office and hides under his desk as his shoes arrive.
- **Structure:** rule → promise → secret smirk → preparation → infiltration → cliffhanger.

| Time | Shot | What happens [O] | Camera | Audio |
|---|---|---|---|---|
| 0.00–3.54 | 1 | Papa strides along, checking his wristwatch, with Mini trotting beside him; he points to a toy table | tracking with them, wide | **Papa: "Mini, meeting in 30 minutes. Go play."** · **Mini: "Okay, Papa. No trouble."** · "Promise." · "Okay." (0.0–3.9) |
| 3.54–5.00 | 2 | Papa walks off (back to camera); Mini turns to camera with a slow evil grin, holding a heart-studded box | medium close-up, Papa out of focus | music builds |
| 5.00–7.04 | 3 | Insert: hands take a heart-sticker sheet from a velvet-lined box (with a slight time jump) | top-down close-up | — |
| 7.04–9.08 | 4 | Mini hugs the box, eyes darting sideways, scheming | medium close-up, slight push in | — |
| 9.08–10.29 | 5 | Mini runs toward camera clutching the box | wide, tracking back | footsteps |
| 10.29–11.88 | 6 | Mini runs through tall double doors into Papa's office (desk, chair, arched windows) | wide from behind | — |
| 11.88–18.13 | 7 | Floor-level under the desk: Mini crawls in, then peeks out holding a heart sticker; Papa's polished shoes and trouser legs arrive and stop inches away | static at floor level | soft swishes/steps |
| 18.13–18.29 | — | end | — | — |

- **Hook:** a strong rule ("meeting in 30 minutes") plus a promise the audience knows will be broken. The 3.5 s evil-grin shot is the real hook.
- **Works without dialogue?** Partly. The watch gesture and the pointing carry it, but the "No trouble" promise is the joke.
- **Ending:** no payoff. It's a cliffhanger ("To be continued") that sends viewers to follow or open the next episode. Its loop potential is low, but it drives follows.
- **Why share or follow [I]:** the anticipation ("what is she going to do with those stickers in his meeting?") and the serial numbering.

### Video C: "Minni wants to cook / Max wants to cook…" (YouTube version)

- **Specs [O]:**
  - 20.18 s, **1276×718 (16:9)**, 24 fps.
  - About 14 shots, so about **1.4 s per shot**.
  - The filename's "Watch on YouTube maxandminniworld" plus the landscape frame suggest **[I]** a separate 16:9 cut for YouTube.
- **Story:** a standoff between Minni (hands on hips) and Papa, while Mama watches. Papa heads to the kitchen and Minni follows. They have a tug of war over a black apron, then cook side by side, Minni in a pink apron. Minni dumps flour, and Papa is left covered head to toe, beard white, staring deadpan.
- **Structure:** standoff → follow → struggle → truce/cooperation → accident → deadpan punchline.

| Time | Shot | What happens [O] | Camera |
|---|---|---|---|
| 0.00–3.04 | 1 | Minni (white/pink outfit, braid with a red tassel) with hands on hips, chin up; Papa leans down, glaring; **Mama** (red outfit) smiles in the background | medium, near static |
| 3.04–3.96 | 2 | Minni walks past the living-room sofa (Mama seated), Papa's arm in the foreground | medium |
| 3.96–4.96 | 3 | From behind: Papa walking, tiny Minni following | rear tracking |
| 4.96–8.00 | 4 | Wide gold-and-cream kitchen: Papa enters through an arch, Minni sneaks behind the island | static wide |
| 8.00–9.38 | 5–6 | Inserts: a big hand lifts a black apron; small hands grab and tug it | close-up |
| 9.38–11.58 | 7 | Wide tug of war: Papa standing, Minni sliding on the floor holding the apron | wide |
| 11.58–13.08 | 8 | Minni peeks over the apron fabric toward the lens, cheeky grin | close-up, apron as foreground frame |
| 13.08–14.17 | 9 | Papa, wearing the apron, faces camera; Minni now in a pink apron | wide frontal |
| 14.17–15.33 | 10 | Papa seriously adds an ingredient; Minni copies him | medium two-shot |
| 15.33–16.46 | 11 | Symmetrical frontal: both at the counter with a bowl | wide |
| 16.46–17.50 | 12 | Minni's hand dumps flour; it explodes | close-up |
| 17.50–19.67 | 13 | Papa is white with flour (beard and suit), deadpan; Minni looks innocent | wide frontal, **held 2.2 s** |
| 19.67–20.18 | 14 | end beat | — |

- **Audio [O]:**
  - Music throughout, quiet for the first 3 s (around −34 dB RMS), then louder (around −17 dB).
  - A broadband burst at about 16.8 s, which is the flour whoosh.
  - Voice-like harmonics around 9.5–12 s could be effort sounds during the tug of war. I can't confirm any words.
- **Works without dialogue?** Fully. This is the clearest proof that the format is visual.
- **Ending and loop:** the deadpan flour-covered Papa is the funniest single image of the three, and the kind of frame people screenshot and share. Good rewatch value.
- **Consistency notes [O]:** Minni's face is more doll-like here than in A and B, her outfit differs, and Papa's body is bulkier. **[I]** This suggests a different generation batch or model, so the character model isn't perfectly locked between episodes. That didn't stop the account from growing.

### Comparison table

| | A: EP 03 Keys | B: Ep 04 No trouble | C: Cooking |
|---|---|---|---|
| Length / aspect | 18.3 s / 9:16 | 18.3 s / 9:16 | 20.2 s / 16:9 |
| fps | 30 | 24 | 24 |
| Shots / average length | 11 / 1.6 s | 8 / 2.3 s | 14 / 1.4 s |
| Longest shot | 4.0 s (Papa reveal) | 6.1 s (under-desk cliffhanger) | 3.0 s (opening standoff) |
| Words spoken | ~13 | ~12 | 0 confirmed |
| Hook type | action in progress + smirk | rule + promise, then smirk | standoff + defiant pose |
| Mischief engine | theft + chase | infiltration | tug of war + accident |
| Big visual punchline | Papa's furious ECU | shoes beside the hidden girl | flour-covered deadpan Papa |
| Ending | affection melts anger | cliffhanger | deadpan gag |
| Works muted | mostly | partly | fully |
| Locations | marble hall, staircase, lounge | hall, toy table, office | living room, kitchen |
| Cast on screen | Mini, Papa | Mini, Papa | Minni, Papa, Mama |

---

## 2. The formula behind these videos

### 2.1 The recurring structure (taken from the three videos, not assumed)

All three videos follow the same seven beats.

1. **COLD OPEN IN CHARACTER (0–3 s).** There is no establishing shot. Each opens on the girl's attitude: a smirk with stolen keys, a promise, or hands on hips.
2. **THE RULE / PAPA'S TERRITORY (0–4 s).** Something belongs to Papa or is forbidden: his keys, his meeting, his kitchen and apron.
3. **THE SMIRK SHOT (around 3–5 s and again mid-video).** Every video has at least one close-up of the girl's mischievous face aimed toward the lens. That is the moment the audience "joins the plan".
4. **PHYSICAL MISCHIEF USING SIZE (5–12 s).** She goes under a table, into a toy car, under a desk, or hangs off an apron. Being tiny is her superpower.
5. **COLLATERAL MESS OR NEAR-CATCH (8–15 s).** Flying cushions and flowers, Papa's shoes inches away, a flour bomb.
6. **PAPA'S FACE (13–17 s).** An ECU of anger, or a deadpan stare. The giant's reaction is the punchline.
7. **RESOLUTION, ONE OF THREE (last 2–4 s):** (a) affection melts anger, (b) cliffhanger, (c) a held deadpan gag.

Short form: **ATTITUDE → RULE → SMIRK → TINY-BODY MISCHIEF → MESS / NEAR-CATCH → BIG REACTION → MELT / CLIFFHANGER / DEADPAN.**

### 2.2 Why it works

- **Archetypes:**
  - The gentle giant who is an authority figure and secretly a softie.
  - The tiny chaos agent who always wins.
  - The relationship is loving and the conflict is a game. Nobody is ever really in trouble.
- **Emotional triggers:**
  - Cuteness (big eyes, a tiny body).
  - "Daddy's girl" nostalgia and recognition.
  - Anticipation (the smirk).
  - Watching a powerful man get beaten by a small child.
  - Identity pride (a Sikh/Punjabi family, which is rarely shown in animation).
  - Aspiration (the palace).
- **Hooks:** the girl's face or posture in the first second, plus a title that tells the joke ("Papa said X, Mini heard Y").
- **Visual consistency:** a fixed silhouette and colour code. Pink girl, black giant, warm gold world. You can recognise the characters from the thumbnail alone.
- **Pacing:** 1.4–2.3 s per shot; the punchline shot is held 2–6 s, the only long shot.
- **Reusable assets:** the same mansion hall, kitchen, office and lounge; props are household objects (keys, apron, flour, stickers, toy car).
- **Why viewers get attached:** the same two characters, numbered episodes, a consistent dynamic, and a warm ending that rewards watching.
- **Why it can run for hundreds of episodes:** episodes are *(any household object or rule) × (girl's mischief) × (Papa's reaction)*. That combination never runs out, and holidays and life events add more.

### 2.3 Essential and optional production details

| Essential (copy the mechanic) | Optional (don't copy, just style) |
|---|---|
| 2 recognisable characters with a strong contrast in size, power or temperament | The luxury palace setting |
| A fixed outfit and colour code per character | A specific ethnicity or culture (use your own) |
| The smirk close-up toward the lens | Native lip-sync (most lines play over wide or back-turned shots) |
| Shots of 1.4–2.5 s; the punchline shot held 2+ s | A separate 16:9 version |
| Under 15 words of dialogue; the story reads muted | Exact music genre |
| A title that states the joke, plus episode numbering | Insert shots (useful but not required) |
| Warm, high-key "animated film" lighting | Perfect consistency between episodes (C shows drift and still did fine) |

---

## 3. How they probably produce it (inferred AI pipeline)

**Evidence I can point to [O]:**
- The characters are identical *within* each episode but drift *between* episodes (Minni's face and Papa's bulk in C). That means per-shot generation from reference images, not a 3D rig.
- Shots are 0.6–4 s and never longer than about 6 s, which fits 5–6 s generation clips trimmed in the edit.
- A has a different frame rate (30 fps) from B and C (24 fps). That points to different tools or export settings across episodes.
- Spoken lines are 1–5 words. Most fall on wide shots, back-turned shots or off-screen speakers. Two lines fall on close-ups where the mouth is open or moving ("Bye Papa!", "Very.").
- Inserts (hands with stickers, apron, flour) are cheap, consistency-safe shots.

**Likely pipeline [I]:**
1. **Character reference sheets.** One hero image per character (front, 3/4, full body) made in an image model that holds identity well (GPT-image, Midjourney with character reference, Flux/Kontext, Seedream or Gemini image editing are all plausible).
2. **Keyframes.** For each shot, an image made from a reference image plus a location plate (edit-type generation that keeps the character).
3. **Image-to-video.** Each keyframe animated for 5 s, then trimmed. Fast, physical motion (sprinting, toy car crash, flour explosion) with stable faces points to a current top-tier model. **Kling, Seedance 2.x, Veo 3.x and Hailuo can all do this; I can't tell which was used.**
4. **Voices.** Either native audio from the video model (Veo 3.x, Seedance 2.x and newer Kling versions can generate speech with lip movement) or TTS (e.g. ElevenLabs) placed over shots where lips don't need to match.
5. **Music and SFX.** A library track or AI music (Suno/Udio-type) under everything, plus stock whooshes and impacts.
6. **Edit.** CapCut or Premiere: fast cuts, sound design, title text, one master with a 9:16 crop and a 16:9 version (C).
7. **Export/upscale.** Possibly a 1080p upscale; the uploaded files are platform re-encodes at 720p, so this can't be checked.

### Tool evaluation for your channel

| Tool | Strength | Weakness | Use it for |
|---|---|---|---|
| **Seedance 2.0 / 2.5** (ByteDance; e.g. via fal) | Strong motion and identity, multi-reference input, native audio | ~$0.24–0.30/s at 720p on fal (2.0); 1080p ~$0.68/s | Hero shots, dialogue close-ups |
| **Kling 2.5 Turbo** | Very cheap (aggregators list ~$0.04–0.07/s on resellers), good physics | Faces can drift on long moves; audio depends on version | Action, wide and running shots |
| **MiniMax Hailuo** | Good physical comedy (falls, slides), cheap | Less fine control of the face | Slapstick beats |
| **Veo 3.1** | Best native dialogue plus lip-sync and SFX | ~$0.15/s (Fast) to $0.40/s (Standard with audio), per third-party trackers | Lines spoken on close-ups |
| **ComfyUI + Wan 2.2 (local)** | You have an RTX 3090 Ti (24 GB): almost no cost per clip, you can train a character LoRA for near-perfect consistency | Slower (estimate several minutes per 5 s clip at 720p; **measure it**), setup time | Bulk shots, B-roll, a consistency LoRA |

*Prices come from fal model pages and third-party aggregators as of Oct 2026, and they change often. Check before budgeting.*

### Cost and time per ~20 s episode (assumptions stated)

Assumptions:
- 11 shots, each generated as a 5 s clip.
- An average of 2.5 attempts per shot, so about **140 s of generated video**.
- Keyframes: 11 shots × ~4 image tries = ~44 images at ~$0.03–0.04 each = **~$1.5–2**.

| Video setup | Video cost | + images/audio | **Per episode** | 30 episodes/month |
|---|---|---|---|---|
| Budget: Kling 2.5 Turbo for everything | ~$6–10 | ~$2–3 | **~$8–13** | ~$250–400 |
| **Hybrid (recommended):** Kling/local Wan for 8 action/wide shots, Seedance or Veo for 3 close-ups | ~$10–18 | ~$2–3 | **~$12–21** | ~$360–630 |
| Seedance 2.0 Fast for everything | ~$34 | ~$2–3 | **~$36** | ~$1,100 |
| Veo 3.1 Standard with audio for everything | ~$56 | ~$2–3 | **~$58** | ~$1,750 |
| Local Wan 2.2 on your 3090 Ti | electricity only | ~$2–3 | **~$3** | ~$90, but GPU time is the limit |

Fixed monthly costs:
- Voices: ~$5–22 a month (an ElevenLabs-type plan).
- Music: ~$10 a month (Suno-type) or a library subscription.
- Check that every plan **allows commercial use**.

Time per episode:
- First episodes: about **3 h** (script 15 min, keyframes 45 min, generation 60–90 min mostly waiting, audio 15 min, edit 30–45 min).
- After about 10 episodes with templates: **~1.5 h**.
- With the n8n automation in §7.4: **~45 min of human time** (choosing takes and the final edit).

---

## 4. Five original concepts starring Noor

None of these copies the father-and-daughter, palace or pink setup. Each changes the **relationship dynamic**, not just the costume.

### Concept 1: **Noor & Teta**
- **Characters:** Noor, 5, a confident little schemer. Teta Salma, 78, her tiny, glamorous, sneaky grandmother. Mama, the house rule-maker, is **never fully shown**: only her voice, her fuzzy pink slippers or her hand. Mishmish is the fat, judgemental ginger cat.
- **Relationship:** *partners in crime.* The reference has the child against the authority figure; here the child and the grandparent team up against the rules. Their love for each other is never in question.
- **Premise:** every episode, Noor and Teta break one of Mama's rules together and try not to get caught. Catchphrase: **"Mama doesn't need to know." 🤫**
- **Visual style:** cosy, colourful stylized 3D. A Levantine stone house with patterned cement tiles, a lemon tree in the courtyard, copper pots and arched windows. Noor is lemon yellow and Teta is emerald and plum. The look is homely and textured, not palace luxury.
- **Emotional appeal:** grandparent love (everyone's "send this to Teta/Nana" moment), cuteness, and old people doing young things, which is already a proven trend.
- **Humour and conflict:** heists, cover-ups, the cat getting blamed, Teta's bottomless handbag, near-catches when the slippers approach.
- **Audience:** women 18–45, mothers, grandchildren, the Arab and Mediterranean diaspora in the US, Canada and Europe, plus a general audience (the story reads muted).
- **10 episode ideas:**
  1. Cookie jar heist
  2. Teta's bottomless handbag
  3. Thunderstorm blanket fort
  4. Smuggling knafeh past Mama's diet rule
  5. Teta learns a TikTok dance and outdances Noor
  6. The broken vase gets superglued (to Teta's hand)
  7. Sneaking up to the roof to see fireworks
  8. Teta does Noor's hair for picture day (a giant bouffant)
  9. Hide-and-seek where Teta naps for 3 hours
  10. Mother's Day breakfast disaster
- **Strengths:** a fresh dynamic, two proven trends in one (cute kid and funny grandma), only 2 characters to keep consistent, brand-friendly (food, family, holidays).
- **Weaknesses:** less physical size contrast than a giant dad; Teta has to look clearly *animated* and charming, not creepy.
- **AI difficulty:** low to medium. **100+ episodes:** yes, easily: rules × heists × holidays.

### Concept 2: **Noor & Jamal**
- **Characters:** Noor, 6, and **Jamal**, a fluffy, clumsy baby camel who lives in her family's city apartment.
- **Relationship:** a girl and her oversized pet. She is the responsible one; Jamal is the chaos.
- **Premise:** a camel calf does not fit an apartment, a school or an elevator, and Noor keeps covering for him.
- **Style:** bright, rounded stylized 3D, a pastel city apartment, rooftop gardens.
- **Appeal:** animal cuteness plus the absurd. It works for any language.
- **Humour:** physical comedy from the size problem (stuck in doors, eating plants, bath time).
- **Audience:** a global, broad family audience.
- **10 ideas:**
  1. Jamal in the elevator
  2. Bath time
  3. Show-and-tell at school
  4. Jamal eats Mama's plants
  5. First snow
  6. Jealous of a new kitten
  7. Birthday cake
  8. Playground slide
  9. Stuck in the doorway
  10. Jamal saves Noor's runaway balloon
- **Strengths:** a very memorable animal, no dialogue needed.
- **Weaknesses:** animal and child touching each other is harder for AI; a 4-legged character drifts more.
- **Difficulty:** medium to high. **100+ episodes:** yes, but the jokes can get repetitive.

### Concept 3: **Big Sister Noor**
- **Characters:** Noor, 6, and her baby brother **Zain**, 1, who can't talk but is an evil genius. Parents are off-screen.
- **Relationship:** sibling rivalry that always turns protective.
- **Premise:** Noor wanted a sister and got Zain. Every episode she tries to get rid of him, outsmart him or win attention back, and ends up saving him.
- **Style:** warm, modern family home, soft pastels.
- **Appeal:** older-sibling recognition ("this is me and my brother") and the protective payoff.
- **Humour:** the baby outsmarting the 6-year-old, jealousy, copying.
- **Audience:** parents of 2+ kids, older siblings.
- **10 ideas:**
  1. Trying to "return" Zain to the hospital
  2. Zain's first word is "Noor"
  3. 5 minutes of babysitting
  4. The stolen toy
  5. The copycat baby
  6. Bath war
  7. Zain only listens to Noor
  8. Sibling photo shoot
  9. Noor protects Zain at the playground
  10. Zain's first steps toward Noor
- **Strengths:** a big emotional hook, easy to relate to.
- **Weaknesses:** the sibling-rivalry niche is crowded; less distinctive.
- **Difficulty:** medium (baby proportions drift). **100+ episodes:** yes.

### Concept 4: **Little Boss Noor**
- **Characters:** Noor, 5, the self-appointed CEO of her **Uncle Fadi**'s tiny bakery in a busy souk. Fadi is a lanky, anxious baker.
- **Relationship:** the kid as boss and the adult as employee (a role reversal).
- **Premise:** a workplace sitcom with a 5-year-old in charge: pricing, customer service, "marketing".
- **Style:** a vibrant market, stacks of bread, wood-fired oven glow.
- **Appeal:** office humour plus a cute kid; food content.
- **Humour:** Noor's business logic, rush hour, competitor shops.
- **Audience:** adults who work, food lovers.
- **10 ideas:**
  1. Noor sets the prices
  2. Rush hour
  3. Health inspector
  4. Viral marketing stunt
  5. Oven alarm
  6. Giant dough monster
  7. Rival bakery
  8. Delivery on a scooter
  9. Employee of the month (it's Noor)
  10. Uncle Fadi's day off
- **Strengths:** natural food-brand tie-ins.
- **Weaknesses:** crowds and extra characters make consistency and cost harder.
- **Difficulty:** medium to high. **100+ episodes:** yes.

### Concept 5: **Noor & the Bronze Lion**
- **Characters:** Noor, 7, daughter of a museum curator, and **Assad**, a small 3,000-year-old bronze lion statue who comes alive only for her after closing time.
- **Relationship:** an ancient, grumpy, proud friend and a curious child.
- **Premise:** night adventures in a history museum. Assad reacts to the modern world; Noor learns history.
- **Style:** a moody, warm museum at night, flashlight beams, exhibits.
- **Appeal:** wonder, light education, and it fits your history skills.
- **Humour:** an ancient creature meets pizza, phones, the guard.
- **Audience:** families, history fans.
- **10 ideas:**
  1. Assad meets a house cat
  2. The mummy-wrap mix-up
  3. Rearranged dinosaur bones
  4. Guard almost catches them
  5. Assad tries pizza
  6. Gift-shop chaos
  7. The Roman coin hunt
  8. Museum sleepover
  9. Assad's 3,000th birthday
  10. The new statue is jealous
- **Strengths:** original, educational, opens up longer YouTube content.
- **Weaknesses:** night lighting, metal textures and many props are hard for AI and expensive. Fantasy needs more explaining.
- **Difficulty:** high. **100+ episodes:** yes.

---

## 5. Scoring the concepts

| Criterion (1–10) | 1 Noor & Teta | 2 Noor & Jamal | 3 Big Sister | 4 Little Boss | 5 Bronze Lion |
|---|---|---|---|---|---|
| Viral potential | 8 | 8 | 7 | 7 | 7 |
| Emotional connection | 9 | 7 | 8 | 6 | 7 |
| Character memorability | 9 | 9 | 6 | 7 | 8 |
| Originality | 8 | 8 | 5 | 7 | 8 |
| Ease of AI generation | 8 | 6 | 7 | 6 | 4 |
| Character consistency | 8 | 7 | 7 | 6 | 5 |
| Production cost (10 = cheapest) | 8 | 7 | 8 | 6 | 5 |
| Long-term storytelling | 9 | 7 | 8 | 8 | 8 |
| Reels/Shorts fit | 9 | 8 | 8 | 7 | 7 |
| **Total / 90** | **76** | **67** | **64** | **60** | **59** |

**Winner: Noor & Teta.** The reasons:

1. It keeps the engine that works: a small character, a big reaction, a smirk, a mess and a warm ending. But it changes the relationship from *child against authority* to *child and grandparent against authority*. That is a new dynamic, not a costume swap.
2. It combines two formats that already grow quickly: cute kid storytelling and the funny, glamorous grandma (the Granny Spills effect).
3. Mama is never fully shown. That makes her funnier (the slippers become a symbol everyone recognises) and leaves **only 2 human characters to keep consistent**, which saves money and effort.
4. Every household has a rulebook, so there are endless episodes, plus Ramadan, Eid, Christmas, back to school and Mother's Day.
5. Brands will pay for it: food, baking, family brands, toys, kids' fashion, holiday campaigns.

---

## 6. Channel blueprint: Noor & Teta

### A. Brand identity

**Name options:**
1. Noor & Teta
2. Mama Doesn't Need to Know
3. Partners in Crumbs
4. Shhh, Teta!
5. The Teta Files
6. Teta's Little Accomplice
7. Lemon House Stories
8. Noor and Teta Club
9. Team Teta
10. Tiny Noor, Tiny Teta

**Recommended:** **Noor & Teta**, handle `@noorandteta` (check availability; fallbacks `@noor.and.teta`, `@noorandtetaworld`). Use the tagline everywhere: **"Mama doesn't need to know 🤫"**.

**Bio (150 characters max):**
`Noor (5) + Teta (78) = partners in crime 🤫🍋 | Mama doesn't need to know | New episode daily | AI-animated series`

**Profile picture:** Noor and Teta cheek to cheek, both with a finger to their lips ("Shhh"), mischievous eyes toward the viewer, on a flat lemon-yellow background. Their faces fill 80% of the circle so it reads at small sizes.

**Logo:** the wordmark "Noor & Teta" in a rounded, hand-lettered font. The "&" is drawn as Teta's round glasses, with a small lemon above the "N".

**Palette:**

| Role | Colour | Hex |
|---|---|---|
| Noor (hero) | Lemon yellow | `#F4C430` |
| Teta | Emerald | `#1F7A5C` |
| Teta's handbag | Plum | `#6B2D5C` |
| World | Terracotta | `#C8553D` |
| World | Cream stone | `#FFF4E0` |
| Accent / Mama | Slipper pink | `#F7A1C4` |

**Visual identity:**
- Warm late-afternoon light and patterned blue-and-terracotta cement tiles in every interior.
- A lemon tree visible through at least one window.
- Every cover frame has the smirk or a "Shhh".
- Title cards: yellow text with a dark outline in the top third, never covering faces.

### B. Character bible

#### Noor
- **Age:** 5.
- **Look:**
  - Round face, big warm brown eyes, light olive-tan skin, rosy cheeks.
  - A **small gap between her front teeth**.
  - Dark-brown curly hair in **two high puffs tied with yellow ribbons**.
- **Clothes (season 1, never change):** a mustard-yellow pinafore dress over a white T-shirt with a tiny lemon print, white socks, **red sneakers**.
- **Personality:** confident, theatrical, loyal, a negotiator.
- **Strengths:** brave, clever, small enough to fit anywhere.
- **Flaws:** can't keep a straight face, terrible at winking (blinks both eyes), and crumbs always give her away.
- **Relationships:** Teta's accomplice, scared of the slippers, rival to Mishmish.
- **Signature expressions:**
  1. The smirk (one corner of the mouth, eyebrows down)
  2. "Shhh", finger to lips
  3. The failed double-blink wink
  4. Angelic hands-folded innocence
  5. Jaw drop
- **Generation prompt:**
  ```
  Character reference sheet of NOOR: a 5-year-old girl, round face, big warm brown eyes, light olive-tan skin, rosy cheeks, small gap between her front teeth, dark-brown curly hair in two high puffs tied with yellow ribbons, mustard-yellow pinafore dress over a white t-shirt with tiny lemon print, white socks, red sneakers. Stylized 3D animated feature-film character design, soft subsurface skin, clean appealing shapes, expressive big eyes. Turnaround: front view, 3/4 view, side view, back view, full body, neutral pose, plus 4 face close-ups: smirk, finger-to-lips "shhh", jaw drop, angelic innocent. Plain light-grey background, even studio lighting, no text, no watermark.
  ```
- **Consistency rules:**
  - Two puffs, always (never a braid or ponytail).
  - Yellow ribbons, gap teeth and red sneakers are always visible when framed.
  - Height reaches Teta's shoulder.
  - Never pink as a main colour (that belongs to Mama's slippers).

#### Teta Salma
- **Age:** 78.
- **Look:**
  - **Petite**, only about a head taller than Noor.
  - A voluminous **silver bouffant**.
  - Oversized **round tortoiseshell glasses**.
  - Red lipstick, gold hoop earrings, laugh lines.
- **Clothes:** an **emerald velvet cardigan** over a cream blouse, a long plum skirt, gold bangles stacked on both wrists (they jingle), low burgundy heels. She always carries a **plum vintage leather handbag with a gold clasp**.
- **Personality:** glamorous, competitive, sneaky, dramatic, deeply soft.
- **Strengths:** her handbag holds anything, she can do 'innocent' perfectly, and she's surprisingly fast.
- **Flaws:** falls asleep mid-mission, can't resist sweets, terrible at technology.
- **Relationships:** Noor's partner in crime. She is Mama's mother-in-law or mother, and pretends to be scared of her. She is Mishmish's enabler.
- **Signature expressions:**
  1. Glasses slowly lowered (the "I have a plan" look)
  2. Innocent tea sip with the pinky raised
  3. The perfect wink
  4. "Shhh"
  5. Weightlifter strain face
- **Generation prompt:**
  ```
  Character reference sheet of TETA SALMA: a petite 78-year-old grandmother, only slightly taller than a 5-year-old, warm olive skin with soft wrinkles and laugh lines, voluminous silver bouffant hair, oversized round tortoiseshell glasses, red lipstick, gold hoop earrings, stacked gold bangles on both wrists, emerald-green velvet cardigan over a cream blouse, long plum skirt, low burgundy heels, carrying a plum vintage leather handbag with a gold clasp. Stylized 3D animated feature-film character design, charming and glamorous, soft subsurface skin, expressive eyes behind glasses. Turnaround: front, 3/4, side, back, full body, plus 4 face close-ups: glasses lowered scheming look, innocent tea sip with pinky up, wink, finger-to-lips "shhh". Plain light-grey background, even studio lighting, no text, no watermark.
  ```
- **Consistency rules:**
  - Glasses always on her face (unless the joke is the lost glasses).
  - Handbag on her arm in every shot unless it's being used.
  - Bangles visible.
  - Silver hair keeps the same volume.
  - Never taller than a kitchen counter plus a head.

#### Mama (partial character)
- **Shown only as:** lower legs in light-blue jeans with **fuzzy pink slippers**, a hand with a gold ring and a pink sleeve, a shadow on a wall, and her voice. **Her face is never shown.** That keeps her mysterious, saves effort, and the slippers become the series symbol.
- **Prompt fragment:**
  ```
  only Mama's lower legs visible: light-blue jeans and fuzzy pink slippers, face never shown
  ```
- **Voice:** warm but firm, mid-30s, a light accent is fine.

#### Mishmish (the cat)
- **Look:** an overweight ginger tabby with a white chest patch and half-closed unimpressed eyes.
- **Role:** witness, scapegoat and snitch. He reacts in a cut-away and gets blamed.
- **Prompt:**
  ```
  MISHMISH: an overweight ginger tabby cat with a white chest patch and half-closed unimpressed eyes, stylized 3D animated
  ```

### C. Storytelling system

**Episode structure (adapted from §2.1):**

| Beat | Time (20 s episode) | Purpose |
|---|---|---|
| 1. SHHH HOOK | 0–2 s | Both faces, or the smirk, toward the lens. The secret starts now. |
| 2. MAMA'S RULE | 2–4 s | A note, the slippers or Mama's voice sets the forbidden thing |
| 3. THE PLAN | 4–7 s | Teta lowers her glasses and the handbag opens: tools come out |
| 4. THE HEIST | 7–12 s | 2–3 fast shots of physical mischief using their small size |
| 5. NEAR-CATCH | 12–15 s | Slippers approach, music cuts out, faces freeze toward camera |
| 6. COVER-UP / PAYOFF | 15–18 s | The impossible reset (tea sip, angelic hands), a twist, or the cat blamed |
| 7. BUTTON | 18–20 s | Wink, failed wink, or "Mama doesn't need to know." Matches the hook so it loops. |

- **Length:** 16–22 s (the reference videos ran 18–20 s).
- **Shots:** 9–12, each 1.5–2.5 s; the payoff shot is held 2–3 s.
- **Dialogue:** 12 words or fewer per episode. Every episode has to work muted.

**Hook library (first 1.5 s):**
1. Two faces peeking over a counter: "Shhh."
2. Teta slowly lowers her glasses at the lens.
3. Extreme close-up of the slippers stepping into frame, then a smash cut.
4. Noor with crumbs on her face, eyes darting.
5. Handbag clasp click, golden glow.
6. A note on the fridge: "NO ___ — MAMA".
7. Teta in a full disguise (sunglasses, scarf) at a doorway.
8. Mishmish staring at the lens, judging.
9. Noor on Teta's shoulders, reaching for something.
10. A crash sound over a black frame, then the reveal of the mess.
11. Teta and Noor shaking hands like a business deal.
12. Noor holding up a hand-drawn "plan" map.
13. Both diving behind the sofa at the same moment.
14. Teta's alarm clock reads 3:00 AM; both eyes open in the dark.
15. "Mama said no." "Mama's not here." (two lines over a two-shot)

**Emotional triggers:**
- Cuteness and mischief (Noor).
- Grandparent love (Teta).
- Suspense (the slippers).
- Relief and laughter (the cover-up).
- Tenderness (about 1 in 5 episodes is a heart episode).

**Running jokes:**
- The bottomless handbag.
- Noor's double-blink wink.
- The cat gets blamed.
- The slippers' "shf… shf…" sound.
- Teta's pinky-up tea sip as the universal alibi.
- Teta falling asleep mid-mission.
- Crumbs give Noor away.

**Endings (rotate them):**
- **A.** They get away with it (wink).
- **B.** They get caught but Mama secretly joins in (her hand takes a cookie).
- **C.** The cat takes the fall.
- **D.** A tender hug or sleep.
- **E.** "To be continued" two-parters (1 per week).

#### 30 episodes

| # | Title | Twist / payoff | Ending |
|---|---|---|---|
| 1 | The Cookie Jar Heist | the cat is blamed | C |
| 2 | Teta's Bottomless Handbag | the cat pops out of the bag | A |
| 3 | Thunder | Teta is scared too; blanket fort | D |
| 4 | Operation Knafeh | Mama put Teta on a diet; Noor smuggles knafeh in her backpack | A |
| 5 | Teta Learns the Dance | Teta outdances Noor; Mama walks in, joins | B |
| 6 | The Vase | superglued to Teta's hand | A |
| 7 | Rooftop Fireworks (pt 1) | sneaking out of bed | E |
| 8 | Rooftop Fireworks (pt 2) | Mama is already on the roof | B |
| 9 | Picture-Day Hair | Noor gets Teta's bouffant | A |
| 10 | Hide-and-Seek | Teta sleeps for 3 hours in the closet | C |
| 11 | Glasses Hunt | they're on her head, and Noor is wearing a second pair | A |
| 12 | The Vegetable Plan | broccoli hidden in the cat's bowl; cat's revenge | C |
| 13 | Eidiyeh Negotiation | a business-deal parody over Eid money | A |
| 14 | Video Call Disaster | they turn on a potato filter on Mama's work call | B |
| 15 | Supermarket Racer | Teta drives the shopping cart like a race car | A |
| 16 | The Spelling Test | Teta "helps" (badly) | A |
| 17 | Teta's 1968 Photo | Teta was a disco queen; dance flashback | D |
| 18 | The Bake-Off | Noor vs. Teta; Mishmish judges and eats both | C |
| 19 | Tooth Fairy Stakeout | Teta falls asleep; Noor leaves her a coin | D |
| 20 | First Day of School | Teta in disguise at the gate | D |
| 21 | Playground Legend | Teta takes the big slide | A |
| 22 | The Quiet Game | the slippers test their silence | B |
| 23 | Beach Day | Teta builds a sandcastle palace with a moat | A |
| 24 | Halloween | Teta's costume scares Noor | A |
| 25 | Teta's Birthday (pt 1) | the surprise cake catches fire | E |
| 26 | Teta's Birthday (pt 2) | the rescue: a cake shaped like the handbag | D |
| 27 | Mother's Day Breakfast | the kitchen explodes, Mama loves it | D |
| 28 | Doctor Visit | Teta is afraid of the injection; Noor holds her hand | D |
| 29 | Ramadan Suhoor Alarm | Noor's pot-and-spoon alarm wakes the whole street | B |
| 30 | Snow Day | they make a snow-Teta, and Mama's slippers get soaked | A |

### D. Production workflow

#### D.1 One-time setup (about 1 day)
1. Generate the **character sheets** with the prompts in §6.B. Make about 20 variations, pick the best, then generate 6–8 extra angles of the chosen design (references work better with several images).
2. Optional on your 3090 Ti: **train a character LoRA** for Noor and for Teta (Flux or Wan, 20–30 images each). This gives the most stable faces at no cost per episode.
3. Generate **location plates**: 2–3 empty camera angles of each location.
   - Kitchen
   - Living room
   - Courtyard with lemon tree
   - Hallway
   - Noor's bedroom
   - Teta's bedroom
   - Roof terrace
   - Front door
4. Save everything in `/assets/characters` and `/assets/locations` with fixed file names. These are your "reference IDs".
5. Lock voices: Noor (a child voice, playful), Teta (a raspy, warm, theatrical elderly voice), Mama (a firm voice). Store the voice IDs in your TTS tool. **Use only synthetic voices, never clone a real person.**

#### D.2 Per-episode pipeline
**Idea → script (JSON) → shot list → keyframes → I2V clips → audio → edit → QC → publish**

**Prompt blocks to reuse:**

`[STYLE]`:
```
stylized 3D animated feature-film look, soft global illumination, warm late-afternoon light, subsurface skin, clean appealing shapes, rich textures, shallow depth of field, vertical 9:16 composition, no text, no watermark, no logos
```
`[NOOR]` and `[TETA]` are the descriptions from the character prompts in §6.B, used word for word.

`[KITCHEN]`:
```
small cozy Levantine kitchen, patterned blue-and-terracotta cement floor tiles, cream stone walls, arched window with a lemon tree outside, open wooden shelves with copper pots and glass jars, mint-green retro fridge with magnets
```
`[LIVING]`:
```
cozy Levantine living room, patterned cement tiles, low cream sofa with embroidered cushions, brass coffee tray, arched window with lemon tree, framed old family photos
```
`[HALL]`:
```
narrow stone hallway with patterned cement tiles, arched doorways, warm wall sconces
```
`[TETABED]`:
```
Teta's bedroom, carved wooden bed with a crocheted blanket, vintage vanity with perfume bottles, family photos
```
`[NOORBED]`:
```
Noor's bedroom, small bed with yellow duvet, star stickers on the wall, toy shelf, arched window
```

**1. Character reference sheet:** use the prompts in §6.B.

**2. Location plate:**
```
[LOCATION], empty, no people, [camera angle: e.g. eye-level wide from the doorway], [STYLE]. Same architecture and props as the reference image.
```

**3. Scene keyframe** (in an edit-capable image model, with the character sheet(s) and the location plate attached as references):
```
Using the attached references, keep the characters' faces, hair, outfits and proportions EXACTLY as in their reference sheets, and keep the room identical to the location reference. Shot: [shot size + angle]. [CHARACTER] is [precise pose/action at the START of the shot], [expression]. [Other character position]. [Lighting note]. [STYLE].
```

**4. Image-to-video:**
```
Animate the provided image. Action (one beat only): [what moves, start → end]. Camera: [move]. Pacing: [snappy / slow]. Keep every character's face, outfit, hair and body proportions identical to the image throughout; no new characters appear; no morphing; no text. [STYLE].
Audio: [exact SFX] | [Dialogue: CHARACTER says "line" in a [voice description] voice] | [no dialogue].
Duration: 5 s.
```
Rules:
- One action per clip.
- Describe where things start and end.
- Never ask for two characters to swap places.
- Ask for the line in the prompt only if the model has native audio; otherwise put "no dialogue" and add TTS later.

**5. Camera vocabulary** (use exactly one per shot):
- `static locked-off`
- `slow push-in`
- `fast push-in (comedic zoom)`
- `tracking backward in front of subject`
- `low angle tilt up`
- `whip pan to the right`
- `top-down insert`
- `handheld slight shake`
- `dolly left past foreground object`

**6. Dialogue and SFX:**
- With TTS, generate each line separately: `[character voice ID] + line + emotion tag (whisper / excited / stern)`.
- Lines that land on close-ups go through a lip-sync pass (built into the video model, or a lip-sync tool). All other lines play over wide, back-turned or off-screen shots.
- **The SFX kit to build once:**
  - Slipper "shf… shf…"
  - Handbag clasp click
  - Bangles jingle
  - Glasses "ting"
  - Comic stomach growl
  - Record scratch
  - Heavenly "aaah" sting
  - Whoosh
  - Flour poof
  - Thunder

**7. Continuity check (before the edit):**
- [ ] Noor: two puffs, yellow ribbons, gap teeth, yellow pinafore, red sneakers
- [ ] Teta: glasses, silver bouffant, emerald cardigan, plum bag, bangles
- [ ] Mama's face is never shown
- [ ] Heights are right (Noor reaches Teta's shoulder)
- [ ] Props stay in the same place across cuts (jar, bag, cups)
- [ ] Light direction is the same across shots in the same scene
- [ ] Hands: 5 fingers, no merged hands, no extra limbs
- [ ] No text the AI invented (add all text in the edit)
- [ ] The story reads with the sound muted
- [ ] The last frame matches the first frame (loop)

#### D.3 Edit and export settings
- Timeline 1080×1920, 24 fps.
- Cut on action, hold the payoff shot 2–3 s.
- Music −20 to −18 LUFS under dialogue, ducked by 6 dB under lines. Target **−14 LUFS** overall.
- Captions for every line in the middle-lower third (about 60% of people watch muted).
- Title text in the first 1.5 s, top third.
- Export H.264, 1080×1920, 24 fps, ~12–16 Mbps, AAC 320 kbps.

Example ffmpeg assembly, automated from a shot list:
```
ffmpeg -f concat -safe 0 -i shots.txt -i music.mp3 -i dialogue_mix.wav \
  -filter_complex "[1:a]volume=0.35[m];[m][2:a]amix=inputs=2:duration=first,loudnorm=I=-14[a]" \
  -map 0:v -map "[a]" -c:v libx264 -crf 18 -r 24 -s 1080x1920 -c:a aac -b:a 320k episode.mp4
```
(`shots.txt` lists trimmed clips with `file`/`inpoint`/`outpoint`.)

#### D.4 Automation (n8n)

```
[Google Sheet: Episode DB] --new row "approved idea"--> [n8n]
  1. LLM node (e.g. Claude API): idea + series bible -> Episode JSON (schema below)
  2. Loop over shots:
       a. Image API (fal / Replicate / local ComfyUI API): keyframe from refs + prompt  (x3 variants)
  3. HUMAN GATE: Telegram/Slack message with thumbnails -> you pick 1 per shot (or "reroll")
  4. Loop: I2V API call per chosen keyframe (route: action->Kling/Wan, close-up dialogue->Seedance/Veo)
       -> poll queue -> download to /episodes/<id>/clips
  5. TTS API per dialogue line -> /audio ; SFX picked from local library by tag
  6. Local "Execute Command": ffmpeg assembly script -> draft.mp4 (+ .srt captions)
  7. HUMAN GATE: approve the draft / send notes
  8. Publish: Instagram Graph API (Reels) + Facebook Page Reels + YouTube Data API (Shorts), scheduled
  9. Write back URLs + 24h/7d metrics to the Sheet (Insights APIs)
```

- **Keep both human gates.** Choosing takes and approving the final cut is where the quality comes from, and unattended uploads of mass-produced AI video are exactly what platforms demonetize.
- **API keys belong in n8n credentials or environment variables, never inside the workflow JSON or the sheet.**
- Local option: n8n plus ComfyUI on your 3090 Ti (ComfyUI exposes an HTTP API). Route bulk shots there and only paid hero shots to cloud APIs.
- Check whether the AI-content label can be set through each platform's API. If not, set it by hand in the app when publishing.

**Episode JSON schema (what the LLM must output):**
```json
{
  "episode": 1, "title": "The Cookie Jar Heist", "duration_s": 20, "ending_type": "C",
  "shots": [
    {"id": 1, "start": 0.0, "dur": 1.8, "location": "KITCHEN", "characters": ["NOOR","TETA"],
     "shot": "ECU two-shot, eye level", "keyframe_prompt": "...", "i2v_prompt": "...",
     "camera": "slow push-in", "dialogue": [{"who":"NOOR+TETA","line":"Shhh.","emotion":"whisper"}],
     "sfx": ["shhh"], "router": "cheap|hero"}
  ],
  "music": "playful pizzicato heist, 100 bpm, stops at 10.0s", "caption": "...", "hashtags": ["..."]
}
```

---

## 7. Three production-ready episodes

For every shot, put `[STYLE]`, `[NOOR]`, `[TETA]` and the location block from §6.D into the keyframe prompt, and attach the character sheets and location plate as references. Generate each clip at 5 s and trim to the duration given.

### Episode 1: "The Cookie Jar Heist" (20.0 s)

**Story:**
- Mama has left a note: no sweets before dinner. Noor and Teta team up to reach the cookie jar on the top shelf, with Noor on Teta's wobbling shoulders.
- The slippers approach. In an impossible half-second they reset to innocence: Teta sipping tea, Noor angelic but covered in crumbs.
- Mama's hand points at the real culprit, Mishmish the cat. Teta winks; Noor's wink fails.

| # | Time | Dur | Shot / camera | Keyframe prompt | I2V prompt | Refs | Audio |
|---|---|---|---|---|---|---|---|
| 1 | 0.0–1.8 | 1.8 | ECU two-shot, eye level, slow push-in | Noor and Teta peeking over the edge of a kitchen counter, only their eyes and noses visible, both pressing a finger to their lips, mischievous eyes looking into the lens, [KITCHEN] blurred behind | Both slowly raise a finger to their lips and narrow their eyes conspiratorially; slow push-in | Noor, Teta, kitchen | Both whisper **"Shhh."** |
| 2 | 1.8–3.6 | 1.8 | Insert, slow push-in | Close-up of a mint-green fridge door with a lemon magnet holding a blank handwritten paper note, warm light | Slow push-in toward the note, the note flutters slightly | kitchen | Low comedic "dun-dun" hit. **Add the text "NO SWEETS BEFORE DINNER ♥ MAMA" in the edit.** |
| 3 | 3.6–5.6 | 2.0 | Low angle tilt up | A large glass cookie jar full of golden ma'amoul cookies on the highest wooden shelf, glowing in a sunbeam, dust motes | Camera tilts up to the jar; sparkles drift in the sunbeam | kitchen | Heavenly choir "aaah" |
| 4 | 5.6–8.0 | 2.4 | Medium wide, static | Teta squatting like a weightlifter, very serious face, Noor climbing onto her shoulders, handbag on the floor beside them | Teta rises slowly and shakily with Noor on her shoulders, knees trembling, glasses sliding down her nose | Noor, Teta, kitchen | Bangles jingle, effort grunt (Teta) |
| 5 | 8.0–10.0 | 2.0 | Close-up from below, slight handheld | Noor stretching up, fingertips on the jar's lid; below, Teta's straining face, cheeks puffed | Noor lifts the lid and grabs a cookie; Teta's arms tremble | Noor, Teta | Lid "clink", Noor's triumphant gasp |
| 6 | 10.0–11.6 | 1.6 | Floor-level insert, static | Fuzzy pink slippers and light-blue jeans stepping onto patterned tiles in a hallway doorway, Mama's face never shown | The slippers take two slow steps forward | hall | **Music cuts out.** "shf… shf…" |
| 7 | 11.6–13.2 | 1.6 | ECU two-shot, fast push-in | Noor (cookie in her mouth) on Teta's shoulders, both heads snapped toward the camera, eyes huge, frozen | Both freeze, eyes widening; one crumb falls | Noor, Teta | Mama (off-screen): **"Teta? Noor?"** |
| 8 | 13.2–15.6 | 2.4 | Wide, static | At a small kitchen table: Teta sipping tea with her pinky up, eyes closed serenely; Noor sitting perfectly, hands folded, but with crumbs all over her face; on the counter Mishmish the cat sits next to the open cookie jar | Teta sips slowly, Noor blinks innocently, the cat looks at the jar | Noor, Teta, Mishmish | Soft tea sip; innocent music sting |
| 9 | 15.6–17.6 | 2.0 | Medium on the cat, static | Mishmish on the counter with a cookie in his mouth, a woman's hand with a gold ring and pink sleeve entering frame, pointing at him | The hand points; the cat's ears flatten, slow unimpressed blink | Mishmish | Cat's disgruntled "mrrp" |
| 10 | 17.6–20.0 | 2.4 | Close two-shot, slow push-in | Teta and Noor at the table side by side, Teta turning to Noor | Teta gives a perfect wink and secretly slides a cookie from her sleeve to Noor; Noor tries to wink back but blinks both eyes; both raise a finger to their lips | Noor, Teta | Teta whispers: **"Mama doesn't need to know."** + "Shhh" (loops to shot 1) |

- **Music:** playful heist pizzicato (strings plus light darbuka), about 100 bpm, from 0 to 10.0 s. Hard stop at the slippers. A soft innocent celesta for shots 8–10.
- **Editing:**
  - Cut shot 7 to shot 8 on a single frame of white flash (the "impossible reset").
  - Burn in captions.
  - Title in the first 1.5 s: **"Mama said NO sweets 🍪"**.
  - End on the "Shhh" so it loops back to shot 1.
- **Caption:** `EP 01 · Mama said no sweets before dinner. Teta said "what Mama?" 🤫🍪 Who's the real thief? 👇 #NoorAndTeta`
- **Hashtags:** `#NoorAndTeta #Teta #Grandma #GrandmaAndMe #AIanimation #animatedshorts #cookiethief #funnyfamily #partnersincrime #mamadoesntneedtoknow`

### Episode 2: "Teta's Bottomless Handbag" (18.0 s)

**Story:**
- Noor is starving and dinner is an hour away. Teta opens her handbag and pulls out a banana, then a steaming flatbread, then an entire pot of rice.
- Finally Mishmish pops out with a cookie in his mouth. The slippers arrive and all three freeze with full mouths. Teta: "…Snacks for the cat."

| # | Time | Dur | Shot / camera | Keyframe prompt | I2V prompt | Refs | Audio |
|---|---|---|---|---|---|---|---|
| 1 | 0.0–1.6 | 1.6 | Close-up, static | Noor on a sofa clutching her tummy, enormous sad puppy eyes looking up into the lens, [LIVING] | Noor's lip trembles, she clutches her tummy tighter | Noor, living | Comically loud stomach growl |
| 2 | 1.6–3.2 | 1.6 | Medium, static | Noor standing beside the sofa, arms limp, dramatically starving | Noor flops face-first into a sofa cushion | Noor, living | Mama (off-screen): **"Dinner in one hour!"** · cushion "flump" |
| 3 | 3.2–5.0 | 1.8 | Medium, slow push-in | Teta sitting on the sofa next to the flopped Noor, turning toward the lens with her handbag on her lap | Teta slowly lowers her glasses and pats the handbag twice | Teta, Noor, living | Glasses "ting", bangles |
| 4 | 5.0–7.0 | 2.0 | Insert, top-down | Teta's hands on the gold clasp of the plum leather handbag | The clasp clicks open; warm golden light glows from inside like a treasure chest | Teta (hands/bag) | Clasp click + treasure "aaah" |
| 5 | 7.0–9.0 | 2.0 | Two-shot, static | Teta holding up a single banana proudly, Noor (sitting up) looking unimpressed | Noor tilts her head, a flat "meh" face; Teta shrugs and drops the banana back in | Noor, Teta | Noor: **"Meh."** |
| 6 | 9.0–11.2 | 2.2 | Two-shot, fast push-in | Teta pulling a large steaming round flatbread with za'atar out of the handbag | Steam rises; Noor's eyes go wide and sparkly | Noor, Teta | Sizzle, Noor gasps |
| 7 | 11.2–13.6 | 2.4 | Medium wide, static | Teta lifting a huge steaming cooking pot of rice out of the small handbag with both hands, physically impossible | Teta sets the giant pot on the coffee table, steam billows; Noor's jaw drops | Noor, Teta, living | Heavy "clunk", steam hiss |
| 8 | 13.6–15.8 | 2.2 | Close-up on the bag, static | The open plum handbag on Teta's lap | The bag wiggles; Mishmish the cat pushes his head out with a cookie in his mouth, deeply unimpressed | Mishmish, Teta | Rustle, cat "mrrp" |
| 9 | 15.8–18.0 | 2.2 | Wide, static | Teta, Noor and Mishmish on the sofa, mouths full, food everywhere; at frame edge fuzzy pink slippers and jeans in the doorway | All three freeze mid-chew and slowly turn their eyes to the slippers | All, living | "shf… shf…" · Teta (mouth full, innocent): **"…Snacks for the cat."** |

- **Music:** a "magic trick" xylophone build that rises with each item (banana, then bread, then pot), with a cymbal swell on the pot. Hard stop on the slippers.
- **Editing:**
  - Each item reveal gets a quick 6-frame zoom punch-in.
  - Title: **"Dinner in 1 hour?? Teta has a plan 👜"**.
  - Freeze-frame the last 0.3 s.
- **Caption:** `EP 02 · Every Teta's handbag has a whole kitchen inside 👜😂 What's in YOUR Teta's bag? #NoorAndTeta`
- **Hashtags:** `#NoorAndTeta #grandmasbag #Teta #AIanimation #animatedshorts #funnygrandma #snacktime #arabfamily #grandmaandme #familycomedy`

### Episode 3: "Thunder" (22.0 s; the heart episode)

**Story:**
- A thunderstorm wakes Noor. She tiptoes to Teta's room for safety and finds Teta hiding under the blanket, just as scared.
- They make a blanket fort. Teta makes shadow puppets and they laugh through the next thunderclap.
- Morning: Mama finds them asleep, with Mishmish on Teta's head, and gently tucks the blanket over them.

| # | Time | Dur | Shot / camera | Keyframe prompt | I2V prompt | Refs | Audio |
|---|---|---|---|---|---|---|---|
| 1 | 0.0–2.0 | 2.0 | Medium, static | Night, [NOORBED], cool blue moonlight; Noor sitting bolt upright in bed clutching a plush camel, the window behind her | A lightning flash fills the room with white light; Noor's eyes go wide, she hugs the plush tighter | Noor, Noor's bedroom (night) | Thunder crack |
| 2 | 2.0–4.2 | 2.2 | Low, tracking behind | Night, [HALL] in blue moonlight; Noor in yellow pajamas (same hair puffs and ribbons) tiptoeing away from camera, dragging the plush camel | Noor takes tiny careful steps down the hallway; distant lightning flickers | Noor, hall (night) | Rumbling thunder, tiny footsteps |
| 3 | 4.2–6.0 | 1.8 | POV through doorway, slow push-in | Night, [TETABED]; a lump under a crocheted blanket on the bed, trembling | Door creaks open, the blanket lump trembles | Teta's bedroom (night) | Door creak |
| 4 | 6.0–8.0 | 2.0 | Close-up, static | The edge of the blanket lifted slightly, Teta's glasses and frightened eyes peeking out, a small flashlight lighting her face from below | Teta's eyes dart to Noor; she blinks, embarrassed | Teta | Teta (whisper): **"You too?"** · Noor nods |
| 5 | 8.0–10.0 | 2.0 | Medium, static | Teta lying in bed holding up the blanket like a tent opening, Noor at the bedside | Teta flaps the blanket open; Noor dives inside | Noor, Teta | Teta: **"Inside. Quick."** · rustle |
| 6 | 10.0–12.6 | 2.6 | Inside the fort, wide | Under the blanket, a warm orange flashlight glow, Teta and Noor lying side by side; Teta's hands make a camel-shaped shadow on the blanket wall | The camel shadow walks along the blanket; Noor smiles | Noor, Teta | Soft oud lullaby begins |
| 7 | 12.6–14.6 | 2.0 | Close two-shot | Noor making a wobbly bunny shadow with her small hands next to Teta's camel | The bunny "hops" onto the camel's back; both giggle | Noor, Teta | Giggles |
| 8 | 14.6–16.4 | 1.8 | Close two-shot, handheld shake | Same fort, sudden bright white flash | Both jump and hug each other tight, then burst out laughing | Noor, Teta | Big thunder → laughter |
| 9 | 16.4–19.4 | 3.0 | Wide, very slow push-in | Morning sun, [TETABED]; the collapsed blanket fort; Teta and Noor asleep cuddled together, plush camel, Mishmish asleep on top of Teta's bouffant; in the doorway, fuzzy pink slippers and jeans | Gentle breathing, curtain moving in the breeze, the cat's tail flicks | All | Birdsong, lullaby continues |
| 10 | 19.4–22.0 | 2.6 | Close-up, static | A woman's hand with a gold ring (face never shown) pulling the crocheted blanket up over the sleeping pair | The hand tucks the blanket; Teta, eyes closed, smiles | Teta, Noor | Teta (sleepy whisper): **"Mama doesn't need to know."** |

- **Music:** a soft solo oud or music-box lullaby starting at shot 6. Sound design only before that (thunder and rain). Rain continues low through the night shots.
- **Editing:**
  - A cooler colour grade for the night shots, then a warm grade for the morning, so the change in feeling shows in the colour.
  - Title: **"When it thunders, go to Teta ⛈️"**.
  - Avoid fast punch-ins in this episode; let it breathe.
- **Caption:** `EP 03 · When the thunder comes, you go to Teta. Even when Teta is scared too 🥹⛈️ Send this to your Teta ❤️ #NoorAndTeta`
- **Hashtags:** `#NoorAndTeta #Teta #grandmalove #grandmaandme #AIanimation #animatedshorts #wholesome #thunderstorm #blanketfort #familylove`

**Character references needed for all three episodes:** Noor sheet (day clothes, plus one pyjama variant for Ep 3 with the same hair and ribbons), Teta sheet, Mishmish sheet, Mama's slippers and hand, and the kitchen, living room, hall (day and night), Teta's bedroom (night and morning) and Noor's bedroom (night).

---

## 8. 90-day launch plan

**Days −14 to 0 (pre-production):**
- Build the characters, locations, voice IDs and SFX kit.
- Produce **10 finished episodes** before posting anything (a buffer means you won't miss days).
- Set the account up as a creator or business account so Insights and API publishing work.

**Days 1–30 (test):**
- Post **1 episode a day** on Instagram Reels, the same file on **Facebook Reels** and **YouTube Shorts** (with a vertical title card).
- Test one variable a week:
  - Week 1: dialogue against no dialogue.
  - Week 2: 15 s against 22 s.
  - Week 3: ending types A, C and E.
  - Week 4: hook styles.
- **What to track** (Insights, 48 h after posting):
  - 3-second hold or skip rate
  - Average % watched (above 100% means rewatches)
  - Shares/sends per 1,000 reach
  - Saves
  - Follows per 1,000 reach
- My rules of thumb for decisions (targets, not promises):
  - Hold under ~60%: fix the hook.
  - Average watched under ~70%: cut the middle.
  - Shares under ~1% of reach: the payoff isn't strong enough.

**Days 31–60 (focus):**
- Keep the 2 best-performing ending types and hook styles; cut the others.
- Add **1 two-part cliffhanger a week**.
- Start a weekly "Ask Teta" episode built from comments. Comment-driven episodes build community.
- Post a YouTube **long-form compilation** every 2 weeks (10–15 episodes, about 4–5 min), since long-form earns more per view.
- Set up a WhatsApp/Telegram sticker pack of the signature expressions (free reach).

**Days 61–90 (monetize):**
- Make a **one-page media kit**: characters, audience, average views, share rate, 3 sample brand-integration ideas.
- Pitch brands that fit naturally:
  - Baking and food brands (Teta's recipes)
  - Tea and coffee (the alibi sip)
  - Family and holiday campaigns (Ramadan, Eid, Christmas, Mother's Day)
  - Kids' clothing and toys
  - Handbags (the bottomless bag)
- **Your own products** (you already use Gumroad):
  - A "Noor & Teta" illustrated storybook ebook
  - A printable colouring pack
  - Later: "Mama doesn't need to know" merch and a Mishmish plush via print-on-demand
- **Platform payouts:**
  - Facebook content monetization (invite-based in many regions)
  - The YouTube Partner Program once you qualify (check the current Shorts thresholds in YouTube Help)
  - Instagram bonuses where offered
  - Treat all of these as unreliable. AI accounts have been demonetized as "unoriginal" before.

**Platform rules that affect this channel:**
- **Disclose AI.** Use Meta's "AI info" / AI label and add "AI-animated series" to the bio. YouTube's synthetic-content disclosure is aimed at realistic content, and clearly animated content has been exempt, but disclosing anyway costs nothing and builds trust.
- **YouTube "made for kids":**
  - Noor & Teta is a cartoon starring a child, but the humour (Mama's rules, grandparent love) is aimed at **adults and families**. Keep it that way: avoid nursery music, toys-as-content and educational kid formats.
  - Answer the "made for kids" question honestly. If you mark it as made for kids, comments and personalised ads are turned off, which hurts growth and income.
  - YouTube has removed AI kids' channels from monetization after scrutiny.
- **Originality:** YouTube's inauthentic/mass-produced content policy and TikTok's "unoriginal" flagging punish near-identical uploads. Every episode needs a genuinely new story; the human gates in the automation are essential.
- **Tool licences:** generate only on plans that grant commercial rights. Never use a real person's likeness or voice clone. Don't name copyrighted studios or characters in prompts.

**Risks and bottlenecks:**

| Risk | What to do about it |
|---|---|
| Character drift (faces, outfits) | Character LoRA on your 3090 Ti, the continuity checklist, 3 keyframe variants per shot |
| Reroll costs spiral | Hybrid routing (cheap model for action shots), max 3 rerolls then rewrite the shot |
| Hands and props glitch | Frame hands out of shot or use inserts; keep props simple |
| Text garbled in AI images | Add every on-screen text in the edit, never in the generation |
| Burnout from daily posting | 10-episode buffer; batch production 2 days a week |
| Copycats | Post fast and build the brand (stickers, book, merch); own the "Mama doesn't need to know" phrase |
| Demonetization of AI content | Diversify: brands plus your own products plus 3 platforms |
| Cultural clichés | Keep it warm and specific (real dishes, real habits); have someone from the culture review scripts |

**Note:** none of this guarantees growth like Max And Minni World's. Its ~103K followers from 30 posts is unusual, and your results will depend mostly on how strong each episode's payoff is, which the 30-day tests are there to measure.

---

## Sources
- fal Seedance 2.0: https://fal.ai/seedance-2.0 · https://fal.ai/models/bytedance/seedance-2.0/image-to-video · https://fal.ai/models/bytedance/seedance-2.0/fast/image-to-video
- Seedance pricing comparison: https://apimodels.app/access/seedance-api-pricing · https://apiframe.ai/models/seedance-2.0/pricing
- Kling pricing: https://costgoat.com/pricing/kling · https://costbench.com/software/ai-media-apis/kling-api/ · https://renderful.ai/blog/kling-api-pricing
- Veo / general video API pricing: https://modelslab.com/blog/api/veo-3-1-vs-kling-3-sora-2-ai-video-api-cost-2026 · https://devtk.ai/en/blog/ai-video-generation-pricing-2026/ · https://www.buildmvpfast.com/api-costs/ai-video
- AI kids' content on YouTube: https://wtsp.com/article/news/ai-animation-being-used-to-target-kids-on-youtube-nobodys-tracking-it/89-55b955d1-eea9-4290-a872-addd73ec270d · https://tech.slashdot.org/story/24/03/19/2117213 · https://channellife.news/story/youtube-sets-2026-agenda-on-creators-kids-ai-tools
- Granny Spills (grandma trend): https://time.com/7329699/ai-influencers-tiktok-granny-spills/

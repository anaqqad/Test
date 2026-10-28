---
name: wojak-lives-video-method
description: Wojak Lives Video Method. Make "Life as… / Life with…" Wojak meme videos end to end (idea, 18-point script, characters, backgrounds, render to MP4, cover, upload metadata) with the pipeline in wojak-lives/render/. Use when asked to create a new video, episode, cover or metadata for Wojak Lives or for another channel or niche in the same style.
---

# Wojak Lives Video Method

Pipeline: `wojak-lives/render/` (code), `wojak-lives/brand/` (rig, fonts), `.claude/skills/wojak-lives-video-method/` (this file).

## 1. Pick the idea
A topic must have all four:
1. **Recognisable at a glance**: an identity or relationship with an iconic look (niqab, apron + chancla, glasses + report card).
2. **A huge community that feels seen**: viewers think "that's me" and send it to a sibling.
3. **Built-in comment debate**: "NOT ALL ___ (most)" versus "so true".
4. **A list of short, true, painful moments**: no plot needed.

- Title formula: `Life as a ___` / `Life with ___` + one emoji. The identity comes first.
- Don't repeat an identity that's already done; pick a *different* community.
- **US audience:** American topics, `$`, °F, miles, US spelling (mom, neighbor, pajamas), and US places (Walmart, Costco, DMV, high school, porch, suburban kitchen).
- **Done:** Muslim girl, Mexican mom, Asian parents.
- **Ideas still open:** Arab son, hijabi in America/Europe, eldest daughter, desi girl, Arab mom, Florida man, kid of immigrant parents.

## 2. Write the script (main format: 16:9, text only, ~75–80 s)
- **Structure:**
  - Title card (4.6 s): big title, a small subtitle, and a yellow stamp "NOT ALL ___ (most)".
  - **18 points**, about 3.5–5 s each. Duration is automatic: `max(3.2, 1.0 + 0.25 × words)`.
  - One warm last point, e.g. "But nobody makes ___ like Mom", with hearts.
  - End card "PART 2?" (2.6 s).
- **One point** = one sentence, top-left, ≤ 18 words, plus one visual gag.
- **Specific nouns and numbers are funny:** "98%", "4 seconds", "GOODBYE 1/47", "leftovers from 2019", "AGE: 9".
- **Rule of three, break the third:** "Cold. Headache. Broken arm. Broken heart."
- **Joke shape:** setup in the caption, then a quote in a speech bubble, then the payoff as a sticker label or a face change at 50–65 % of the scene.
- **Tone:** joke about the *situation* (aunties, group chat, slipper, rice cooker), never the religion, race or people.
  - No accent jokes and no tragedy.
  - Punch up or inward.
  - End warm.
- **Never call the first video "part 2"**: the reference video belongs to another creator. Don't copy its title word for word.

## 3. Characters (Wojak faces only)
- **Same Wojak face for everyone.** Only skin tone, hair, clothes and props change. **No ethnic caricature** (no slanted eyes, no exaggerated features).
- **Veiled characters:** `python3 wojak-lives/render/draw_niqabi.py` → `assets/chars/{girl,mom,aunty_red,aunty_green}_{tired,wide,angry,side,sad,cry,happy,roll,dead}.png`, plus `girl_{tired,side,wide,happy}_phone`.
- **Family characters (shared rig in `brand/draw_cast.py`):** `python3 wojak-lives/render/draw_family.py` → `<who>_<expr>.png`.
  - **who:** mxmom, mxmom_chancla, mxmom_spoon, mxdad, mxkid, tia, asmom, asmom_spoon, asdad, asdad_report, askid, askid_report.
  - **expr:** feels, bloomer, crying, rage (red face), soy (shocked), smug, side-eye, doomer.
  - To add a new family, add a `CAST` entry (skin, shirt, hair, props) and, if needed, a hair style in `hair_front` and a prop in `PROPS`.
- **Men / extras:** the Nobo cut-outs (`brand/nobo/face_*`), recoloured to black and grey automatically. Use `tint="npc"` for grey extras.
- **Avoid on kids:** `doomer` (it adds stubble).
- **Layout:**
  - "You" (the kid) on the left facing right: `pos=(0.33, 1.16), size=0.95`.
  - The parent on the right: `flip=True, pos=(0.74, 1.16), size=1.05, enter=0.4`.
  - Single character: default centre.
  - Title card: `pos=(0.5, 1.42)` so the title clears the head.
- **Better art (optional):** ChatGPT image generation with `wojak-lives/chatgpt_prompts.md`.
  - Ask for the *simple MS-Paint Wojak meme template, flat colours, no realism, no cross-hatching*.
  - Attach a Wojak meme as a style-only reference.
  - Upload the master sheet with every request.
  - Cut out with a transparent background.

## 4. Backgrounds
- Real photos, no text in frame, never a mosque interior.
- Source: **Pexels** (free licence, no attribution). Find IDs with a web search (`pexels photo <scene>`), then download:
  `curl -A "Mozilla/5.0" -o assets/bg169/<name>.jpg "https://images.pexels.com/photos/<ID>/pexels-photo-<ID>.jpeg?auto=compress&cs=tinysrgb&w=1920"`
- Check a contact sheet before use. Wikimedia Commons (`fetch_bg.py`) works but rate-limits and needs CC BY-SA credits.
- **Existing 16:9 backgrounds (`assets/bg169/`):** us_kitchen, us_kitchen2, us_living, us_living_tv, us_backyard_party, us_classroom, us_porch, us_desk, alley, alley_people, street, small_store, beach, wedding_hall, moroccan_room, mall2, university, market_night, shops_night.
- **Vertical ones** are in `assets/bg/`.
- **Treatment (automatic):** saturation −25 %, slight blur; `tint="night"|"warm"`; `blur=` per scene.

## 5. Episode file → MP4
Create `wojak-lives/render/episodes/ep_<slug>.py` with:
```python
B = "bg169/"
EPISODE = {"title": "LIFE WITH ___", "size": (1920, 1080), "no_title": True, "music": "sad", "scenes": [
  dict(bg=B+"us_kitchen2.jpg", dur=4.6, char="<who>_smug", pos=(0.5, 1.42),
       lines=[dict(t=0, text="Life with ___", size=140, y=0.13), dict(t=1.3, text="(subtitle)", size=62, y=0.27)],
       labels=[dict(t=2.6, text="NOT ALL ___ (most)", x=0.5, y=0.38, size=66, rot=-6)],
       sfx=[dict(t=0, name="impact", gain=0.8), dict(t=1.3, name="impact", gain=0.6), dict(t=2.6, name="thwack")]),
  dict(bg=B+"us_kitchen.jpg", char="<kid>_feels", pos=(0.33, 1.16), size=0.95,
       text="Caption sentence.", keywords=["WORD."],
       extras=[dict(t=0, img="<parent>_smug", pos=(0.74, 1.16), size=1.05, flip=True, enter=0.4)],
       bubbles=[dict(t=0.3, text="Quote.", x=0.72, y=0.34, tail="down", talk=True, talk_dur=0.9)],
       labels=[dict(t="60%", text="PAYOFF", x=0.33, y=0.36, size=60)],
       beats=[dict(t="60%", char="<kid>_crying", punch=1.12, shake=0.3)],
       fx=[dict(t="55%", kind="flames", x=0.5, y=0.16)], sfx=[dict(t="60%", name="scratch")]),
  # … 18 points, warm ending with fx hearts, then:
  dict(bg=B+"us_kitchen2.jpg", blur=12, char="<who>_smug", pos=(0.5, 1.4), dur=2.6,
       labels=[dict(t=0.2, text="PART 2?", x=0.5, y=0.3, size=110)], sfx=[dict(t=0.2, name="thwack")]),
]}
```
- **Times:** seconds, `"N%"` of the scene, or `"vo±X"`.
- **`keywords`** match the caption words *with their punctuation*, in upper case.
- **fx:** flames (anger), sweat, question, exclaim, hearts, steam.
- **sfx:** impact, thwack, scratch (before the main punchline), boing, pop, ding, whoosh, buzz (phone), horn, slide_down, sting, door, tick.
- **Bubbles:** `style="phone"` for texts and group chats.
- **Commands:**
  - Check stills first: `python3 wojak-lives/render/render.py wojak-lives/render/episodes/ep_<slug>.py --still N` (scene N; scene 1 is the title).
  - Full render: `python3 wojak-lives/render/render.py wojak-lives/render/episodes/ep_<slug>.py` → `out/ep_<slug>.mp4`. About 4–5 min, so run it in the background; two renders in parallel are fine.
- **Verify** with a frame contact sheet (`ffmpeg -i X.mp4 -vf "fps=1/3.2,scale=320:-1,tile=6x5" -frames:v 1 sheet.jpg`) and check for overlaps (sticker on eyes, title on head).
- **Copy** to `out/<Video title>.mp4` and send it.
- **Audio:** procedural music and SFX (no copyright claims); loudness is −14 LUFS automatically. Tell the user to listen once (it can't be checked by eye).

**Alternative format (9:16 Shorts with voice):** `episodes/ep001_introvert.py` style.
- Piper TTS narrator (`pip install piper-tts`), auto captions, a yellow "LIFE AS…" tag at 0:00, Nobo faces.
- 60–75 s, about 160–200 words, a loop ending, and a "WHO'S NEXT?" end card.

## 6. Cover (thumbnail)
Copy the reference: **one big calm Wojak face, centred, on the episode's photo, no text, no red face, no props by default.**
```
python3 wojak-lives/render/thumbnail.py <who>_feels bg169/<bg>.jpg "out/<Video title> - cover.png" --y 0.1 --scale 1.3 --dx -0.05
```
- Nudge `--dx` until the head is centred (glasses or props shift the bounding box; e.g. asdad `--dx -0.16`).
- Optional second cover with the iconic prop (e.g. chancla) for A/B testing.

## 7. Upload metadata (save in `render/metadata/<slug>.md`, give it to the user as copy-paste blocks)
- **Title:** `Life with ___ <emoji>`
- **Description:**
  ```
  <one punchline>. <emoji>

  Tag your sibling who ___ 👇

  Not all ___ (most). Satire for entertainment; all characters are fictional.

  #<identity> #<identity2> #<identity3>
  ```
- **Tags:** identity variants, `___ be like`, the community's own words (chancla, first gen, …), wojak, wojak animation, relatable, funny animation.
- **Pinned comment:** a question that invites stories ("What did YOUR mom keep in the ice cream tub? 👇") or the next topic ("Part 2: ___, ___ or ___? 👇").
- **Settings:**
  - Category **Comedy** (set as the upload default)
  - Language English (United States)
  - Made for kids: No
  - Altered or synthetic content: No
- **Schedule:** one video every 2–3 days, 12–3 pm US Eastern, Thursday to Sunday.

## 8. Channel identity (Wojak Lives)
- **Name:** Wojak Lives, `@wojaklives`
- **Bio:** "Every life is a little ridiculous."
- **Profile picture:** one Wojak character, black and grey only, no text.
- **Characters:** a different cast per video; no fixed recurring cast.

## 9. Deliver
- Commit the code, episode file and metadata, then push.
- `out/` is git-ignored: send the MP4 and the cover with SendUserFile.
- Keep replies short, and give metadata as copyable blocks.

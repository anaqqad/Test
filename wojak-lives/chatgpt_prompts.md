# Wojak Lives: ChatGPT image prompt pack (badass Wojak art)

The final character art comes from **ChatGPT image generation**, not the flat SVG rig in `brand/`. The rig
is now only for quick layout tests and animatics. The target look is the "doomer Wojak" meme style: the
simple MS-Paint Wojak face template, thin black lines, flat colours, a few stubble dots, dark eye bags, tough
tired faces, pasted on blurred real photos. It must look like a meme, not a realistic illustration. That's the quality level of **Broke & Famous** (see the README, "Reference channels").

**Don't copy Broke & Famous's character.** Their Wojak wears a black beanie and a black tank top, in black
and white. Ours is **bald with buzz-cut stubble, a scar through the eyebrow, and a coral-orange hoodie**.
The coloured hoodie is our signature: in a feed of black-and-white Wojaks, the coral stands out.

## How to keep the character consistent in ChatGPT
1. Generate the **master sheet** (prompt 1) once. Pick the best result and save it as `nobo_master.png`.
2. For every new image, **start a fresh message, upload `nobo_master.png`**, and begin the prompt with
   *"Use the exact same character as in the attached image: same face, scar, stubble and hoodie."*
3. Ask for a **transparent background** (or plain white) for characters, so you can paste them onto photos
   in CapCut. Generate backgrounds separately (prompt 6).
4. Sizes: characters 1024×1536 (portrait), thumbnails 1536×1024 (landscape).
5. If a result drifts (hair appears, the hoodie changes colour), reply: *"Same image, but fix: [thing]. Keep everything else identical."*

---

## 1. Master character sheet: NOBO (main character)

**v1 came out too realistic** (an illustrated real man instead of a meme). Words like "detailed",
"cross-hatching" and "stipple shading" push ChatGPT towards realism, so v2 asks for the *meme template*
and forbids realism. Best results: **upload a screenshot of a classic doomer Wojak meme** (e.g. a Broke &
Famous thumbnail) together with the prompt, and say it's for the *drawing style only*.

**If you're still in the same ChatGPT chat as v1, just reply:**
```
Too realistic. Redraw him as an actual Wojak meme: the classic simple MS Paint Wojak face template
(bald egg-shaped head, flat white skin, thin wobbly black lines, simple almond eyes with heavy lids and
grey eye bags, the hooked one-line Wojak nose, tiny ear), not a realistic man. Remove all realistic
anatomy, neck tendons, skin texture and cross-hatching. Stubble = a few scattered black dots only.
Hoodie = flat coral-orange fill with a few simple black lines. Keep the scar, the layout and the expressions.
```

**Fresh prompt (v2):**
```
[Attach a classic doomer Wojak meme image] Use the attached image for DRAWING STYLE ONLY, not the character.

Draw an original character named Nobo as a real Wojak meme: the classic 2010s "Feels Guy" / Doomer Wojak
face template, drawn like the meme in MS Paint. Simple and flat: thin slightly wobbly black outlines,
flat white skin, almost no shading (only soft grey eye bags and a little grey on the back of the head),
NO realistic anatomy, NO skin texture, NO cross-hatching, NO realistic neck or muscles.

Nobo: bald egg-shaped Wojak head in three-quarter view facing right with a faint grey buzz-cut tone on
the scalp, simple almond eyes with heavy droopy lids and dark grey eye bags, tired stare, the classic
hooked one-line Wojak nose, small simple ear, short sad mouth line, a few scattered black stubble dots on
the jaw, a small red scar line through his left eyebrow. Done-with-life but tough.

Clothes: coral-orange hoodie (#FF6B4A) as a flat fill with simple black outlines, hood down, two
drawstrings, grey t-shirt collar. Cropped at the chest like a meme bust.

Layout on plain white: top row = three busts (3/4 front, side, back). Bottom row = six head close-ups:
thousand-yard stare, gritted-teeth rage (red face), shocked tiny pupils, smug smirk, single tear, forced
smile with sweat drop. Every face must look like a Wojak meme, not a person. No text.
```

### ✅ Approved master (v2)
The v2 prompt worked. The approved sheet is saved as `brand/nobo/nobo_master.webp`, with transparent
PNG cut-outs ready for CapCut: `bust_front`, `bust_side`, `bust_back`, and `face_stare`, `face_rage`,
`face_shocked`, `face_smug`, `face_tear`, `face_forced_smile` (all `.png` in `brand/nobo/`).
**Upload `nobo_master.webp` with every future prompt.**

Two faces need a redo because **smug** and **forced smile** look almost the same. Regenerate them with:
- `Use the exact same character as in the attached image. Head close-up, SMUG: one eyebrow raised high, eyes half-closed looking sideways at the viewer, a one-sided smirk pulled up on the right, chin slightly raised. Same simple Wojak meme style, transparent background.`
- `Use the exact same character as in the attached image. Head close-up, FORCED SMILE: huge wide grin showing a full row of teeth, eyes completely dead and staring, big sweat drop, one eye twitching. Same simple Wojak meme style, transparent background.`

## 2. Single expressions (upload `nobo_master.png` first)
Start each with: *"Use the exact same character as in the attached image: same face, scar, stubble and hoodie."* Then add:

| Use | Add this |
|---|---|
| Default narration | `Half-body, three-quarter view facing right, thousand-yard stare, slight frown. Transparent background.` |
| Rage | `Half-body, gritted teeth, veins on temple, eyes bulging, face slightly red, fists clenched. Transparent background.` |
| Shock | `Half-body, eyes wide with tiny pupils, mouth hanging open, sweat drops flying. Transparent background.` |
| Smug | `Half-body, smug half-lidded smirk, one eyebrow raised, arms crossed. Transparent background.` |
| Crying (tough) | `Half-body, single tear rolling down, jaw clenched, looking slightly down. Transparent background.` |
| Dead inside | `Half-body, completely empty eyes with no pupils, grey skin tone, mouth a flat line. Transparent background.` |
| Forced smile | `Half-body, huge fake smile showing teeth, eyes dead, sweat drop on temple. Transparent background.` |
| Phone | `Half-body, holding a smartphone close to his face with one hand, screen light on his face, tired stare. Transparent background.` |
| Lying in bed | `Lying in bed under a grey blanket, only head and shoulders visible, staring at the ceiling, side view. Transparent background.` |
| Walking | `Full body walking to the right, hands in hoodie pocket, dark jeans, worn sneakers, head down. Transparent background.` |
| At a desk | `Sitting at an office desk in three-quarter view, hands on keyboard, slumped, monitor glow on his face. Transparent background.` |

## 3. Secondary cast (same art style; one master per character)
Begin each with: *"Same simple Wojak-meme drawing style as the attached image (thin MS-Paint lines, flat colours, white skin, no realism), but a NEW character:"*

- **Mama:** `a Wojak-style mother in her 50s wearing a deep purple hijab framing her face, sharp knowing eyes with eye bags, smug confident smirk, small laugh lines, green cardigan. Half-body, three-quarter view facing right, transparent background.`
- **Lulu (female lead):** `a Wojak-style young woman (the "Wojak girl" meme style) with long straight black hair and a side fringe, tired eyes with lashes and subtle bags, unimpressed expression, teal sweater. Half-body, transparent background.`
- **Dad (boomer):** `a "Boomer" Wojak dad with black sunglasses, grey mustache, balding with grey sides, white polo shirt, holding a coffee mug, unimpressed. Half-body, transparent background.`
- **Boss:** `a smug corporate Wojak boss with a greasy comb-over, grey suit, red tie, fake smile, pointing at the viewer. Half-body, transparent background.`
- **Bro:** `a "Chad"-style Wojak friend with blond swept hair, square jaw, huge enthusiastic grin, yellow t-shirt, arms open wide. Half-body, transparent background.`
- **NPC crowd:** `three grey "NPC Wojak" characters side by side: flat grey skin, dot eyes, triangle nose, straight line mouth, plain grey clothes, identical blank expressions. Transparent background.`

## 4. Profile picture
```
Square 1:1 YouTube profile picture. Use the exact same character as in the attached image (Nobo).
Head-and-shoulders, centred, filling most of the frame, three-quarter view, thousand-yard stare,
simple MS-Paint doomer-Wojak meme style with a few stubble dots and dark eye bags, coral-orange hoodie (#FF6B4A)
with hood down. Background: flat solid royal blue (#3D7BFF) circle. No text. Must read clearly at tiny sizes.
```

## 5. Thumbnail (16:9, landscape)
```
YouTube thumbnail, 16:9, 1536x1024. Use the exact same character as in the attached image (Nobo).
Nobo very large on the left half, half-body, [EXPRESSION, e.g. gritted-teeth rage], simple meme doomer-Wojak
ink style, coral-orange hoodie. Background: a real photo of [PLACE, e.g. a supermarket aisle] with strong
motion/zoom blur so the character pops, slight dark vignette. On the right, one bold prop: [PROP, e.g. a
giant price sign reading "$2500"]. High contrast, no other text.
```
Then add the yellow "LIFE AS…" tag in CapCut or Canva yourself, since image models misspell text.

## 6. Backgrounds (real-photo look, no people)
```
Vertical 9:16 smartphone photo, [SCENE], eye-level, natural light, realistic and unremarkable,
no people, no text, no logos, empty space in the lower half for a character, slight depth of field.
```
The `[SCENE]` lines for each episode are in `episodes/0X-*.md` under "Image-generation prompts".

## 7. Props / stickers (in-video gags)
```
[PROP], drawn in the same simple Wojak-meme style (thin black outlines, flat fills,
mostly black-white-grey with one flat accent colour), isolated on a transparent background.
```
Examples: a pizza with sad Wojak eyes, a cash-machine receipt, a smug sun with sunglasses, a box of dates, a beige desk phone.

---

**Cost note:** these prompts are written for the ChatGPT app (included in your ChatGPT plan). Generating
them through the OpenAI API instead costs money per image and needs an API key; only set that up once
you've decided you want it.

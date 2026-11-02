# ChatGPT prompts: Most Notorious Gangs Wojaks (5 images → 19 characters)

Goal: the crude MS-Paint meme Wojaks of the reference list channels, not our clean vector rig.

**How to use**
1. Open a new ChatGPT chat. Attach `ref_wojaks.png` (the style sheet I sent you, cropped from the reference
   video) to **every** prompt. It's there for the drawing style only.
2. Paste prompt 1, then 2… Each image = 4 characters in a 2×2 grid (prompt 5 = 3). Square 1024×1024.
3. If a result looks too clean or realistic, reply with the **Fix** line at the bottom.
4. Upload the 5 images here (any order, just tell me the sheet number). I run
   `python3 render/import_gpt.py sheet1.png g_yakuza g_camorra g_triad g_sicily` (etc.), which cuts them out
   and re-renders the video.

The rule for every sheet: lots of white space between the characters, so the cut-out can split them.

---

## Shared style (already inside each prompt)
```
Use the attached image for DRAWING STYLE ONLY. Draw original characters as classic crude MS Paint Wojak
memes: thin, slightly wobbly black lines, flat colours, flat pale Wojak skin, almond eyes with heavy lids and
grey eye bags, the hooked one-line Wojak nose, a small simple ear, a few scattered black stubble dots. Ugly,
amateur, meme-like. NOT realistic: no shading except grey eye bags, no skin texture, no cross-hatching, no
realistic anatomy. Each character is a head-and-shoulders bust cropped flat at the chest, three-quarter view
facing right, with a closed black outline along the bottom edge. Plain pure white background, characters
far apart and not touching, 2x2 grid. No text, no logos, no weapons.
```

## Sheet 1 → `g_yakuza g_camorra g_triad g_sicily`
```
[shared style above]
Top-left: Japanese man, slicked-back black hair, black sunglasses, black suit, white shirt open at the
collar with a bit of a colourful tattoo showing, calm smug face.
Top-right: Italian man from Naples, grey buzz cut, dark sunglasses, white tracksuit jacket, thin gold chain,
side-eye.
Bottom-left: 1980s Hong Kong man, neat side-parted black hair, white shirt, black blazer, cold stare.
Bottom-right: old Sicilian man, flat grey coppola cap, thick grey moustache, dark waistcoat over a white
shirt, tired smirk.
```

## Sheet 2 → `g_ndrangheta g_peaky g_usmafia g_hells`
```
[shared style above]
Top-left: old Calabrian farmer, short grey hair, thick black moustache, plain dark jacket, suspicious squint.
Top-right: 1920s Birmingham man, grey flat newsboy cap, short undercut, three-piece tweed suit with a white
collar, cold stare.
Bottom-left: 1930s New York man, grey fedora, pinstripe suit, wide tie, smug grin.
Bottom-right: biker, black bandana on the head, black sunglasses, goatee, plain black leather vest over a
grey T-shirt (no patches, no logos), angry red face.
```

## Sheet 3 → `g_krays g_latinkings g_eme g_westies`
```
[shared style above]
Top-left: 1960s London man, short slicked dark hair, thick black-rimmed glasses, dark suit, thin tie,
blank stare.
Top-right: 1990s Chicago guy, gold baseball cap, black hoodie, smug face.
Bottom-left: California man, shaved head, thin black moustache, light-blue button-up work shirt, tired stare.
Bottom-right: 1970s New York Irish-American man, messy red hair with sideburns, brown leather jacket, side-eye.
```

## Sheet 4 → `g_crips g_bloods g_medellin g_cali`
```
[shared style above]
Top-left: 1980s Los Angeles guy, blue bandana tied on the head, blue flannel shirt, side-eye to the right.
Top-right: 1980s Los Angeles guy, red bandana tied on the head, red flannel shirt, side-eye to the left.
Bottom-left: 1980s Colombian man, curly black hair, thick black moustache, short-sleeve polo shirt,
smug face.
Bottom-right: 1990s Colombian businessman, slick black hair, small glasses, grey suit and tie, polite smile.
```

## Sheet 5 → `g_ms13 g_sinaloa g_pcc`
```
[shared style above, but "3 characters in a row" instead of "2x2 grid"]
Left: shaved head, black sunglasses, plain white T-shirt, a few small blue tattoo dots on the face,
blank stare.
Middle: Mexican man, white cowboy hat, thick black moustache, plaid western shirt, smug face.
Right: Brazilian man from São Paulo, shaved head, thin chain, plain grey tank top, tired stare.
```

---

**Fix (too clean or realistic):**
`Uglier and cruder. Real MS Paint Wojak meme: wobbly lines, flat fills, egg-shaped head, no shading. Same layout and characters.`

**Fix (characters touching):** `Same image, but put much more white space between the characters.`

ChatGPT may refuse anything that says "gang". These prompts only describe clothes and eras, so keep it that way.

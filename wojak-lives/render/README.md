# Wojak Lives: video renderer

Turns an episode file into a finished vertical video (1080×1920, 30 fps, MP4, loudness −14 LUFS for YouTube),
with no editing app needed.

```
pip install piper-tts                     # free offline voice (downloads ~60 MB voice model once)
python3 wojak-lives/render/render.py wojak-lives/render/episodes/ep001_introvert.py
python3 wojak-lives/render/render.py wojak-lives/render/episodes/ep001_introvert.py --still 6   # check one scene
```
Output: `wojak-lives/render/out/<episode>.mp4`

What it does automatically:
- **Voice:** Piper TTS (`en_US-ryan-medium`), deadpan narrator, free and offline. Replace it with your own
  recorded voice later for better quality.
- **Captions:** word-chunk captions synced to the voice, with keywords in yellow.
- **Title tag:** a yellow "LIFE AS…" tag slapped on at 0:00 that stays on screen.
- **Characters:** the Wojak cut-outs in `brand/nobo/`, recoloured to black and grey. Other people are greyed
  copies for now; swap in each video's own ChatGPT characters as PNGs in `brand/`.
- **Speech bubbles and phone messages** with gibberish "blip" voices, plus yellow label stickers.
- **Camera:** slow push, punch-ins, shake, character slide-outs.
- **Sound:** synthesised SFX (boing, record scratch, whoosh, phone buzz, pop, tick…) and a quiet lo-fi loop,
  all generated in code, so there are no copyright claims.

Backgrounds: `assets/bg/` (Pexels photos, free licence; sources in `assets/bg/credits.json`).
`fetch_bg.py` can pull CC-licensed photos from Wikimedia Commons (it rate-limits; credit CC BY-SA authors).

Episode files: `episodes/ep001_introvert.py` documents every scene key (backgrounds, voice line, faces,
beats, bubbles, labels, extra characters, sound effects, timing).

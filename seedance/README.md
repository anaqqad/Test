# Seedance 2.5 prompts (saved from a chat session)

Context: an uploaded 30 s vertical video (720x1280, 24 fps, lip-synced dialogue, ~16 cuts) was analyzed and the
prompt was rebuilt in the structure the Seedance 2.5 guides recommend. The original prompt was never found online
(the file had no generation metadata), so everything here is a reconstruction or a new variant.

## Prompt structure that works
1. Global style line: format (`Vertical 9:16, 30s`), look, light, lens, "exactly N characters, identical faces and wardrobe".
2. Characters: one line each, name in CAPS, age, ethnicity, hair, wardrobe, one prop.
3. Location + blocking: who stands where; "screen direction never flips".
4. Shot list with second timestamps (`0s-2s:`), shot size, action, `NAME (cue): "line"`. Keep lines ~8 words.
5. Camera + audio + negatives ("no subtitles, no text overlays, no watermark").
6. Optional: reference photos tagged `@Image1 = NAME` for stable faces.

Sources: Higgsfield, suno.bi, Picsart, Runway, OpenArt, Seedance.tv, Atlabs, Ambience AI, MindStudio, mkanime,
Seeddance lip-sync guides (links in `prompts.md`).

## Files
- `prompts.md`: the three full prompts plus extra story ideas.

## Lessons
- The first rebuild copied the original cast and dialogue word for word; the owner wanted a *fresh* version.
  When remaking a viral format, keep the story beats and change cast, setting, wardrobe, props and every line.

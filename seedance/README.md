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
- Hook rule (owner's data): the first 4 seconds decide the video. Best openers are a girl crying in extreme
  close-up from frame 1, or a strong man with a little girl running to him. Start mid-moment, dialogue at 0.0s,
  a loud sound cue (door slam) around 2s, and the payoff visual by 4s.

## Stories already made (don't repeat)
- Mother owns the house (deed reveal, evicts son and wife)
- Cheap car key opens a Mercedes
- Biker at a father-daughter dance ("Never Dance Alone")
- Always (firefighter saves his own daughter from a fire)
- The Ice (rescue: sanitation worker saves boy from frozen pond)
- The Stowaway (pirate captain, compass)
- Not Breathing (teen saves grandpa in a supermarket)
- The Car (teacher finds student living in a car)
- The Paper Piano (mocked girl plays)
- The Little Boat (dinghy -> yacht)
- The Little House (gift reveal), The Payroll (guard underpaid), The Owner (steakhouse)
- Add the rest of the owner's past videos here.
- Review of the first render of "The Owner" (480x854): the story beats all landed, but the output was only 480p,
  the big man's 3s "rise" showed just his legs (no hero shot), the girl walked instead of ran, and 8s-12s was
  four seconds of the same crying close-up. Fixes: render at 720p/1080p, describe the hero shot as
  "full body, head to boots, standing", write "sprints" plus "slow motion", and keep every shot under 2.5s in the first 15s.
- Hood-reveal shot in the same render: the framed photo behind him faded in during the shot (a morph, not a cut),
  and the photo showed him in the same hoodie and chain. Fix: put the frame on the wall in an earlier wide shot
  ("already hanging, sharp, unchanged"), keep the hood shot one continuous take with a static background, and dress
  him differently in the photo. Also make every big guy look clearly fictional (distinct hair, glasses, tattoos)
  so he isn't mistaken for a celebrity.
- Face fix for "The Owner" (2026-10-06): FaceFusion 3.9.1 on the RTX 3090 Ti (CUDA), `seedance/fix_the_owner/run_facefusion.bat`.
  The full 30.08 s / 721-frame video took about 2 min 20 s end to end (two passes of ~55-60 s each, about 14-16 frames/s,
  plus the final encode; the first run also downloads ~1 GB of models). Pass 1 swaps the man (reference face at frame 540),
  pass 2 swaps the framed photo behind him (2nd-largest face at frame 540). Girl and manager unchanged, audio bit-identical.
  Distance 0.3, not 0.5: in 3.9.1 the scale changed and at 0.5 the manager got swapped too.

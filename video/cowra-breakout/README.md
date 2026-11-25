# Japanese POWs at Cowra (WWII Frontlines, working title)

The Cowra breakout, 5 August 1944: at about 2 a.m. a bugle sounded in B compound of No. 12 POW Compound, Cowra, New South
Wales, and about 1,100 Japanese prisoners charged the wire with baseball bats, knives and blankets. Told through the man
said to have blown the bugle, Hajime Toyoshima, the Zero pilot shot down over Darwin who was the first Japanese prisoner
taken on Australian soil and who lived under a false name, and through the guards of the 22nd Garrison Battalion.

## Improvements over missouri-surrender (from LESSONS.md and the scoreboard, 24 Nov 2026)
1. **Back to the title shape that works for us.** Our hits start with "Japanese POWs…" / "German POWs…" (baseball 63K,
   no fence 14K, trains 2.2K, nurses 2.2K, sukiyaki 1.5K); the MacArthur / Pacific raid run got 12–50 views each
   (Missouri 12 in 15 h). WWII Box's all-time top three are also "German POWs…" titles (624K, 273K, 108K). Title starts
   with "Japanese POWs", and the baseball bats link to our biggest hit.
2. **No repeated 3D seconds** (owner, 24 Nov 2026: "you repeat too much the plane scene"). Every reconstruction is
   rendered long enough or from new angles for every beat it covers; no clip's seconds used more than twice; risk and
   reuse checks live in `tools/`, not `build/` (build/ is regenerable and was deleted with the last episode's scripts).
3. **Documents on their own** (owner, 24 Nov 2026: "never show them over the document template, show them
   separately"): scans full frame by themselves with the highlight on the page, no card template around them.

Research: `research/facts_raw.md`, `research/media_candidates.md`, `research/sources.md`.

## Build (24 Nov 2026)
- Narration: Kokoro `bm_george` 1.2, 123 paragraphs, 30:53; no archive voices (the AWM oral histories are copyright,
  so survivors' and guards' words are read and shown on quote cards, attributed to the transcript page).
- Plan: `tools/plan.py` (engine) exec()s `tools/plan_cards.py` (films, tags, maps, quote cards, numbers, documents)
  and `tools/plan_body.py` (shots per paragraph, prints). Episode data lives in tools/, never in build/.
- Checks before rendering: `python tools/check_anchors.py` (every anchor/synced phrase is spoken; lists all at once),
  `python tools/reuse_check.py` (no 3D second on screen more than twice, no cut past a clip's end; counts only what
  is visible), `python tools/risk.py` (slates, titles, surgery, blown-out stretches). All print `bad 0`.
- 3D: 14 shots in `tools/blender/cowra_shots.py` (exec'd by scene.py): zero, camp_day, camp_night, bugle, charge,
  vickers, broadway, dawn, farm + second angles night_tower, broadway_day, charge_side, ash_walk, farm_verandah.
  `bash tools/render3d.sh "<shots>"` renders (frames land in build/r3d/<s>/<s>/), `bash tools/encode3d.sh <shots>` encodes.
  Night scenes need exposure ~1.1 and moon 0.25 (0.4 was black, 1.6 looked like day).
- Documents: shown plain, full frame (owner: "never over the document template"): `LedgerDocument` with `plain: true`.
- Photos: the AWM offers 640 px downloads; its deep-zoom viewer has full scans but blocks scripts (not worked around).
- Stand-in film: only the U.S. Navy Noumea POW films (NPC-740, -738) and two captured 1942 Japanese newsreels were
  usable; NPC-744 is blown out, the Saipan reel is a civilian camp, the airman reel has burned-in timecode.

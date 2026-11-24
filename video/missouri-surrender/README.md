# Japan Expected MacArthur to Humiliate Them on the Missouri (WWII Frontlines, working title)

The Japanese surrender, 15 Aug - 2 Sep 1945, told from both sides: the Atsugi landing, the first prisoners freed in
Tokyo Bay, Wainwright and Percival brought out of Manchuria, and the 23 minutes on USS Missouri, seen through the report
the diplomat Toshikazu Kase wrote for the Emperor. Title format: WWII Box's MacArthur series, used literally
(owner, 23 Nov 2026: "let's make another MacArthur or something that can go viral").

## Improvements over bush-chichijima (from LESSONS.md and the scoreboard, 23 Nov 2026)
1. **Ride a topic that is trending right now.** Missouri-surrender videos are pulling 165K (6 days), 237K (3 weeks) and
   420K; WWII Box's MacArthur series 61K-189K. Our two MacArthur-format videos (Wainwright 89, Homma 44) took the format
   but not a trending moment; this one takes both, with searchable names in title and chapters (MacArthur, USS Missouri,
   Atsugi, Wainwright, Percival, Shigemitsu, Tokyo Bay).
2. **Thumbnail copied exactly from the reference** (owner: their success is "mainly their 3D animations and
   thumbnails"): photo left, black panel right, two-word question in white, yellow place-and-date line, one straight
   thick red arrow to the face. No curved grease-pencil arrow this time.
3. **Moving reconstruction scenes where no camera was** (owner, 23 Nov 2026, after Immersive Past's 1.4M video, about half
   of which is simple 3D animation): at least 4 animated scenes (Atsugi approach, the road to Yokohama, the Missouri deck
   plan with who stood where, the 23-minute ceremony clock), in our own colours, no realistic people.

Research: `research/sources.md`, `research/facts_raw.md` (23 sources), `research/story_outline.md`, `research/media_candidates.md`.

## Build (23 Nov 2026)
- Narration: Kokoro `bm_george` 1.2, 99 paragraphs, 34:34, four `[CLIP]` lines of MacArthur's own voice on the Missouri
  (U.S. Navy Combat Bulletin No. 7, NARA 80-MN-9034G; United News 208-UN-171B). The "malice or hatred" and "freedom,
  tolerance and justice" lines are on no government reel: narrated and shown on quote cards.
- 3D: `tools/blender/scene.py` (Blender 4.2 EEVEE, kit copied from kaktus-engine): battleship, destroyer, C-54/C-46, B-29,
  carrier planes, sedan, LCVP, barracks, faceless clay figures. Eight shots (s_arrive, s_deck_plan, s_deck_sign, s_flyover,
  s_road, s_atsugi, s_drop, s_omori), 10-12 s each, `bash build/render3d.sh "<shots>"` -> `assets/footage/r3d_<shot>.mp4`.
  Motion blur off (10 s/frame -> ~2 s/frame), JPEG frames (disk), encode only when Blender exits cleanly.
- Plan: `tools/plan.py` = cat of `build/plan_head/helpers/cards/body/tail.py`; 479 shots, 191 overlays; `build/risk.py`
  prints `bad 0` (slates, United News eagle cards, white flashes, the atomic-bomb segment of Screen Magazine 68).
- Highlights: staff-history pages 24, 31, 100 (archive.org BookReader scans); word boxes from archive.org's own
  `fulltext/inside.php` (RapidOCR misreads the italic quote columns).
- Cards: rendered in three parallel `node render.mjs <ids>` processes (one was ~1.7 min/card).
- Thumbnail: `python tools/thumbs_episode.py` (reference layout, straight red arrow).

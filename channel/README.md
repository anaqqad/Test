# Borderclock: data-driven map-timelapse videos (Remotion)

One JSON file in `data/videos/` describes one video: map framing, sides, territory keyframes, pace, camera,
events and captions, counters, leaders, audio and thumbnail. The engine renders the video, the thumbnail, and a
YouTube description with chapters. Strategy, format analysis and the first four videos: `../docs/channel-plan.md`.

## Run
    npm i
    npm run studio                                   # preview and scrub in the browser
    node scripts/render.mjs korean-war          # out/<id>/<id>.mp4, thumbnail.jpg, description.txt
    node scripts/render.mjs korean-war --qc     # one still per event, to check fronts against sources
    node scripts/render.mjs korean-war --keyframes   # one still per territory keyframe
    node scripts/render.mjs korean-war --range=0-299 --scale=0.5   # quick partial preview
    npm run typecheck

Without internet access to download Remotion's Chrome, point it at an installed one:
`REMOTION_BROWSER=/path/to/chrome node scripts/render.mjs ...` (also read by `npx remotion` via `remotion.config.ts`).

## Videos
- `korean-war` - built by `python3 tools/build_korean_war.py` from front lines researched in the US Army CMH
  official histories (Appleman; Mossman) and the Natural Earth line of control.
- `mongol-empire` - built by `python3 tools/build_mongol_empire.py` from `tools/mongol/extents.geojson`
  (regions drawn from Wikipedia campaign articles, cross-checked against Taagepera's areas; `build_extents.py`
  regenerates it with shapely). Labels and leaders: `tools/mongol/static.json`.
Edit the builder, rerun it, then check with `--keyframes` before rendering.

Music: Scott Buckley (CC BY 4.0). His Content ID system claims any video whose description lacks the credit, so
the credit line is part of each video's `youtube.credits` and goes into the generated description. Upload with
that description from the start.

## New video
1. Copy `data/videos/korean-war.json`, change `id`, keep `"draft": true`.
2. Register it in `src/videos.ts`.
3. Set `map.bounds` (west/south, east/north) and `map.theatre` (Natural Earth country names, e.g. "South Korea";
   unknown names raise an error listing them).
4. Territory keyframes: each date lists layers painted in order; a later layer takes pixels from earlier ones.
   - `{ "faction": "a", "everywhere": true }` - all theatre land
   - `{ "faction": "a", "countries": ["Finland"] }`
   - `{ "faction": "b", "beyond": { "side": "north", "line": [[lon, lat], ...] } }` - everything north of a front
     line (line runs west to east; for east/west sides it runs south to north)
   - `{ "faction": "b", "geometry": { GeoJSON Polygon/MultiPolygon } }` - pockets, enclaves (draw at geojson.io)
   Shapes may spill over sea and neighbours; they are clipped to theatre land. Borders morph smoothly between
   keyframes, so add a keyframe wherever the real movement was not a straight slide. A faction that is absent in one
   keyframe and present in the next only appears near the end of that interval: give it a tiny seed shape earlier.
5. Events: `holdSeconds` freezes the clock, `chapter: true` puts it in the description's chapters, `source` is for
   fact-checking (not rendered).
6. Check with `--qc`, fix, then set `"draft": false`; draft renders carry a red banner on every frame.

## Notes
- Projection `conicEqualArea` (default) makes the "territory held" km² exact; the demo measures 220,760 km² for the
  two Koreas (real: ~220,750).
- Measured on a 4-core cloud VM without GPU: ~0.9 s per 1080p frame (a 3-minute video is ~80 min). Rendering is
  CPU canvas work, so more cores help more than the GPU.
- The demo's front lines are rough approximations from general knowledge, for testing the engine only.
- Data: Natural Earth via world-atlas (public domain / ISC). Fonts: Cinzel, Barlow Condensed (SIL OFL).

# 3D Mediterranean Table

**Origin:** Built for Malta v4 (`table` shots in `lingo/longform4.mjs`), extending the 3D desk idea from WWII Frontlines' `DocDesk3D` to a sea chart: a paper Mercator chart on a wooden table in CSS 3D, objects dropped onto it.

**When to use:** Map-heavy stretches where two or more places are compared over time. The physical table gives every map beat a new camera angle and lets evidence (coins, prints, reports) sit next to the place it is about.

**How to build (`lingo/longform4.mjs`):**
- `EP.table = { tex, w, box: [[lon0, lat0], [lon1, lat1]], regions, labels: [[text, place, size, dx, dy]], objects: { id: { kind: "coin"|"print"|"card", src, at, dx, dy, w, rot } }, arrows: [{ from, to, color, dash, label, at }], title }`.
- Shots: `{ table: { from: { at, zoom, tilt, rz }, to: {...}, focus }, place: [objectIds], fill: {...}, fillAt }`.
- Overhead (tilt ≈ 5) to locate; low angle (tilt 55–65) when an object is placed; close (zoom 5–10) to cut into the artifact; back overhead only when there is something new to compare.
- North up, one scale bar, labels printed on the chart: they never change between angles. Island colours share the map's fill timeline, so map shots and table shots agree.
- Objects drop with a shadow and Foley (coin on wood, paper).

**Pitfalls:** Labels are in the chart, so very low angles foreshorten them: keep tilt ≤ 65. The title can be printed onto the chart between the places it names.

**Used in Malta v4:** 0:11 (h5), 0:23 (h7), 0:28 (h8), 0:45 (g2), 1:04 (t2), 2:02 (t7), 2:09 (t8), 2:18 (t9), 2:37 (t11), 3:12 (p4) in `out/malta4_v4.mp4`

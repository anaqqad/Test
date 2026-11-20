# Read the Ink

**Origin:** Adapted from WWII Frontlines' LedgerDocument (a highlighter runs along real scan lines in step with narration). New: the camera path and the final pull-back to the attribution.

**When to use:** Any primary document the story depends on (a manuscript, a register, a title page). The viewer investigates it instead of looking at it.

**How to build (`lingo/longform3.mjs`):**
`photo` with `path: [[q, fx, fy, scale], ...]` (q = 0–1 through the overlay), `sweep: { box, q0, q1 }` (an underline that travels along the line), `mark: [x0, y0, x1, y1]` + `markAt` (a box on the key word), `attrib` + `attribAt` (who wrote it, who copied it, when found), `capAt`.
Order: tight on line 1 → track across the ink as it is read → hold on the key word → pull back to the whole page → attribution.

**Pitfalls:** Coordinates are fractions of the image. Leave a music gap (`musicGap`) on the line that is read out.

**Used in Malta v3:** 3:43 (m1), 3:54 (m3), 7:58 (r3) in `out/malta3_v3.mp4`

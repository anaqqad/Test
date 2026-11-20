# Document Pullback

**Origin:** Port of WWII Frontlines' DocDesk3D (Hoog-style 3D desk) to LingoDude: `desk` shots in `lingo/longform4.mjs`, with highlighter sweep, word circle and a line box.

**When to use:** Any primary document whose wording matters: read the line, make it readable, then show where it sits on the real page.

**How to build (`lingo/longform4.mjs`):**
- `EP.docs = { key: photoKey }`; shots `{ desk: { doc, from: { tilt, rz, zoom, fx, fy }, to, focus: { y, band, blur }, sweep: { box, q0, q1 | full }, mark: { box, at }, line: box } }`.
- Order: macro glide along the line (narrow focus band) → readable typed transcription on a plate → pull back to the whole page with the line boxed → low angle on the key word, circled.
- Keep the translation as a line-level overlay (`show` with `until`) so it stays in place across the cut from transcription to page.
- Show surrounding text only when it changes the meaning (here: the poem sits among legal papers).

**Pitfalls:** Fewer than ~1000 px of scan width blurs at zoom > 3; use the macro on high-resolution scans only.

**Used in Malta v4:** 3:40 (p7), 3:47 (m1), 3:52 (m2), 3:58 (m3), 4:01 (m4), 4:05 (m5), 8:00 (r3), 8:09 (r4) in `out/malta4_v4.mp4`

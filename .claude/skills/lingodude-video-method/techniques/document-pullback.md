# Document Pullback

**Origin:** Port of WWII Frontlines' DocDesk3D (Hoog-style 3D desk) to LingoDude: `desk` shots in `lingo/longform4.mjs`, with highlighter sweep, word circle and a line box.

**When to use:** Any primary document whose wording matters: read the line, make it readable, then show where it sits on the real page.

**How to build (`lingo/longform4.mjs`):**
- `EP.docs = { key: photoKey }`; shots `{ desk: { doc, from: { tilt, rz, zoom, fx, fy }, to, focus: { y, band, blur }, sweep: { box, q0, q1 | full }, mark: { box, at }, line: box } }`.
- Order: macro glide along the line (narrow focus band) → readable typed transcription on a plate → pull back to the whole page with the line boxed → low angle on the key word, circled.
- Keep the translation as a line-level overlay (`show` with `until`) so it stays in place across the cut from transcription to page.
- Show surrounding text only when it changes the meaning (here: the poem sits among legal papers).

**Pitfalls:** Fewer than ~1000 px of scan width blurs at zoom > 3; use the macro on high-resolution scans only.

**Used in Malta v4:** {{TS4:p7,m1,m2,m3,m4,m5,r3,r4}}

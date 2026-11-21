# Investigation Board

**Origin:** Concept from the owner's other conversations (no implementation existed on any branch); built for Malta v4 in `lingo/longform4.mjs` (`board` shots). Felt board, paper cards and red pins in the channel palette.

**When to use:** A why-question film where evidence arrives over several minutes. The board keeps the case in one place: the viewer sees each new piece land and what it supports.

**How to build (`lingo/longform4.mjs`):**
- `EP.board = { w, h, cards: { id: { kind: "q"|"claim"|"photo"|"word"|"conclusion", x, y (top centre), w, rot, text, tag, src (photo key), cite } } }`.
- Shots: `{ board: { view: "full" | cardId, push, k, tilt }, add: [ids], link: [[evidence, conclusion]], rewrite: { card, text, tag, tagColor, at } }`.
- Cards are pinned when the narration meets the evidence (tack Foley); strings draw only from evidence to the conclusion it supports.
- Cut pattern: full board (where it fits) → card detail (what it says) → conclusion card (what it proves). Never hold the full board more than ~3 s: the text is too small on a phone.
- The Claim Rewrites Itself runs on board cards: strike-through, typed revision, new certainty tag.

**Pitfalls:** Keep card text under ~10 words. A string must be defensible from the source; list them in the episode's sources file.

**Used in Malta v4:** 0:35 (b0), 1:14 (t3b), 1:25 (t3c), 2:18 (t9), 2:51 (p1), 3:05 (p3), 4:12 (m6), 5:57 (w10), 7:53 (r2) in `out/malta4_v4.mp4`

## v5: a board the viewer can follow (owner brief, 2026-11-21)
**Layout:** shared clue on top (the language clue and the link being investigated, plus any competing claim about the
link with the test beside it), then the question, then two columns (Malta left, Sicily right) in date order with the
oldest at the top, each row = evidence card (left) → finding card (right), and a PROVISIONAL ANSWER band at the bottom.
`kind: "head"` cards are fixed headings; `lines: [[x1, y1, x2, y2, dashed]]` draws the dividers.

**Strings say something:** `links: { id: [evidence, finding, label, style?, { route: "below", bx, at, sag }] }` and shots
reveal them by id (`link: ["L1241"]`). Labels: records / shows (solid red), suggests (dashed red, an inference),
challenges / supports (blue, a test), not shown (grey dashed, a step left open). Strings run under the cards; labels sit
on top (`at` = position along the curve, `bx` spreads joins that end on the same card).
**The rule:** if you can't finish "this source supports this claim because…", there is no string (list each string in
the episode's sources file). A step the sources don't prove gets an OPEN card and a "not shown" string.

**One step at a time:** close on the active card (`hl: [id]` sweeps a highlighter over its `[[marked]]` phrase), then cut
wide (`cut: true`) as the labelled string draws. `lit: [ids]` keeps those cards bright and dims the rest (blends over
0.6 s between consecutive board shots). `cap: [kicker, text]` is a caption strip; the same `cap` on consecutive shots
stays put, giving extra reading time across the cut. Consecutive board shots glide from the previous framing (eased,
with a small zoom-out arc) unless `cut: true`; `view` can be a card, a list of cards (fitted) or `{ x, y, k }`.

**Competing claims:** put the claim beside the card that tests it, draw a CHALLENGES string, then rewrite the claim on
screen. A picture that is not evidence (a coin) is pinned with a VISUAL ANCHOR tag and no string.

**Ending:** full board, then trace each column with `lit` (glide down it), then the joins into the answer band, then
the open question, then the full board again.

**Used in Malta v5** (`out/malta4_v5.mp4`): see `longform/malta4/CHANGES_v5.md` for timestamps.

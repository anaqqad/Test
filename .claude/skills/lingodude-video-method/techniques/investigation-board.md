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

**Used in Malta v4:** {{TS4:b0,t3b,t3c,t9,p1,p3,m6,w10,r2}}

# The Word Arrives Before the Place

**Origin:** Invented for Malta v3 (no reference channel opens on a sound alone; closest is WWII Frontlines' document-first opens, which start on paper, not on a voice).

**When to use:** The opening of any language film whose hook is a word. The viewer hears a real native speaker before seeing a map, a title or a narrator, so the first question is 'what was that?'.

**How to build (`lingo/longform3.mjs`):**
1. First line: no `say`, `hear: ["<word>"]`, `hearFirst: true`, `quietHear: true` (no LISTEN badge), `lead` 0.4–0.6 s, `dur` ~2.5 s.
2. Show a tight physical object that carries the word (a dictionary page, a sign) with `photo` + `enter: "cut"` + a slow `path` push-out (scale 3.3 → 2.75).
3. Put the page-turn Foley 0.3 s *before* the line (`sfx: [{ s: "page", at: -0.3 }]`) so the sound lands before the picture settles.
4. No score until the reveal: the first `score` cue sits on the first narrated line.
5. A one-line `tagline` names the object (date · source) for muted viewers.

**Pitfalls:** Keep the word under 1 s and loud (words are pre-levelled to −17 LUFS). Never put narration over it.

**Used in Malta v3:** 0:00 (oA1) in `out/malta3_v3.mp4`

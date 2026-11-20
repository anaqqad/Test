# The Consonants Lock In

**Origin:** Invented for Malta v3. Adapted from LingoDude's own word-pair cards; the motion idea (letters sliding into shared columns) has no reference-channel source.

**When to use:** Any comparison where two related words share a skeleton (Semitic roots, sound laws, cognates). It shows the relationship instead of saying it.

**How to build (`lingo/longform3.mjs`):**
`{ type: "lock", dark: true, rows: [{ lang, hear, gloss, script, parts: [[text, isConsonant, column]] }] }`.
- Each row appears exactly when its recording plays (the renderer reads the clip times).
- After the last word, consonants slide into red columns (K · T · B), vowels shrink and drop: the half-beat to connect.
- Use `hearFirst`, `hearGap` 0.7–0.8 and `quietHear`; the score is silenced automatically for every word clip.

**Pitfalls:** Vowels must be marked `0` or they also lock. Arabic script row needs the `script` field (Noto Naskh).

**Used in Malta v3:** {{TS:oA2,w4,w5}}

# Typography Follows the Voice

**Origin:** Invented for Malta v4 (`words` overlay).

**When to use:** Whenever a native recording is the evidence: the word is written by the voice itself, so the viewer connects sound and spelling.

**How to build (`lingo/longform4.mjs`):**
`{ type: "words", items: [{ hear, text, script, label, labelAt }] }`. The renderer measures each recording's loudness envelope (30 fps); letters appear in proportion to the energy spoken so far and the word swells with the voice. Labels (MALTESE / ARABIC) can be held back and revealed later.

**Pitfalls:** Keep it to 1–2 words per row; long phrases read better as an `aside`.

**Used in Malta v4:** {{TS4:h1,h2,w3a,s5,s5b}}

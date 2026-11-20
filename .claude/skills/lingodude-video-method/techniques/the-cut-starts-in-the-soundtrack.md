# The Cut Starts in the Soundtrack

**Origin:** Missing from the inspected references (WWII Frontlines uses a bed only, no pre-laps). Standard film J-cut, built as a renderer feature.

**When to use:** Every hard cut into a new place: the viewer hears the door, page or harbour 0.3–0.7 s before seeing it, so cuts feel motivated, not abrupt.

**How to build (`lingo/longform3.mjs`):**
- Foley: `sfx: [{ s: "door", at: -0.7, gain: -4 }]` on the line that cuts (negative `at` = before the line starts).
- Location sound: every `video` overlay brings its own audio as the ambience stem, faded in 0.5 s early.
- Score changes texture per sequence (`score` cues) and crossfades over 1.5 s.

**Pitfalls:** Foley is peaked at −12 dBFS in the stem; keep `gain` negative for doors.

**Used in Malta v3:** {{TS:m7,w3,s5}}

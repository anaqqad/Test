# Two Islands, One Clock

**Origin:** Adapted from BorderClock (branch ccr-9383248a-do6ckh: one map, a year counter driving borders) and WWII Frontlines' ledger timelines; the split-screen same-scale comparison is new.

**When to use:** Any 'why here and not there?' story: two places that share a start and diverge. Viewers compare states at a glance instead of holding them in memory.

**How to build (`lingo/longform3.mjs`):**
`{ type: "twin", until: "<last line>", y0, y1, steps: [{ at: "<line id>", year, mark, sic: { c, status, note }, mal: { ... } }] }`.
- Both shapes are drawn at one scale (the bigger place sets the zoom), so size is part of the argument.
- One shared year counter and timeline bar; each step recolours a side, swaps its status pill and note.
- Evidence (photo, frame, dots) pauses the clock: the twin dims to 25 % while it is on screen.
- End the sequence with a music gap on the line where the clocks disagree.

**Pitfalls:** Keep notes under ~45 characters. Re-use the twin at the end to deliver the answer in its final state.

**Used in Malta v3:** {{TS:t1,t8,t12,r1}}

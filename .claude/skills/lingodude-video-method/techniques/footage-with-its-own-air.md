# Footage With Its Own Air

**Origin:** Adapted from TheLanguageMap's live-action cutaways; built for LingoDude because v2 had only stills.

**When to use:** Breaking a long map or document passage: 3–6 s of real location footage resets attention, and its own sound tells the viewer where they are before the caption does.

**How to build (`lingo/longform3.mjs`):**
`{ type: "video", src, from, enter: "cut", s0: 1.0, s1: 1.06, caption, ambGain }`; sources in `EP.videos` with credits. Frames are pre-extracted and colour-graded to the palette; the clip's audio becomes the ambience stem, levelled ~22 dB under the voice and dipped under native words.

**Pitfalls:** Use Commons footage with clear licences; prefer clips with natural sound and no music.

**Used in Malta v3:** {{TS:oA3,p1,w1,s1,r5}}

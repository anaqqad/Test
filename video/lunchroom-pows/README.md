# German POWs Ate at the Tables (WWII Frontlines, 15 min)

Cpl. Rupert Trimmingham's letter to Yank (28 April 1944): nine Black soldiers on their way from Camp Claiborne to Fort
Huachuca could only eat in a station kitchen while about two dozen German POWs were served at the tables. With the
replies in Yank, Lloyd Brown in Salina, Kansas, Lena Horne at Camp Robinson, the Florence nurses and Executive Order 9981.

## Improvements over cowra-breakout (owner and scoreboard, 25 Nov 2026)
1. **15 minutes, not 30** (owner: "let's make 15 min videos now instead"). The 30-min run (Navajo to Cowra) got 20-466
   views; the niche's hits this month (Captive Witness, Captive Reality) are 12-16 min. 2,241 words, 58 paragraphs, 14:30.
2. **Captive Witness's title and thumbnail** (owner: "what works for this channel are the thumbnails"): "German POWs
   <did X>. <Contrast>." and a B&W split with a 2-word yellow question, on real archive images (no AI).
3. **No 3D renders** (owner, 25 Nov 2026), no film/photo second more than twice (`tools/reuse_check.py` covers every
   film), documents full frame on their own (Yank page, Executive Order 9981).

## Build
- Narration: Kokoro `bm_george` 1.2 (runs on the CPU, ~25 min for 14:30; Whisper alignment also CPU).
- Research: `research/sources.md` (22 sources, disagreements: the station is never named; Horne at Camp Robinson, Ark.,
  not Fort Riley; Brown's account is his own NYT op-ed of 1973, not Terkel).
- Plan: `tools/plan.py` + `tools/plan_cards.py` + `tools/plan_body.py`; checks `check_anchors.py`, `reuse_check.py`,
  `risk.py` all `bad 0`. Film Bulletin 164 is badly faded (graded in `assemble.py`, used for ~30 s only).
- Omaha Guide scans not shown (loc.gov bot check; rights page unreachable): its words are on text cards with the source.

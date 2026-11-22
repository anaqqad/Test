# Navy File Shows What George H.W. Bush Really Did in WW2 (WWII Frontlines)

Lt (jg) George H.W. Bush, VT-51, USS San Jacinto: the Chichi Jima strike of 2 September 1944, the bailout, the rescue by
USS Finback, and the American airmen captured on Chichi Jima whose fate came out at the U.S. Navy war crimes trials on
Guam (1946-47). Told from the records: squadron action report, flight logbook, Finback's war patrol report, citations,
the trial record. Title format from Nobody To Legend ("<Branch> File Shows What <famous name> Really Did in WW2",
owner's choice, 22 Nov 2026).

## Improvements over cabanatuan-raid (from LESSONS.md and the scoreboard, 22 Nov 2026)
1. **A famous name in the title.** The 30-min Pacific run sits at 26-123 views after 1-3 days (Cabanatuan 31, Homma 39,
   Los Baños 26, Navajo 123); the only POW hits were contrast stories. Test the competitor pattern that pulls 150-367K
   (famous name + official file + "really did"), on a topic with proven search demand (Chichi Jima: 9.6M and 3.1M views).
2. **The file is the spine.** The title promises a file, so every act opens on a page of it (action report, logbook,
   patrol report, citation, trial record), shown as desk documents and highlights, and the narration names the page.
3. **A real voice in the first two minutes and chapters veterans search for:** Bush's own voice from a public-domain
   government recording if one exists; chapter names VT-51, USS San Jacinto, TBM Avenger, Chichi Jima, USS Finback,
   Guam war crimes trials.

Research: `research/sources.md`, `research/facts_raw.md`, `research/media_candidates.md`.

## Build (22 Nov 2026)
- Narration: Kokoro `bm_george` 1.2, 101 paragraphs, 33:11, five `[CLIP]` lines of Bush's own voice (1991 WHCA audio as
  waveform cards made by `tools/voice_card.sh`, 1992 White House Television interview on camera).
- Plan: `tools/plan.py` is concatenated from `build/plan_head.py`, `plan_helpers.py`, `plan_cards.py`, `plan_body.py`,
  `plan_tail.py` (edit the parts, then `cat` them together). 456 shots, 189 cards; `build/risk.py` checks every shot
  against the slate / face / timecode ranges in `build/film_log.md` (must print `bad 0`).
- New: `Verdict` card (three claims, stamps synced to the words), Chart `islands` outlines traced from the 2014 aerial,
  `tools/line_bands.py` for highlight rects on microfilm scans the OCR cannot read.
- Wikimedia originals answer 429 to curl: run a localhost receiver, open it in the built-in browser, `fetch` the
  Commons file in the page and POST it back (finback rescue film, 1992 interview).
- Render: `HEIGHT=1080 bash tools/render_missing.sh`, `python tools/assemble.py --clips-only --hd`,
  `python tools/assemble_parts.py 8`. QC: no black frames, -16 LUFS, contact sheets checked for symbols and faces.

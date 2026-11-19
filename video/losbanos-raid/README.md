# The raid at Los Baños (WWII Frontlines)

The 11th Airborne Division and Filipino guerrillas free 2,147 starving civilian internees at Los Baños, Luzon, on 23 February
1945, told with what the popular version leaves out: why H-hour was 7:00 (Pete Miles and the guards' calisthenics), the starvation
evidence from the Konishi trial, the killings of Filipino civilians around Los Baños, Konishi's real execution date (30 April 1949)
and the U.S. and Filipino plaques. Topic and title format from reference channel Sealed Orders. Narration 30:01 (Kokoro bm_george 1.2).

- Script `script.md` (88 paragraphs, 4,425 words); sources `research/sources.md` (40 sources, 25 disagreements, editor's notes);
  NARA album finds `research/stills_nara.md`; footage notes `build/footage_notes.md`; risky ranges `build/risk.py`.
- Plan `tools/plan.py` -> `build/storyboard.json`: 405 shots, 145 overlays. Cards are mixed (owner's rule): Brew-style QuoteCards,
  DocDesk (the 1945 report pages and two Signal Corps captions), GlobeMap (Santo Tomas to Los Baños; Miles' route), two Section
  reconstructions (the exercise field; the escape), ArchivePrints, ledger cards, IconCount (2,147).
- Music bed is 8 minutes and loops in assembly (`-stream_loop -1`), to save disk.

Build (when the owner says render):
`HEIGHT=1080 bash tools/render_missing.sh`, `python tools/assemble.py --clips-only --hd`, `python tools/assemble_parts.py 8`.
Then QC (contact sheets, blackdetect, ebur128), thumbnail `thumbnail/thumbnail_A.jpg`, metadata in `youtube.md`.

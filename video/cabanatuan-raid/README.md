# The raid at Cabanatuan (WWII Frontlines)

The 6th Ranger Battalion, the Alamo Scouts and Filipino guerrillas free more than 500 prisoners, most of them survivors of
Bataan and Corregidor, from the camp at Pangatian near Cabanatuan, Luzon, on 30 January 1945. Title format from Sealed
Orders ("The True Story of …"). Narration 30:17 (Kokoro bm_george 1.2), with four original recordings of freed men
(`[CLIP]` lines: an unnamed prisoner on Leyte, 111-ADC-3330, twice; Cpl. Cecil Hay and Sgt. Samuel Goldie, Universal Newsreel).

## Improvements over homma-trial (from LESSONS.md)
1. **A real voice inside the first two minutes** (Homma's first came at minute 8): a freed prisoner at 1:20 says he thought
   it was a massacre. Four real voices in all.
2. **Chapters named the way veterans search**: 6th Ranger Battalion, Alamo Scouts, Lingayen, Guimba, Cabu bridge, P-61
   "Hard to Get", Capt. James Fisher.
3. **Real film of the event itself** instead of stand-ins at the key beats: the Signal Corps footage of the raid in
   "Appointment in Tokyo" (1945) for the march, the grass, the wire and the freed men walking out; quote cards big and
   centred (owner, 21 Nov 2026); every 4-row bar chart cut to 3 rows after the card QC.

- Script `script.md` (87 paragraphs, ~4,450 narrated words); sources `research/sources.md` (31 sources, 19 disagreements).
- Plan `tools/plan.py` (from build/plan_*.py) -> `build/storyboard.json`: 414 shots, 123 overlays (12 QuoteCards, 26
  ArchivePrints, 2 DocDesk, 3 GlobeMaps, Section crawl reconstruction, Chart of the plan, IconCount 511/225, bars, timeline).
  Risky ranges: `build/risk.py` (bad 0).

Build: `HEIGHT=1080 bash tools/render_missing.sh`, `python tools/assemble.py --clips-only --hd`, `python tools/assemble_parts.py 8`,
then QC, `python tools/thumbs_episode.py`, `python tools/srt.py`.

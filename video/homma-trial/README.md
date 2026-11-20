# The trial of General Homma (WWII Frontlines)

Lt. Gen. Masaharu Homma, commander of the Japanese army that took Bataan, tried by a U.S. military commission in Manila
(3 Jan – 11 Feb 1946) for the Bataan Death March, told from the 3,365-page trial record: the survivors who testified, Homma on the
stand, Fujiko Homma's testimony, the five-minute verdict, the Murphy and Rutledge dissents, Fujiko's meeting with MacArthur,
MacArthur's review and the firing squad at Los Baños (3 Apr 1946). Title format from WWII Box's MacArthur series.
Narration 28:00 (Kokoro bm_george 1.2), with the original 1945 recording of Chaplain Leslie Zimmerman (ADC-5281) spliced in as
paragraph 23 (`[CLIP file t0 t1]` lines in script.md; `tools/tts_kokoro.py` cuts the soundtrack and matches its loudness; the
plan shows the same film in sync).

- Script `script.md` (87 paragraphs, ~4,200 words); sources `research/sources.md` (32 sources, 18 disagreements, witnesses by
  trial day, quote list).
- Trial pages for the 3D desk shots come from the archive.org microfilm item `USMilitaryCommissionRecordsMicrofilm` (Reels 83–84):
  page images via BookReaderImages.php, located with the item's full-text search (`fulltext/inside.php`), cropped to the paper,
  then `tools/doc_desk.py page`. DocDesk aspect = height / width.
- Plan `tools/plan.py` (built from build/plan_*.py) -> `build/storyboard.json`: 386 shots, 105 overlays (QuoteCards, DocDesk
  transcript pages, GlobeMaps of Luzon, the march route and Los Baños, a Section reconstruction of the headquarters by the road,
  IconCount of 136 witnesses, ledger bars/quotes/timelines, ArchivePrints). Risky ranges: `build/risk.py`.

Build:
`HEIGHT=1080 bash tools/render_missing.sh`, `python tools/assemble.py --clips-only --hd`, `python tools/assemble_parts.py 8`.
Then QC (contact sheets, blackdetect, ebur128), thumbnail `python tools/thumbs_episode.py`, captions `python tools/srt.py`.

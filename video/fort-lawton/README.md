# Fort Lawton, 1944 (WWII Frontlines)

On the night of August 14, 1944, a riot between Black American soldiers and Italian prisoners at Fort Lawton, Seattle, ended
with an Italian POW, Guglielmo Olivotto, found hanged on the obstacle course. The Army tried 43 Black soldiers, convicted 28,
and in 2007 ruled that the trial had been fundamentally unfair. Script in `script.md`, sources in `research/sources.md`
(documents in `research/docs/`), footage in `research/footage_credits.md`.

The first episode with highlighted documents (`LedgerDocument` cards): the sentences come from the PDFs' own text layer via
`python tools/doc_spans.py --pdf <file> <page> <key> "<phrase>"`, checked by eye in `build/doc_check_<key>.jpg`.
Pipeline as in the method skill: `tools/tts_kokoro.py`, `tools/align.py`, `tools/plan.py`, `tools/render_missing.sh`,
`tools/assemble.py`, `tools/srt.py`, `tools/thumbnail.py`.

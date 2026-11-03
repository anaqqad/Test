# Krug and Stephan: one weekend in Detroit, 1942

"A German POW Escaped to Detroit. The Man Who Fed Him Was Sentenced to Hang." Same pipeline and house style as
`../hereford-hunger` (copied tools and Remotion cards; `node_modules` moved here from hereford-hunger):

```
bash tools/fetch_footage.sh                                  # ~0.6 GB of public-domain film
python tools/fetch_stills.py                                 # Commons photos -> assets/stills/ (then blur Krug's insignia, see below)
bash tools/shots.sh                                          # source-film cut points -> build/shots/
python <kokoro venv> tools/tts_kokoro.py bm_george 1.2       # channel voice; writes audio/
python tools/align.py                                        # word timings (faster-whisper small.en)
(cd remotion && node ../tools/map_data.mjs ../build/states-10m.json src/data/map.json)   # route map
python tools/plan.py                                         # -> build/storyboard.json
HEIGHT=720 bash tools/render_missing.sh                      # cards -> build/overlays/
python tools/assemble.py                                     # -> out/krug-detroit.mp4 (720p)
python tools/thumbnail.py                                    # -> thumbnail/thumbnail_A.jpg, _B.jpg
python tools/srt.py                                          # -> out/krug-detroit.srt
```
Pronunciations for Kokoro (Krug, Normandie, Milan, von Werra, Rintelen, Bertelmann) are in `spoken()` in
`tools/tts_cosyvoice.py`. Set `PYTHONUTF8=1` on Windows when running the Python tools.

`assets/stills/krug_1942.jpg` has the Luftwaffe cap eagle, cap wreath, breast eagle and tunic badge blurred (Gaussian,
badges only, never the face). No Nazi symbol is on screen.

Sources: `research/sources.md` (the main source is the Sixth Circuit opinion, a public-domain court record).
Credits: `research/footage_credits.md`. Metadata: `youtube.md`.

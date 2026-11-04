# Whitewater: the POW camp with no fence, and the teacher, 1944

"German POWs Found a Camp With No Fence. Then Two Knocked on a Teacher's Door." Same pipeline and house style as
`../krug-detroit` (copied tools and Remotion cards; `node_modules` and `bed.wav` moved here from krug-detroit):

```
bash tools/fetch_footage.sh                                  # ~1.2 GB of public-domain film
python tools/fetch_stills.py                                 # Commons photos -> assets/stills/ (then blur insignia, see below)
bash tools/shots.sh                                          # source-film cut points -> build/shots/
python <kokoro venv> tools/tts_kokoro.py bm_george 1.2       # channel voice; writes audio/
python tools/align.py                                        # word timings (faster-whisper small.en)
python tools/plan.py                                         # -> build/storyboard.json
HEIGHT=720 bash tools/render_missing.sh                      # cards -> build/overlays/
python tools/assemble.py                                     # -> out/whitewater-camp.mp4 (720p)
python tools/thumbnail.py                                    # -> thumbnail/thumbnail_A.jpg, _B.jpg
python tools/srt.py                                          # -> out/whitewater-camp.srt
```
Pronunciations for Kokoro (Afrika Korps, Chastko, Chrun, Zaporoza, Dauphin, Reinhard, Willi, Waiser, Olha, Horod) are in
`spoken()` in `tools/tts_cosyvoice.py`. Set `PYTHONUTF8=1` on Windows when running the Python tools.

`assets/stills/pows_debarking_1942.jpg` has the eagle badges on caps and tunics blurred (Gaussian, badges only, never a
face); the original is kept in `build/`. No Nazi symbol is on screen.

Sources: `research/sources.md` (the main source is Bill Waiser, "Riding Mountain POWs: The Teacher's Tale," *Manitoba
History* 61, 2009). Credits: `research/footage_credits.md`. Metadata: `youtube.md`.

# Camp Hereford: la fame and the paintings of Umbarger

"Hungry Italian POWs Ate Rattlesnakes in Texas. Then a Church Fed Them." Same pipeline and house style as `../pow-trains`
(copied tools and Remotion cards; `node_modules` moved here from pow-trains):

```
bash tools/fetch_footage.sh                                  # ~0.45 GB of public-domain film
bash tools/shots.sh                                          # source-film cut points -> build/shots/
python <kokoro venv> tools/tts_kokoro.py bm_george 1.2       # channel voice; writes audio/
python tools/align.py                                        # word timings (faster-whisper small.en)
python tools/plan.py                                         # -> build/storyboard.json
HEIGHT=720 bash tools/render_missing.sh                      # cards -> build/overlays/
python tools/assemble.py                                     # -> out/hereford-hunger.mp4 (720p)
python tools/thumbnail.py                                    # -> thumbnail/thumbnail_A.jpg, _B.jpg
python tools/srt.py                                          # -> out/hereford-hunger.srt
```
Pronunciations for Kokoro (la fame, cacciatore, bocce, FitzSimon, Cabitto) are in `spoken()` in `tools/tts_cosyvoice.py`.
Set `PYTHONUTF8=1` on Windows when running the Python tools.

Sources: `research/sources.md`. Credits: `research/footage_credits.md`. Metadata: `youtube.md`.

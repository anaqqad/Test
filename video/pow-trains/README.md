# What 370,000 German POWs saw from American trains

"What 370,000 German POWs Saw When Their Trains Crossed America". Same pipeline and house style as
`../box-1142`, plus a `BigNumber` card (remotion/src/overlays.tsx) so the number is the first thing on screen, made to run on the Windows PC with little free disk:

```
bash tools/fetch_footage.sh                                  # ~0.45 GB of public-domain film
bash tools/shots.sh                                          # source-film cut points -> build/shots/
python tools/make_music.py 625 assets/music/bed.wav
python <kokoro venv> tools/tts_kokoro.py bm_george 1.2       # draft = channel voice; writes audio/
python tools/align.py                                        # word timings (faster-whisper small.en)
python tools/plan.py                                         # -> build/storyboard.json
bash tools/render_missing.sh                                 # cards -> build/overlays/*.webm (720p VP9 with alpha, retries on a full disk)
python tools/assemble.py                                     # -> out/pow-trains.mp4 (720p; --hd for 1080p)
python tools/thumbnail.py                                    # -> thumbnail/thumbnail_A.jpg, _B.jpg
python tools/srt.py                                          # -> out/pow-trains.srt
python ../../tools/upload_youtube.py . --dry-run             # then without --dry-run: uploads as private
```
Differences from McCoy (shared with Camp Tracy): overlays are VP9 WebM instead of ProRes (a few MB each instead of hundreds), the default build is
720p, file I/O is UTF-8, photos are measured with Pillow (no ImageMagick), and Remotion downloads its own headless Chrome
(`BROWSER=<path>` to use another). Set `PYTHONUTF8=1` on Windows when running the Python tools.

Sources: `research/sources.md`. Credits: `research/footage_credits.md`. Metadata and thumbnail prompt: `youtube.md`.

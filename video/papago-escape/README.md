# Papago Park: the tunnel, the boat and the dry river

"German POWs Dug a Tunnel to Float to Mexico. The River Was Dry." Same pipeline and house style as
`../interrogation-sukiyaki`, made to run on the Windows PC with little free disk:

```
bash tools/fetch_footage.sh                                  # ~0.9 GB of public-domain film
bash tools/shots.sh                                          # source-film cut points -> build/shots/
python tools/make_music.py 625 assets/music/bed.wav
(cd remotion && node ../tools/map_data.mjs ../build/states-10m.json src/data/map.json)  # Arizona map (us-atlas@3.0.1)
python <kokoro venv> tools/tts_kokoro.py bm_george 1.2       # draft = channel voice; writes audio/
python tools/align.py                                        # word timings (faster-whisper small.en)
python tools/plan.py                                         # -> build/storyboard.json
cd remotion && npm ci && node render.mjs && cd ..            # cards -> build/overlays/*.webm (VP9 with alpha)
python tools/assemble.py                                     # -> out/papago-escape.mp4 (720p; --hd for 1080p)
python tools/srt.py                                          # -> out/papago-escape.srt
python ../../tools/upload_youtube.py . --dry-run             # then without --dry-run: uploads as private
```
Differences from McCoy (shared with Camp Tracy): overlays are VP9 WebM instead of ProRes (a few MB each instead of hundreds), the default build is
720p, file I/O is UTF-8, photos are measured with Pillow (no ImageMagick), and Remotion downloads its own headless Chrome
(`BROWSER=<path>` to use another). Set `PYTHONUTF8=1` on Windows when running the Python tools.

Sources: `research/sources.md`. Credits: `research/footage_credits.md`. Metadata and thumbnail prompt: `youtube.md`.

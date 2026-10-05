# Camp McCoy: Japanese POWs and baseball

"Japanese POWs Were Told to Die Before Capture. Then a Wisconsin Camp Handed Them Baseball Gloves."
It uses the same pipeline and house style as `../chicago-lights` (see that README). The Remotion `node_modules` is a
symlink to the Chicago project's, so run `npm install` there first.

```
bash ../chicago-lights/tools/fetch_footage.sh && bash tools/fetch_footage.sh
bash tools/shots.sh
python3 tools/tts_kokoro.py bm_george 1.2      # or tools/tts_cosyvoice.py on the GPU PC
python3 tools/align.py && python3 tools/plan.py
cd remotion && node render.mjs && cd .. && python3 tools/assemble.py
```
Metadata, the thumbnail prompt and sources: `youtube.md`, `research/sources.md`, `research/footage_credits.md`.

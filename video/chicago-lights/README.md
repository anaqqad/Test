# Chicago lights: the Reinhold Pabel episode

"German POWs Came From a Blacked-Out Continent. Then One Rode Into Chicago at Night." Built to
`VIDEO_STYLE_BLUEPRINT.md`: B&W archival footage cut on the narration's words (median shot ~3.4 s),
navy/gold/serif cards (memoir excerpts, AP clipping, two timelines, route map, date lower thirds),
honest context labels, a silent subscribe card at 36 % and a spoken comment CTA near the end.

## Pipeline
```
bash tools/fetch_footage.sh                 # public-domain films -> assets/footage/ (~2.3 GB)
bash tools/shots.sh                         # source-film shot boundaries -> build/shots/
python3 tools/make_music.py 650 assets/music/bed.wav
python3 tools/tts_kokoro.py bm_george 1.2   # or tools/tts_cosyvoice.py (below)
python3 tools/align.py                      # word timestamps (faster-whisper) -> audio/words.json
python3 tools/plan.py                       # shot plan -> build/storyboard.json
cd remotion && npm install && node render.mjs && cd ..   # cards -> build/overlays/*.mov
python3 tools/assemble.py                   # -> out/chicago-lights.mp4
```
Changing the voice only means re-running from step 4: every cut and card is anchored to words, so
timings follow the new narration automatically.

## Redoing the narration with CosyVoice on the RTX 3090 Ti
The cloud draft uses Kokoro (`bm_george`). On this PC (4 CPU cores, no GPU) CosyVoice-300M-SFT ran at
about 4.5x slower than real time, so ~8.5 minutes of narration would take ~40 minutes. On a 3090 Ti
expect roughly 1-3 minutes, plus the one-time ~2.5 GB model download.

```
git clone --recursive https://github.com/FunAudioLLM/CosyVoice.git
pip install -r CosyVoice/requirements.txt          # CUDA build of torch
huggingface-cli download FunAudioLLM/CosyVoice-300M-SFT --local-dir models/CosyVoice-300M-SFT
python tools/tts_cosyvoice.py CosyVoice models/CosyVoice-300M-SFT 英文男 0.82
```
Speed 0.82 brings the built-in English male speaker down to ~155 words/min (the reference pace).
To use a cloned voice instead, swap `inference_sft` for `inference_zero_shot` with your sample in
`tools/tts_cosyvoice.py`. Years and ordinals are converted to spoken form there ("nineteen forty-five"),
because CosyVoice reads "1945" as "one thousand nine hundred...".

## Before publishing
- Set the channel name on the subscribe card: `CHANNEL` in `tools/plan.py`.
- Metadata and sources for the description: `youtube.md`, `research/sources.md`, `research/footage_credits.md`.

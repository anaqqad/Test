# Hugo Krauss and Camp Hearne (WWII Frontlines)

A New Yorker came back to America as a German POW, said he wanted to stay, and was beaten to death by fellow prisoners
at Camp Hearne, Texas, in December 1943; the case broke two years later when one of the killers confessed to a young
woman whose car he had fixed on the road. Script in `script.md`, sources in `research/sources.md`.

## Pipeline
```
PYTHONUTF8=1 /c/Users/anass/Desktop/kokoro/venv/Scripts/python.exe tools/tts_kokoro.py bm_george 1.2
PYTHONUTF8=1 python tools/align.py
python tools/fetch_footage.py      # best-quality archive copies (never 512kb); big masters re-encoded from the stream
python tools/fetch_stills.py       # Commons photos (the ship photo's badges are blurred; original in build/)
bash tools/shots.sh
PYTHONUTF8=1 python tools/plan.py
HEIGHT=720 bash tools/render_missing.sh
PYTHONUTF8=1 python tools/assemble.py --only-base
PYTHONUTF8=1 python tools/assemble.py
PYTHONUTF8=1 python tools/srt.py
python tools/thumbnail.py
```
Footage gets the no-AI clean-up in `assemble.py` (`CLEAN`: deinterlace, light denoise, lanczos, mild sharpening).

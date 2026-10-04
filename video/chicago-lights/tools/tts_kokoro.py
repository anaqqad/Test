"""Narration with Kokoro-82M (free, local). Placeholder voice until the CosyVoice pass on the GPU PC.
Same outputs as tts_cosyvoice.py: audio/narration.wav and audio/paragraphs.json (with "spoken" text).
Usage: python3 tools/tts_kokoro.py [voice] [speed]"""
import json, re, sys
from pathlib import Path
import numpy as np, soundfile as sf
from kokoro import KPipeline

ROOT = Path(__file__).resolve().parent.parent
VOICE = sys.argv[1] if len(sys.argv) > 1 else "bm_george"
SPEED = float(sys.argv[2]) if len(sys.argv) > 2 else 1.08  # ~155 wpm like the reference
SR = 24000
src = (ROOT / "tools/tts_cosyvoice.py").read_text()
exec("import re\n" + src[src.index("ONES ="):src.index("paras, act")])  # shared spoken-form rules (years, ordinals)

paras, act = [], None
for l in (ROOT / "script.md").read_text().splitlines():
    if l.startswith("## "): act = l[3:].strip(); continue
    if not l.strip() or l.startswith(("#", "<!--")): continue
    paras.append({"act": act, "text": l.strip(), "spoken": spoken(l.strip())})

pipe = KPipeline(lang_code="b" if VOICE.startswith("b") else "a")
out, t = [], 0.0
for i, p in enumerate(paras):
    gap = 0.25 if i == 0 else (1.1 if paras[i - 1]["act"] != p["act"] else 0.7)
    out.append(np.zeros(int(gap * SR), np.float32)); t += gap
    chunks = []
    for s in [s for s in re.split(r"(?<=[.!?])\s+", p["spoken"]) if s]:
        a = np.concatenate([np.asarray(x) for _, _, x in pipe(s, voice=VOICE, speed=SPEED)])
        chunks += [a.astype(np.float32), np.zeros(int(0.3 * SR), np.float32)]
    audio = np.concatenate(chunks[:-1])
    p["start"] = round(t, 3); t += len(audio) / SR; p["end"] = round(t, 3)
    out.append(audio)
    print(f"{i:02d} {p['start']:7.2f}-{p['end']:7.2f} {p['text'][:50]}", flush=True)
out.append(np.zeros(int(1.5 * SR), np.float32))
wav = np.concatenate(out); wav = wav / max(1e-6, np.abs(wav).max()) * 0.89
sf.write(ROOT / "audio/narration.wav", wav, SR)
json.dump(paras, open(ROOT / "audio/paragraphs.json", "w"), indent=1, ensure_ascii=False)
words = sum(len(p["text"].split()) for p in paras)
print("total", round(len(wav) / SR, 2), "s,", round(words / (len(wav) / SR) * 60), "wpm")

"""Narration with Kokoro-82M (free, local). Placeholder voice until the CosyVoice pass on the GPU PC.
Same outputs as tts_cosyvoice.py: audio/narration.wav and audio/paragraphs.json (with "spoken" text).
Usage: python3 tools/tts_kokoro.py [voice] [speed]"""
import json, re, sys
from pathlib import Path
import numpy as np
try:
    import soundfile as sf
except ImportError:  # e.g. a bare Kokoro venv: write 16-bit PCM with the standard library instead
    import wave
    class sf:
        @staticmethod
        def write(path, data, sr):
            with wave.open(str(path), "wb") as w:
                w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
                w.writeframes((np.clip(data, -1, 1) * 32767).astype("<i2").tobytes())
from kokoro import KPipeline

ROOT = Path(__file__).resolve().parent.parent
VOICE = sys.argv[1] if len(sys.argv) > 1 else "bm_george"
SPEED = float(sys.argv[2]) if len(sys.argv) > 2 else 1.08  # ~155 wpm like the reference
SR = 24000
src = (ROOT / "tools/tts_cosyvoice.py").read_text(encoding="utf-8")
exec("import re\n" + src[src.index("ONES ="):src.index("paras, act")])  # shared spoken-form rules (years, ordinals)

PRON = {"Chichi Jima": "Chee-chee Jee-mah", "Jima": "Jee-mah", "Minami": "Mee-nah-mee", "Ani": "Ah-nee", "Haha": "Hah-hah",
        "Futami": "Foo-tah-mee", "Tachibana": "Tah-chee-bah-nah", "Matoba": "Mah-toh-bah", "Woellhof": "Wool-hoff",
        "Mierzejewski": "Meer-zeh-jef-skee", "Mierzejewski's": "Meer-zeh-jef-skee's", "Iwatake": "Ee-wah-tah-keh",
        "Nobuaki": "No-boo-ah-kee", "Horie": "Ho-ree-eh", "Kunizo": "Koo-nee-zo", "Yoshio": "Yo-shee-oh",
        "Sueo": "Soo-eh-oh", "Yoshitaka": "Yo-shee-tah-kah", "Ogasawara": "Oh-gah-sah-wah-rah", "Jacinto": "Juh-sin-toh",
        "Bonin": "Bo-nin", "Bonins": "Bo-nins", "Majuro": "Mah-joo-ro", "Kwajalein": "Kwah-jah-lin", "Ulithi": "Oo-lee-thee",
        "Mershon": "Mur-shon", "Mershon's": "Mur-shon's", "Kohler": "Koh-ler", "Wykes": "Wikes", "Rixey": "Rix-ee", "Nadeau": "Nah-doe",
        "Delaney": "Deh-lay-nee", "Mori": "Mo-ree", "Donnet": "Don-ay", "Melvin": "Mel-vin", "Bronson": "Bron-son"}
def pron(t):
    for k, v in sorted(PRON.items(), key=lambda kv: -len(kv[0])):
        t = re.sub(r"(?<![\w-])" + re.escape(k) + r"(?![\w-])", v, t)
    return t

paras, act = [], None
for l in (ROOT / "script.md").read_text(encoding="utf-8").splitlines():
    if l.startswith("## "): act = l[3:].strip(); continue
    if not l.strip() or l.startswith(("#", "<!--")): continue
    m = re.match(r"\[CLIP (\S+) ([\d.]+) ([\d.]+)\]\s*(.*)", l.strip())
    if m:
        paras.append({"act": act, "text": m.group(4), "spoken": spoken(m.group(4)), "clip": [m.group(1), float(m.group(2)), float(m.group(3))]})
        continue
    paras.append({"act": act, "text": l.strip(), "spoken": pron(spoken(l.strip()))})

pipe = KPipeline(lang_code="b" if VOICE.startswith("b") else "a")
out, t = [], 0.0
for i, p in enumerate(paras):
    gap = 0.25 if i == 0 else (1.1 if paras[i - 1]["act"] != p["act"] else 0.7)
    out.append(np.zeros(int(gap * SR), np.float32)); t += gap
    chunks = []
    if p.get("clip"):  # original archive recording, played as it is (cut from the film's soundtrack)
        f, c0, c1 = p["clip"]
        import subprocess
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(c0), "-t", str(c1 - c0), "-i", str(ROOT / "assets/footage" / f), "-ac", "1", "-ar", str(SR),
                              "-af", "highpass=f=90,lowpass=f=7000,afade=t=in:d=0.15,afade=t=out:st=" + str(round(c1 - c0 - 0.3, 2)) + ":d=0.3", "-f", "f32le", "-"], capture_output=True).stdout
        chunks = [np.frombuffer(raw, np.float32).copy()]
    else:
      for s in [s for s in re.split(r"(?<=[.!?])\s+", p["spoken"]) if s]:
        a = np.concatenate([np.asarray(x) for _, _, x in pipe(s, voice=VOICE, speed=SPEED)])
        chunks += [a.astype(np.float32), np.zeros(int(0.3 * SR), np.float32)]
    audio = np.concatenate(chunks if p.get("clip") else chunks[:-1])
    p["start"] = round(t, 3); t += len(audio) / SR; p["end"] = round(t, 3)
    out.append(audio)
    print(f"{i:02d} {p['start']:7.2f}-{p['end']:7.2f} {p['text'][:50]}", flush=True)
out.append(np.zeros(int(1.5 * SR), np.float32))
rms = lambda a: float(np.sqrt(np.mean(a[np.abs(a) > 1e-3] ** 2))) if np.any(np.abs(a) > 1e-3) else 1.0
nar = [a for a, p in zip(out[1::2], paras) if not p.get("clip")]
target = np.median([rms(a) for a in nar])
for k, p in enumerate(paras):
    if p.get("clip"):
        a = out[2 * k + 1]; out[2 * k + 1] = np.clip(a * (target / rms(a)), -1, 1)
wav = np.concatenate(out); wav = wav / max(1e-6, np.abs(wav).max()) * 0.89
sf.write(ROOT / "audio/narration.wav", wav, SR)
json.dump(paras, open(ROOT / "audio/paragraphs.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
words = sum(len(p["text"].split()) for p in paras)
print("total", round(len(wav) / SR, 2), "s,", round(words / (len(wav) / SR) * 60), "wpm")

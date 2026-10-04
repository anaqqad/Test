"""Narration with CosyVoice-300M-SFT, built-in speaker '英文男' (English male). Free and local.
One script paragraph = one scene. Writes audio/narration.wav and audio/paragraphs.json.
Run with the CosyVoice venv:  python tools/tts_cosyvoice.py <CosyVoice repo> <model dir>"""
import json, re, sys, time
from pathlib import Path
import numpy as np, soundfile as sf, torch

REPO, MODEL = sys.argv[1], sys.argv[2]
SPK = sys.argv[3] if len(sys.argv) > 3 else "英文男"
SPEED = float(sys.argv[4]) if len(sys.argv) > 4 else 0.82  # reference narration runs ~155 wpm
sys.path[:0] = [REPO, f"{REPO}/third_party/Matcha-TTS"]
from cosyvoice.cli.cosyvoice import CosyVoice  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()
ORD = {1: "first", 2: "second", 3: "third", 5: "fifth", 8: "eighth", 9: "ninth", 11: "eleventh", 12: "twelfth"}

def two(n):
    return ONES[n] if n < 20 else TENS[n // 10] + ("-" + ONES[n % 10] if n % 10 else "")

def year(y):
    return f"{two(y // 100)} {two(y % 100)}" if y % 100 >= 10 else f"{two(y // 100)} oh {ONES[y % 100]}"

def ordinal(n):
    if n in ORD: return ORD[n]
    w = two(n)
    if n > 20 and n % 10 in ORD: return w.rsplit("-", 1)[0] + "-" + ORD[n % 10]
    return w + ("th" if not w.endswith("y") else "") if not w.endswith("y") else w[:-1] + "ieth"

def spoken(t):
    t = re.sub(r"\b(\d{1,2})(st|nd|rd|th)\b", lambda m: ordinal(int(m.group(1))), t)
    t = re.sub(r"\b(1[89]\d\d)\b", lambda m: year(int(m.group(1))), t)
    t = t.replace("V-E Day", "V E Day").replace("FBI", "F B I")
    return t

paras, act = [], None
for l in (ROOT / "script.md").read_text().splitlines():
    if l.startswith("## "): act = l[3:].strip(); continue
    if not l.strip() or l.startswith(("#", "<!--")): continue
    paras.append({"act": act, "text": l.strip(), "spoken": spoken(l.strip())})

torch.set_num_threads(4)
cv = CosyVoice(MODEL, load_jit=False, load_trt=False, fp16=False)
SR = cv.sample_rate
out, t = [], 0.0
for i, p in enumerate(paras):
    gap = 0.25 if i == 0 else (1.1 if paras[i - 1]["act"] != p["act"] else 0.7)
    out.append(np.zeros(int(gap * SR), np.float32)); t += gap
    t0 = time.time()
    sents = [s for s in re.split(r"(?<=[.!?])\s+", p["spoken"]) if s]
    chunks = []
    for s in sents:
        w = torch.cat([o["tts_speech"] for o in cv.inference_sft(s, SPK, stream=False, speed=SPEED)], 1).squeeze(0).numpy()
        chunks += [w, np.zeros(int(0.3 * SR), np.float32)]
    audio = np.concatenate(chunks[:-1]).astype(np.float32)
    p["start"] = round(t, 3); t += len(audio) / SR; p["end"] = round(t, 3)
    out.append(audio)
    print(f"{i:02d} {p['start']:7.2f}-{p['end']:7.2f} ({time.time()-t0:.0f}s) {p['text'][:50]}", flush=True)
out.append(np.zeros(int(1.5 * SR), np.float32))
wav = np.concatenate(out); wav = wav / max(1e-6, np.abs(wav).max()) * 0.89
(ROOT / "audio").mkdir(exist_ok=True)
sf.write(ROOT / "audio/narration.wav", wav, SR)
json.dump(paras, open(ROOT / "audio/paragraphs.json", "w"), indent=1, ensure_ascii=False)
print("total", round(len(wav) / SR, 2), "s")

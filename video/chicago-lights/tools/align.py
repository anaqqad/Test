"""Word timestamps for the narration: faster-whisper per paragraph, mapped onto the script's own
(spoken-form) words so every anchor in plan.py can be found. Writes audio/words.json."""
import json, re
from pathlib import Path
import numpy as np, soundfile as sf
from faster_whisper import WhisperModel

ROOT = Path(__file__).resolve().parent.parent
norm = lambda w: re.sub(r"[^a-z0-9]", "", w.lower())

paras = json.load(open(ROOT / "audio/paragraphs.json"))
wav, sr = sf.read(ROOT / "audio/narration.wav", dtype="float32")
if wav.ndim > 1: wav = wav.mean(1)
model = WhisperModel("small.en", device="cpu", compute_type="int8")
out = []
for p in paras:
    a, b = int(p["start"] * sr), int(p["end"] * sr)
    clip = wav[a:b]
    if sr != 16000:
        clip = np.interp(np.arange(0, len(clip), sr / 16000), np.arange(len(clip)), clip).astype(np.float32)
    segs, _ = model.transcribe(clip, word_timestamps=True, beam_size=5, language="en")
    heard = [w for s in segs for w in s.words]
    words = p["spoken"].split()
    res = [None] * len(words)
    j = 0
    for i, w in enumerate(words):
        for k in range(j, min(j + 5, len(heard))):
            if norm(heard[k].word) == norm(w):
                res[i] = (heard[k].start, heard[k].end); j = k + 1; break
    dur = (b - a) / sr
    anchors = [(-1, 0.0, 0.0)] + [(i, r[0], r[1]) for i, r in enumerate(res) if r] + [(len(words), dur, dur)]
    for (i0, _, e0), (i1, s1, _) in zip(anchors, anchors[1:]):
        gap = i1 - i0 - 1
        for n in range(1, gap + 1):
            res[i0 + n] = (e0 + (s1 - e0) * (n - 1) / gap, e0 + (s1 - e0) * n / gap)
    hit = sum(1 for x in anchors[1:-1])
    out.append([{"text": w, "start": round(p["start"] + r[0], 3), "end": round(p["start"] + r[1], 3)} for w, r in zip(words, res)])
    print(f"{len(out)-1:02d} matched {hit}/{len(words)} words")
json.dump(out, open(ROOT / "audio/words.json", "w"), indent=0)

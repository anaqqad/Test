# Mix narration + Hear-It clips for longform.mjs: python3 longform_mix.py mix.json out.wav
# Narration is levelled to -16 LUFS overall; clips are pre-levelled; loudness is only ever turned down at the end.
import json, subprocess, sys
import numpy as np
SR = 48000
spec = json.load(open(sys.argv[1]))
out = np.zeros(int((spec["total"] + 1) * SR), np.float32)
def load(f):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32)
for it in spec["items"]:
    a = load(it["f"]) * (1.0 if it["kind"] == "vo" else 0.9)
    i = int(it["t"] * SR); out[i:i + len(a)] += a[: len(out) - i]
tmp = sys.argv[2] + ".f32"; out.tofile(tmp)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", tmp,
                "-af", "loudnorm=I=-16:TP=-1.5:LRA=11,pan=stereo|c0=c0|c1=c0", "-ar", str(SR), sys.argv[2]], check=True)
import os; os.remove(tmp)
print("mix", sys.argv[2], round(len(out) / SR, 1), "s")

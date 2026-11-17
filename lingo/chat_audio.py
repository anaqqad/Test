# Sound mix for chat.mjs (Blueprint 03): python3 chat_audio.py <timeline.json> <out.wav>
# Music bed (real, credited CC track) plays only under beats with "music": true and cuts to silence on deadpan
# beats; the music keeps its place between windows (it does not restart). Sound effects: chat/assets/sfx/*.wav.
import json, os, subprocess, sys, wave, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
SR = 44100
tl = json.load(open(sys.argv[1]))
dur = tl["dur"]
out = np.zeros(int(SR * (dur + 1)), np.float32)

def load(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()

m = tl.get("music")
if m:
    mus = load(os.path.join(HERE, m["file"])) * 10 ** (m.get("gain", -15) / 20)
    cursor = int(SR * m.get("start", 0))
    beats = tl["beats"]
    for k, b in enumerate(beats):
        if not b["music"]:
            continue
        a = b["start"]; e = beats[k + 1]["start"] if k + 1 < len(beats) else dur
        i0, i1 = int(SR * a), int(SR * e)
        n = i1 - i0
        seg = np.resize(mus[cursor % len(mus):], n) if cursor % len(mus) + n > len(mus) else mus[cursor % len(mus): cursor % len(mus) + n].copy()
        f = min(int(SR * 0.025), n // 2)
        seg[:f] *= np.linspace(0, 1, f); seg[n - f:] *= np.linspace(1, 0, f)
        out[i0:i1] += seg; cursor += n

cache = {}
for b in tl["beats"]:
    for s in b["sfx"]:
        p = os.path.join(HERE, "chat", "assets", "sfx", s["name"] + ".wav")
        if s["name"] not in cache:
            cache[s["name"]] = load(p)
        x = cache[s["name"]]; i0 = int(SR * s["at"])
        out[i0:i0 + len(x)] += x[: len(out) - i0]
out = out[: int(SR * dur)]
out = out / max(1.0, np.abs(out).max() / 0.95)
with wave.open(sys.argv[2], "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((out * 32767).astype(np.int16).tobytes())
print("audio ->", sys.argv[2])

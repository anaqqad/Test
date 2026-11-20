# v3 mixer for longform3.mjs: python3 longform_mix3.py mix.json out.wav
# Five stems, written next to the mix so the soundtrack stays editable:
#   vo     narration (Kokoro), as recorded
#   words  native-speaker recordings (each pre-levelled to -17 LUFS)
#   amb    location sound (the footage's own audio + named ambiences), levelled to a quiet bed, ducked under words
#   sfx    Foley (page turns, doors), placed with pre-laps
#   score  music cues with crossfades; ducked ~9 dB under narration, silent for every word comparison
# The final mix is loudness-normalised in two passes to -16 LUFS / -1.5 dBTP (linear gain, no pumping).
import json, os, subprocess, sys
import numpy as np

SR = 48000
spec = json.load(open(sys.argv[1])); OUT = sys.argv[2]
N = int((spec["end"] + 0.5) * SR)
os.makedirs(spec["stems"], exist_ok=True)

def load(f, start=0.0, dur=None):
    cmd = ["ffmpeg", "-v", "error", "-ss", str(start), "-i", f]
    if dur: cmd += ["-t", str(dur)]
    r = subprocess.run(cmd + ["-vn", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True)
    if r.returncode: print("  no audio in", os.path.basename(f)); return np.zeros(0, np.float32)
    raw = r.stdout
    return np.frombuffer(raw, np.float32).copy()

def rms_db(a):
    return 20 * np.log10(np.sqrt(np.mean(a.astype(np.float64) ** 2)) + 1e-9)

def place(buf, a, t):
    i = int(t * SR)
    if i < 0: a = a[-i:]; i = 0
    if i >= len(buf): return
    n = min(len(a), len(buf) - i); buf[i:i + n] += a[:n]

def fades(a, fin, fout):
    n1, n2 = int(fin * SR), int(fout * SR)
    if n1: a[:n1] *= np.linspace(0, 1, min(n1, len(a)))[: len(a[:n1])]
    if n2: a[-n2:] *= np.linspace(1, 0, min(n2, len(a)))[: len(a[-n2:])]
    return a

tr = {k: np.zeros(N, np.float32) for k in ["vo", "words", "amb", "sfx", "score"]}
for it in spec["items"]:
    k = it["track"]
    if k == "amb":
        a = load(it["f"], it.get("from", 0), it["d"])
        if len(a) == 0: continue
        a *= 10 ** ((-38 - rms_db(a) + it.get("gain", 0)) / 20)   # quiet bed: ~22 dB under the voice
        place(tr[k], fades(a, it.get("fade", 0.5), it.get("fade", 0.5)), it["t"])
    elif k == "sfx":
        a = load(it["f"]); a *= 10 ** ((-12 - 20 * np.log10(np.max(np.abs(a)) + 1e-9) + it.get("gain", 0)) / 20)
        place(tr[k], a, it["t"])
    else:
        place(tr[k], load(it["f"]), it["t"])

# score: cues crossfade into each other; each track levelled to a bed
t_axis = np.arange(N) / SR
cues = sorted(spec["cues"], key=lambda c: c["t"])
for i, c in enumerate(cues):
    if not c["f"]: continue
    t0 = c["t"]; t1 = cues[i + 1]["t"] if i + 1 < len(cues) else spec["end"]
    if t0 >= spec["end"]: continue
    d = t1 - t0 + 2.0
    a = load(c["f"], c.get("from", 0), d)
    if len(a) == 0: continue
    a *= 10 ** ((-27 - rms_db(a[: SR * 20]) + c.get("gain", 0)) / 20)
    place(tr["score"], fades(a, 1.5, 2.0), t0)

# ducking: score under narration (smoothed envelope), silence for word comparisons; ambience dips under words
def env(x, att=0.05, rel=0.45):
    win = int(0.05 * SR); p = np.sqrt(np.convolve(x.astype(np.float64) ** 2, np.ones(win) / win, mode="same"))
    on = (p > 10 ** (-45 / 20)).astype(np.float64)
    out = np.zeros_like(on); a1, r1 = 1 - np.exp(-1 / (att * SR / 32)), 1 - np.exp(-1 / (rel * SR / 32))
    y = 0.0
    for j in range(0, len(on), 32):
        target = on[j]; y += (target - y) * (a1 if target > y else r1); out[j:j + 32] = y
    return out
duck = 1 - env(tr["vo"]) * (1 - 10 ** (-9 / 20))
mute = np.ones(N)
for a, b in spec["silence"]:
    i0, i1 = int(max(0, a) * SR), int(min(spec["end"], b) * SR)
    if i1 <= i0: continue
    r = int(0.25 * SR)
    mute[i0:i1] = 0
    lo = max(0, i0 - r); mute[lo:i0] = np.minimum(mute[lo:i0], np.linspace(1, 0, i0 - lo))
    hi = min(N, i1 + r); mute[i1:hi] = np.minimum(mute[i1:hi], np.linspace(0, 1, hi - i1))
tr["score"] *= (duck * mute).astype(np.float32)
tr["amb"] *= (0.5 + 0.5 * mute).astype(np.float32)

mix = sum(tr.values())
tmp = OUT + ".f32"; mix.astype(np.float32).tofile(tmp)
meas = subprocess.run(["ffmpeg", "-v", "info", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", tmp, "-af", "pan=stereo|c0=c0|c1=c0,loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
m = json.loads(meas[meas.rindex("{"): meas.rindex("}") + 1])
gain = 10 ** ((-16 - float(m["input_i"])) / 20)
# peaks: a short look-ahead limiter (2 ms attack) catches the few narration/Foley transients above -1.5 dBTP;
# the gain itself stays linear, so nothing pumps.
for k, a in tr.items():
    (a * gain).astype(np.float32).tofile(tmp)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", tmp, os.path.join(spec["stems"], k + ".wav")], check=True)
(mix * gain).astype(np.float32).tofile(tmp)
lim = "alimiter=limit=0.8:attack=2:release=60:level=disabled:asc=1"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", tmp, "-af", lim + ",pan=stereo|c0=c0|c1=c0", OUT], check=True)
chk = subprocess.run(["ffmpeg", "-v", "info", "-i", OUT, "-af", "loudnorm=print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
c = json.loads(chk[chk.rindex("{"): chk.rindex("}") + 1]); print(f"  final: {c['input_i']} LUFS, true peak {c['input_tp']} dBTP")
os.remove(tmp)
print(f"mix {OUT}: {spec['end']:.1f} s, input {m['input_i']} LUFS -> gain {20*np.log10(gain):+.1f} dB; stems in {spec['stems']}")

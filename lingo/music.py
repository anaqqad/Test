"""Soft royalty-free ambient bed (generated, no samples): slow pad chords + gentle plucked arpeggio.
  python3 music.py out.wav seconds"""
import sys, wave, numpy as np

SR = 48000
out, secs = sys.argv[1], float(sys.argv[2])
n = int(SR * secs)
t = np.arange(n) / SR
note = lambda m: 440 * 2 ** ((m - 69) / 12)
# Am - F - C - G, 4 s per chord
chords = [[57, 60, 64, 69], [53, 57, 60, 65], [48, 55, 60, 64], [55, 59, 62, 67]]
bar = 4.0
pad = np.zeros(n)
pl = np.zeros(n)
rng = np.random.default_rng(3)
for k in range(int(secs / bar) + 1):
    ch = chords[k % 4]
    a, b = int(k * bar * SR), min(n, int((k + 1) * bar * SR + SR))
    if a >= n:
        break
    tt = t[a:b] - k * bar
    env = np.clip(tt / 1.2, 0, 1) * np.clip((bar + 1 - tt) / 1.2, 0, 1)
    for m in ch:
        f = note(m)
        pad[a:b] += env * (np.sin(2 * np.pi * f * tt) + 0.5 * np.sin(2 * np.pi * f * 1.003 * tt) + 0.25 * np.sin(2 * np.pi * f * 2.001 * tt))
    # arpeggio: 8 plucks per bar
    for j in range(8):
        m = ch[[0, 1, 2, 3, 2, 1, 2, 3][j]] + 12
        s0 = a + int(j * bar / 8 * SR)
        L = min(int(1.6 * SR), n - s0)
        if L <= 0:
            continue
        tp = np.arange(L) / SR
        pl[s0:s0 + L] += np.exp(-tp * 3.2) * (np.sin(2 * np.pi * note(m) * tp) + 0.3 * np.sin(4 * np.pi * note(m) * tp)) * (0.8 + 0.2 * rng.random())
# gentle low-pass on pad via moving average
k = 24
pad = np.convolve(pad, np.ones(k) / k, mode="same")
mix = 0.10 * pad + 0.16 * pl
# simple stereo widening with a short delay on the right
d = int(0.012 * SR)
left, right = mix, np.concatenate([np.zeros(d), mix[:-d]])
# echo
e = int(0.375 * SR)
for ch in (left, right):
    ch[e:] += 0.25 * ch[:-e]
st = np.stack([left, right], 1)
st /= np.abs(st).max() / 0.8
with wave.open(out, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st * 32767).astype(np.int16).tobytes())

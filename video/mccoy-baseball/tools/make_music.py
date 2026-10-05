"""Original ambient music bed (no samples, no licences): slow minor-key string pad with a sparse
low piano-like pulse. Usage: python3 tools/make_music.py <seconds> <out.wav>"""
import sys
import numpy as np
import soundfile as sf

SR = 48000
dur = float(sys.argv[1]); out = sys.argv[2]
n = int(dur * SR)
t = np.arange(n) / SR
rng = np.random.default_rng(7)

def midi(m): return 440.0 * 2 ** ((m - 69) / 12)

# A minor progression, 12 s per chord: Am, F, C, G, Am, Dm, F, E
chords = [[57, 60, 64, 69], [53, 57, 60, 65], [48, 55, 60, 64], [55, 59, 62, 67],
          [57, 60, 64, 69], [50, 57, 62, 65], [53, 57, 60, 65], [52, 56, 59, 64]]
CH = 12.0
pad = np.zeros((n, 2))
for k in range(int(np.ceil(dur / CH)) + 1):
    notes = chords[k % len(chords)]
    s0 = k * CH - 3.0  # 3 s crossfade between chords
    i0, i1 = max(0, int(s0 * SR)), min(n, int((s0 + CH + 6.0) * SR))
    if i0 >= n: break
    tt = t[i0:i1] - s0
    env = np.clip(tt / 4.0, 0, 1) * np.clip((CH + 6.0 - tt) / 4.0, 0, 1)
    env = env ** 1.5
    for m in notes:
        for ch, det in ((0, -0.07), (1, 0.07)):
            f = midi(m) * (1 + det / 100)
            w = sum(np.sin(2 * np.pi * f * h * tt + rng.uniform(0, 6.28)) / h ** 1.6 for h in range(1, 6))
            pad[i0:i1, ch] += w * env * 0.05
# gentle tremolo
pad *= (0.85 + 0.15 * np.sin(2 * np.pi * 0.13 * t))[:, None]

# sparse low "piano" notes on chord roots every 6 s
piano = np.zeros(n)
for k in range(int(dur / 6)):
    root = chords[(k // 2) % len(chords)][0] - 12
    i0 = int((k * 6 + 0.5) * SR); L = min(n - i0, int(5 * SR))
    if L <= 0: break
    tt = np.arange(L) / SR
    f = midi(root)
    tone = sum(np.sin(2 * np.pi * f * h * tt) * np.exp(-tt * (1.2 + h)) / h for h in range(1, 7))
    piano[i0:i0 + L] += tone * 0.09 * np.minimum(1, tt / 0.01)
mix = pad + piano[:, None]

# cheap reverb: convolve with decaying noise
ir_len = int(2.5 * SR)
ir = rng.normal(0, 1, (ir_len, 2)) * np.exp(-np.arange(ir_len) / SR * 2.4)[:, None]
ir[0] = 0
from numpy.fft import rfft, irfft
L = n + ir_len
N = 1 << int(np.ceil(np.log2(L)))
wet = np.stack([irfft(rfft(mix[:, c], N) * rfft(ir[:, c], N), N)[:n] for c in range(2)], 1)
mix = mix * 0.6 + wet / np.abs(wet).max() * np.abs(mix).max() * 0.55
# low-pass (one-pole) for warmth
a = np.exp(-2 * np.pi * 2500 / SR)
for c in range(2):
    y = np.empty(n); acc = 0.0
    x = mix[:, c]
    # vectorised one-pole via lfilter equivalent
    from scipy.signal import lfilter
    mix[:, c] = lfilter([1 - a], [1, -a], x)
fade = np.minimum(1, np.minimum(t / 3.0, (dur - t) / 4.0))[:, None]
mix *= fade
mix = mix / np.abs(mix).max() * 0.9
sf.write(out, mix.astype(np.float32), SR, subtype="PCM_16")
print("wrote", out, dur, "s")

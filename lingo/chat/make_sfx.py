# Original UI sound effects for the chat-comedy format (Blueprint 03): python3 chat/make_sfx.py
# Synthesised here from sine waves and noise, so they are our own assets. Sound effects only, no music, no speech.
import os, wave, numpy as np
SR = 44100
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "sfx")
os.makedirs(OUT, exist_ok=True)
t = lambda d: np.arange(int(SR * d)) / SR

def tone(f, d, decay=18.0, harm=(1.0, 0.25)):
    x = t(d); env = np.exp(-decay * x) * np.minimum(1, x / 0.004)
    return env * sum(a * np.sin(2 * np.pi * f * (k + 1) * x) for k, a in enumerate(harm))

def cat(*parts, gap=0.0):
    out = []
    for p in parts:
        out += [p, np.zeros(int(SR * gap))]
    return np.concatenate(out)

def save(name, x, peak=0.7):
    x = x / (np.abs(x).max() + 1e-9) * peak
    with wave.open(os.path.join(OUT, name + ".wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())

rng = np.random.default_rng(7)
# message pop: matched to the reference's measured pop (about 160 ms; a G4+D5 pair, then G5+C5 from about 35 ms),
# rebuilt from sine tones so it is our own sound, not a copy of anyone's file
def chord(fs, d, decay, amps):
    x = t(d); env = np.exp(-decay * x) * np.minimum(1, x / 0.003)
    return env * sum(a * (np.sin(2 * np.pi * f * x) + 0.12 * np.sin(4 * np.pi * f * x)) for f, a in zip(fs, amps))
pop = np.zeros(int(SR * 0.2))
p1 = chord((392, 587), 0.07, 38, (1.0, 0.55)); pop[:len(p1)] += p1
p2 = chord((784, 523), 0.16, 26, (1.0, 0.6)); o = int(SR * 0.035); pop[o:o + len(p2)] += p2[: len(pop) - o]
save("pop", pop, 0.5)                                                                    # every new line
save("ping", cat(tone(1568, 0.12, 22), tone(2093, 0.35, 9), gap=0.0), 0.55)             # @mention / highlight
save("join", cat(tone(523, 0.09, 25), tone(784, 0.25, 10), gap=0.02), 0.5)              # someone joins
save("role", cat(*[tone(f, 0.07, 30) for f in (784, 988, 1175)], tone(1568, 0.45, 7), gap=0.005), 0.55)  # role granted
x = t(0.7); sweep = np.sin(2 * np.pi * np.cumsum(110 * np.exp(-2.2 * x) + 38) / SR)
save("boom", sweep * np.exp(-4.2 * x) + 0.4 * rng.standard_normal(len(x)) * np.exp(-30 * x), 0.9)  # impact
x = t(0.32); n = rng.standard_normal(len(x)); f = np.cumsum(np.interp(x, [0, 0.16, 0.32], [400, 2600, 300])) / SR
save("scratch", n * (0.5 + 0.5 * np.sin(2 * np.pi * f)) * np.exp(-3 * x), 0.5)           # record scratch (reversal)
clicks = np.zeros(int(SR * 0.6))
for k in range(5):
    s = int(SR * (0.05 + k * 0.11 + rng.uniform(0, 0.03))); c = rng.standard_normal(300) * np.exp(-np.arange(300) / 40)
    clicks[s:s + 300] += c
save("typing", clicks, 0.25)                                                            # keyboard under a typing indicator
print("sfx ->", OUT, sorted(os.listdir(OUT)))

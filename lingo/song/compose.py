"""Whistled-languages song: real whistle recordings tuned to a melody over a generated beat (owner allowed a generated
beat for this series, 2026-10-30).  python3 song/compose.py -> song/out/song.wav + song/out/timeline.json"""
import json, os, subprocess, wave, hashlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out"); os.makedirs(os.path.join(OUT, "notes"), exist_ok=True)
SR, BPM = 48000, 100
BEAT = 60 / BPM; BAR = 4 * BEAT; E8 = BEAT / 2
SEG = json.load(open(os.path.join(HERE, "segments.json")))

# singer order, caption and stereo position (-1 left .. 1 right)
SINGERS = [
    ("Silbo Gomero", "Spanish, but make it a bird", -0.3),
    ("Bird Language", "Turkish ‘bird language’ has entered the chat", 0.3),
    ("Sfyria", "Greek village group chat, 1 km wide", -0.5),
    ("Whistled Occitan", "Pyrenees shepherds sliding into the DMs", 0.5),
    ("Whistled Yoruba", "Talking drums? We have talking whistles", -0.2),
    ("Hmong", "Flirting, but whistled", 0.2),
    ("Chinantec", "No phone signal in the mountains? No problem", -0.6),
    ("Pirahã", "The Amazon joins the remix", 0.6),
    ("Wayãpi", "French Guiana hunters drop the last line", 0.0),
]
# hook, 4 bars of eighth notes (MIDI note, or None = rest, "-" = hold the previous note)
HOOK = [
    [76, 76, 74, 72, 74, "-", 76, "-"],      # Am
    [72, "-", 69, "-", 72, 74, 76, "-"],     # F
    [79, 79, 76, 72, 74, "-", 72, "-"],      # C
    [71, "-", 69, 67, 69, "-", "-", None],   # G
]
CHORDS = [(57, [57, 60, 64]), (53, [53, 57, 60]), (48, [55, 60, 64]), (55, [55, 59, 62])]  # bass root, pad notes
hz = lambda m: 440.0 * 2 ** ((m - 69) / 12)


def notes_of(bars):
    """[(start_eighth, length_eighths, midi)] for a list of hook bars"""
    seq = [x for b in bars for x in b]
    out = []
    for i, x in enumerate(seq):
        if isinstance(x, int):
            n = 1
            while i + n < len(seq) and seq[i + n] == "-": n += 1
            out.append((i, n, x))
    return out


def read_wav(p):
    w = wave.open(p); n = w.getnframes(); ch = w.getnchannels()
    a = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float32) / 32768
    return a.reshape(-1, ch).mean(axis=1) if ch > 1 else a


SEGIDX = {}
def whistle_note(singer, midi, dur, k=0):
    """one real whistle snippet of `singer`, tuned to `midi` (in the singer's own octave) and stretched to `dur` s"""
    d = SEG[singer]
    segs = [s for s in d["segs"] if s["spread"] < 0.08 and s["end"] - s["start"] >= 0.11 and 600 < s["f0"] < 4000] or d["segs"]
    i = (SEGIDX.get(singer, 0) + k) % len(segs); SEGIDX[singer] = SEGIDX.get(singer, 0) + 1
    s = segs[i]
    target = hz(midi)
    oct_ = round(np.log2(s["f0"] / target)); target *= 2 ** oct_          # stay in the whistler's own register
    src_len = s["end"] - s["start"] - 0.02
    key = hashlib.md5(f"{singer}|{s['start']}|{target:.2f}|{dur:.3f}".encode()).hexdigest()[:12]
    p = os.path.join(OUT, "notes", key + ".wav")
    if not os.path.exists(p):
        tempo = min(4.0, max(0.25, src_len / dur))
        src = os.path.join(HERE, "..", "cache", "audio", d["file"])
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(s["start"] + 0.01), "-t", str(src_len), "-i", src,
                        "-af", f"rubberband=pitch={target / s['f0']:.5f}:tempo={tempo:.4f},highpass=f=400,"
                               f"afade=t=in:d=0.012,apad,atrim=0:{dur:.3f},afade=t=out:st={max(0, dur - 0.06):.3f}:d=0.06",
                        "-ac", "1", "-ar", str(SR), p], check=True)
    a = read_wav(p)
    rms = np.sqrt(np.mean(a ** 2)) + 1e-6
    return a / rms * 0.08


# ---------------- generated beat ----------------
def env(n, a=0.002, r=0.2):
    t = np.arange(n) / SR
    return np.minimum(1, t / a) * np.exp(-t / r)

def kick():
    n = int(0.35 * SR); t = np.arange(n) / SR
    f = 45 + 95 * np.exp(-t / 0.045)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.001, 0.12) * 0.9

def snare():
    n = int(0.25 * SR); t = np.arange(n) / SR; rng = np.random.default_rng(1)
    noise = rng.standard_normal(n); noise = np.diff(noise, prepend=0)
    return (0.55 * noise * env(n, 0.001, 0.07) + 0.4 * np.sin(2 * np.pi * 185 * t) * env(n, 0.001, 0.05)) * 0.55

def clap():
    n = int(0.22 * SR); rng = np.random.default_rng(2); x = np.diff(rng.standard_normal(n), prepend=0)
    e = sum(env(n, 0.0005, 0.012) * (np.arange(n) >= int(d * SR)) for d in (0, 0.011, 0.022)) + env(n, 0.001, 0.08)
    return x * e * 0.22

def hat(open_=False):
    n = int((0.18 if open_ else 0.05) * SR); rng = np.random.default_rng(3)
    x = np.diff(np.diff(rng.standard_normal(n), prepend=0), prepend=0)
    return x * env(n, 0.0005, 0.06 if open_ else 0.012) * 0.08

def bass_note(m, dur):
    n = int(dur * SR); t = np.arange(n) / SR; f = hz(m)
    x = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 2 * f * t) + 0.12 * np.sign(np.sin(2 * np.pi * f * t))
    return x * np.minimum(1, t / 0.005) * np.exp(-t / 0.5) * np.minimum(1, (dur - t) / 0.02).clip(0) * 0.28

def pad(ms, dur):
    n = int(dur * SR); t = np.arange(n) / SR
    x = sum(np.sin(2 * np.pi * hz(m + 12) * t + np.sin(2 * np.pi * 0.3 * t)) + 0.3 * np.sin(2 * np.pi * hz(m + 24) * t) for m in ms)
    return x * np.minimum(1, t / 0.4) * np.minimum(1, (dur - t) / 0.4).clip(0) * 0.035


# ---------------- arrangement ----------------
SECTIONS = []  # (name, bars, singers, hook bars)
SECTIONS.append(("intro", 2, ["Silbo Gomero"], None))
for i, (name, cap, _) in enumerate(SINGERS):
    SECTIONS.append(("solo", 2, [name], HOOK[0:2] if i % 2 == 0 else HOOK[2:4]))
SECTIONS.append(("chorus", 4, [s[0] for s in SINGERS], HOOK))
SECTIONS.append(("break", 2, ["Pirahã", "Bird Language"], None))
SECTIONS.append(("chorus", 4, [s[0] for s in SINGERS], HOOK))
SECTIONS.append(("outro", 2, [s[0] for s in SINGERS], None))
total_bars = sum(s[1] for s in SECTIONS)
L = int((total_bars * BAR + 1.5) * SR)
mix = np.zeros((L, 2), np.float32)
PAN = {s[0]: s[2] for s in SINGERS}
CAP = {s[0]: s[1] for s in SINGERS}

def put(x, t, pan=0.0, gain=1.0):
    i = int(t * SR); x = x[: max(0, L - i)]
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    mix[i:i + len(x), 0] += x * gain * l * 1.41; mix[i:i + len(x), 1] += x * gain * r * 1.41

def raw_phrase(singer, t, maxdur, gain=1.0):
    """an untouched stretch of the original recording (no tuning): the 'real thing' moments"""
    d = SEG[singer]; seg = max(d["segs"], key=lambda s: s["end"] - s["start"])
    a = read_wav(os.path.join(HERE, "..", "cache", "audio", d["file"]))
    st = max(0, seg["start"] - 0.2); x = a[int(st * SR): int((st + maxdur) * SR)].copy()
    fade = int(0.05 * SR); x[:fade] *= np.linspace(0, 1, fade); x[-fade:] *= np.linspace(1, 0, fade)
    put(x / (np.sqrt(np.mean(x ** 2)) + 1e-6) * 0.08, t, PAN.get(singer, 0), gain)

timeline, t0, ONSETS = [], 0.0, []
for name, bars, singers, hook in SECTIONS:
    for b in range(bars):
        bt = t0 + b * BAR
        root, chord = CHORDS[(b + (0 if name != "solo" else 0)) % 4] if hook is None else CHORDS[(HOOK.index(hook[b % len(hook)])) % 4]
        full = name in ("chorus", "outro")
        # drums
        for beat in range(4):
            tb = bt + beat * BEAT
            if name == "intro" and b == 0: continue
            if name == "break":
                if beat in (0, 2): put(kick(), tb)
                continue
            if full or beat in (0, 2): put(kick(), tb)
            if beat in (1, 3): put(snare(), tb, 0, 0.9); put(clap(), tb, 0.1) if full else None
            for h in range(2): put(hat(open_=(h == 1 and beat == 3)), tb + h * E8, 0.35)
        # bass + pad
        if not (name == "intro" and b == 0):
            for e in range(8):
                if e in (0, 3, 4, 6) or full: put(bass_note(root - 12 if e % 2 == 0 else root, E8 * 0.9), bt + e * E8)
        if name != "break": put(pad(chord, BAR), bt, 0, 1.4 if full else 0.8)
    # whistles
    if name in ("solo", "chorus"):
        for k, s in enumerate(singers):
            for st8, n8, m in notes_of(hook):
                dur = n8 * E8 - 0.03
                put(whistle_note(s, m, dur, k), t0 + st8 * E8, PAN[s], 1.0 if name == "solo" else 0.45)
                ONSETS.append([round(t0 + st8 * E8, 3), round(dur, 3), s])
        if name == "chorus":   # a third below for half of the group
            for k, s in enumerate(singers[::2]):
                for st8, n8, m in notes_of(hook):
                    put(whistle_note(s, m - 3 if m % 12 in (4, 11) else m - 4, n8 * E8 - 0.03, k + 3), t0 + st8 * E8, PAN[s], 0.25)
    elif name == "intro":
        raw_phrase("Silbo Gomero", t0 + 0.2, 2 * BAR - 0.4)
    elif name == "break":
        raw_phrase("Pirahã", t0, BAR); raw_phrase("Bird Language", t0 + BAR, BAR)
    elif name == "outro":
        for k, s in enumerate(singers):
            put(whistle_note(s, 69, BAR * 1.5, k), t0, PAN[s], 0.4)
    timeline.append({"section": name, "start": round(t0, 3), "end": round(t0 + bars * BAR, 3), "singers": singers,
                     "caption": CAP[singers[0]] if name == "solo" else {"intro": "Silbo Gomero starts it off…", "chorus": "EVERYBODY NOW",
                     "break": "The original recordings, untouched", "outro": "9 languages, 0 words"}[name]})
    t0 += bars * BAR

# master: soft limiter, fade out
peak = np.max(np.abs(mix)); mix = np.tanh(mix / peak * 1.6) / np.tanh(1.6) * 0.89
fo = int(1.2 * SR); mix[-fo:] *= np.linspace(1, 0, fo)[:, None]
with wave.open(os.path.join(OUT, "song.wav"), "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
json.dump({"bpm": BPM, "bar": BAR, "duration": round(L / SR, 2), "sections": timeline, "onsets": ONSETS}, open(os.path.join(OUT, "timeline.json"), "w"), indent=1, ensure_ascii=False)
print(f"song.wav {L / SR:.1f}s, {total_bars} bars")

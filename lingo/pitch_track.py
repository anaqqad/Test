"""Add a pitch trace to every clip of a video, for the on-screen pitch line (videos with pitchLine: true).
   python3 pitch_track.py <key>   -> manifest[<item>]["pitch"] = [[t, 0..1 or null], ...] (100 ms smoothing, log scale per clip)"""
import json, os, re, sys, numpy as np, parselmouth
HERE = os.path.dirname(os.path.abspath(__file__))
key = sys.argv[1]
mp = os.path.join(HERE, "cache", "audio", key, "manifest.json"); man = json.load(open(mp))
slug = lambda n: re.sub(r"^_+|_+$", "", re.sub(r"[^\w]+", "_", n)).lower()
for name, e in man.items():
    if not e: continue
    wav = os.path.join(HERE, "cache", "audio", key, slug(name) + ".wav")
    if not os.path.exists(wav): print("missing", wav); continue
    pt = parselmouth.Sound(wav).to_pitch_ac(time_step=0.02, pitch_floor=70, pitch_ceiling=500)
    f = pt.selected_array["frequency"]; t = pt.xs()
    st = np.where(f > 0, 12 * np.log2(np.maximum(f, 1) / 100), np.nan)
    v = st[~np.isnan(st)]
    if len(v) < 5: continue
    lo, hi = np.percentile(v, 5), np.percentile(v, 95)
    out = [[round(float(a), 2), None if np.isnan(b) else round(float(np.clip((b - lo) / max(hi - lo, 1), 0, 1)), 3)] for a, b in zip(t, st)]
    # drop octave-jump glitches: a point far from both neighbours breaks the line instead of drawing a spike
    for i in range(1, len(out) - 1):
        a, b, c = out[i - 1][1], out[i][1], out[i + 1][1]
        if b is not None and (a is None or abs(b - a) > 0.3) and (c is None or abs(b - c) > 0.3): out[i][1] = None
    e["pitch"] = out
    print(name, len(out), "points")
json.dump(man, open(mp, "w"), indent=1, ensure_ascii=False)

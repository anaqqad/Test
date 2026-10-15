# Cry-melody analysis for the "babies cry with an accent" video: python3 baby_analyze.py
# Reads cache/babies/raw/<country>.wav, finds each cry (voiced stretch), tracks its pitch with Praat and labels the
# melody shape the way Mampe et al. (2009) did: where the pitch peak falls within the cry (early = falling, late = rising).
# Writes cache/babies/analysis.json and cache/babies/contours.png.
import json, os, sys
import numpy as np
import parselmouth

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "cache", "babies")
ORDER = ["france", "germany", "china", "cameroon", "cameroon2", "sweden", "sweden2", "sweden3"]


def cries(path):
    snd = parselmouth.Sound(path)
    # infant cries sit roughly 250-800 Hz; adults talking nearby fall mostly below 300 Hz
    pitch = snd.to_pitch_ac(time_step=0.01, pitch_floor=150, pitch_ceiling=1200, voicing_threshold=0.5)
    t, f = pitch.xs(), pitch.selected_array["frequency"]
    out, start = [], None
    for i, v in enumerate(np.append(f, 0)):
        if v > 0 and start is None:
            start = i
        elif v == 0 and start is not None:
            # bridge gaps shorter than 80 ms (cry breaks, glottal noise)
            if i < len(f) and np.any(f[i:i + 8] > 0):
                continue
            seg_t, seg_f = t[start:i], f[start:i]
            if seg_t[-1] - seg_t[0] >= 0.3:
                voiced = seg_f > 0
                ft, ff = seg_t[voiced], seg_f[voiced]
                peak = (ft[np.argmax(ff)] - ft[0]) / (ft[-1] - ft[0])
                semis = 12 * np.log2(ff.max() / ff.min())
                shape = "rising" if peak > 0.6 else "falling" if peak < 0.4 else "rise-fall"
                # melody complexity: direction changes of the smoothed contour bigger than 2 semitones (Wermke's "arcs")
                st = 12 * np.log2(np.convolve(ff, np.ones(5) / 5, mode="valid") / 100) if len(ff) > 5 else 12 * np.log2(ff / 100)
                arcs, ext, d = 1, st[0], 0
                for v in st[1:]:
                    nd = 1 if v > ext else -1
                    if d == 0 and abs(v - ext) >= 2: d, ext = nd, v
                    elif d and nd == d: ext = v
                    elif d and abs(v - ext) >= 2: arcs, d, ext = arcs + 1, nd, v
                out.append({"start": round(float(ft[0]), 2), "end": round(float(ft[-1]), 2), "median_hz": round(float(np.median(ff))),
                            "range_semitones": round(float(semis), 1), "peak_position": round(float(peak), 2), "shape": shape, "arcs": arcs,
                            "contour": [[round(float(a - ft[0]), 3), round(float(b), 1)] for a, b in zip(ft, ff)]})
            start = None
    low = float(np.mean((f > 0) & (f < 300))) / max(float(np.mean(f > 0)), 1e-9)
    return snd.duration, out, low


res = {}
for k in ORDER:
    p = os.path.join(D, "raw", k + ".wav")
    if not os.path.exists(p):
        continue
    dur, cs, low = cries(p)
    shapes = {s: sum(c["shape"] == s for c in cs) for s in ["rising", "falling", "rise-fall"]}
    res[k] = {"duration": round(dur, 1), "cries": cs, "shapes": shapes, "low_pitch_share": round(low, 2),
              "mean_arcs": round(float(np.mean([c["arcs"] for c in cs])), 2) if cs else None,
              "mean_range_semitones": round(float(np.mean([c["range_semitones"] for c in cs])), 1) if cs else None}
    print(f"{k:9} {dur:5.1f}s  cries {len(cs):2}  {shapes}  mean range {res[k]['mean_range_semitones']} st  "
          f"arcs/cry {res[k]['mean_arcs']}  median f0 {int(np.median([c['median_hz'] for c in cs])) if cs else '-'} Hz  voiced<300Hz {low:.0%}")
    for c in cs:
        print(f"           {c['start']:5.2f}-{c['end']:5.2f}s  {c['shape']:9} peak@{c['peak_position']:.2f}  {c['range_semitones']:4.1f} st  {c['median_hz']} Hz")
json.dump(res, open(os.path.join(D, "analysis.json"), "w"), indent=1)

if "--plot" in sys.argv:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, len(res), figsize=(4 * len(res), 3.2), sharey=True)
    for ax, (k, r) in zip(np.atleast_1d(axes), res.items()):
        for c in r["cries"]:
            x = np.array(c["contour"])
            ax.plot(x[:, 0], x[:, 1], color={"rising": "#1f77b4", "falling": "#d62728", "rise-fall": "#7f7f7f"}[c["shape"]], lw=1.5)
        ax.set_title(f"{k} ({len(r['cries'])} cries)")
        ax.set_xlabel("seconds into cry")
    np.atleast_1d(axes)[0].set_ylabel("pitch (Hz)")
    fig.tight_layout()
    fig.savefig(os.path.join(D, "contours.png"), dpi=110)

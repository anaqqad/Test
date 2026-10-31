"""Find pitched whistle segments in the whistled-language clips -> song/segments.json"""
import json, os, numpy as np, parselmouth
HERE = os.path.dirname(os.path.abspath(__file__))
CL = {"Silbo Gomero": "whistled/silbo_gomero.wav", "Bird Language": "whistled/bird_language.wav", "Sfyria": "whistled/sfyria.wav",
      "Whistled Occitan": "whistled/whistled_occitan.wav", "Whistled Yoruba": "whistled/whistled_yoruba.wav", "Hmong": "whistled2/hmong.wav",
      "Chinantec": "whistled2/chinantec.wav", "Pirahã": "whistled2/pirahã.wav", "Wayãpi": "whistled2/wayãpi.wav"}
out = {}
for name, rel in CL.items():
    p = os.path.join(HERE, "..", "cache", "audio", rel)
    snd = parselmouth.Sound(p)
    pt = snd.to_pitch_ac(time_step=0.01, pitch_floor=400, pitch_ceiling=5000, voicing_threshold=0.5)
    f = pt.selected_array["frequency"]; t = pt.xs()
    segs, cur = [], []
    for i, v in enumerate(f):
        if v > 0 and (not cur or abs(np.log2(v / f[cur[-1]])) < 0.15): cur.append(i)
        else:
            if len(cur) >= 12: segs.append(cur)
            cur = [i] if v > 0 else []
    if len(cur) >= 12: segs.append(cur)
    segs = [{"start": round(float(t[s[0]]), 3), "end": round(float(t[s[-1]]), 3), "f0": round(float(np.median(f[s])), 1),
             "spread": round(float(np.std(np.log2(f[s]))), 3)} for s in segs]
    out[name] = {"file": rel, "segs": segs}
    print(f"{name:18s} {len(segs):3d} segs  f0 {[s['f0'] for s in segs][:8]}  durs {[round(s['end']-s['start'],2) for s in segs][:8]}")
json.dump(out, open(os.path.join(HERE, "segments.json"), "w"), indent=1, ensure_ascii=False)

# Audio for "Ranking the World's Most Vulgar Languages": python3 fetch_vulgar.py
# One Lingua Libre recording per language (vulgar.json "rec"), trimmed and loudness-matched, with the speaker's pitch
# (to pick a Wojak of the right gender). Writes cache/audio/vulgar/<key>.wav, manifest.json and out/vulgar_credits.txt.
import json, os
import numpy as np, parselmouth
import fetch_audio as fa
import fetch_pairs as fp

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "vulgar.json")))
OUT = os.path.join(HERE, "cache", "audio", "vulgar")
os.makedirs(OUT, exist_ok=True)
man, credits = {}, []
for it in D["items"]:
    if not it.get("rec"):
        man[it["key"]] = None; print(it["key"], "no recording"); continue
    dst = os.path.join(OUT, it["key"] + ".wav")
    m = fp.clip(it["rec"], dst)
    if not m:
        man[it["key"]] = None; print(it["key"], "download failed"); continue
    p = parselmouth.Sound(dst).to_pitch(pitch_floor=60, pitch_ceiling=400).selected_array["frequency"]; p = p[p > 0]
    f0 = int(np.median(p)) if len(p) else 0
    man[it["key"]] = {"d": round(fa.duration(dst), 2), "f0": f0, "voice": "female" if f0 > 165 else "male", "credit": m}
    credits.append(f"{it['name']}: \"{m['title'][5:]}\" by {m['artist']}, {m['license']}, via Wikimedia Commons, {m['page']}")
    print(it["key"], man[it["key"]]["d"], "s, F0", f0, man[it["key"]]["voice"], flush=True)
json.dump(man, open(os.path.join(OUT, "manifest.json"), "w"), indent=1, ensure_ascii=False)
open(os.path.join(HERE, "out", "vulgar_credits.txt"), "w").write("Audio credits (Ranking the World's Most Vulgar Languages)\n\n" + "\n".join(credits) + "\n")

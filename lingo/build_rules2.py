# Audio for "These Languages Break the Rules of Speech, Part 2": python3 build_rules2.py
# Recordings (Wiktionary pronunciation files and Lingua Libre, downloaded as Commons mp3 transcodes into cache/sounds2,
# credits in cache/sounds2/meta.json) are trimmed, peak-normalised and joined with short gaps, one wav per language.
# Writes cache/audio/rules2/<key>.wav, manifest.json (durations, voice pitch, credits) and out/rules2_credits.txt.
import json, os, re, subprocess, urllib.parse
import numpy as np, parselmouth
import fetch_audio as fa

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "rules2.json")))
SRC = os.path.join(HERE, "cache", "sounds2")
META = json.load(open(os.path.join(SRC, "meta.json")))
OUT = os.path.join(HERE, "cache", "audio", "rules2")
os.makedirs(OUT, exist_ok=True)
GAP = 0.7
man, credits = {}, []
for it in D["items"]:
    k = it["key"]; parts = []
    for r in it["recs"]:
        src = os.path.join(SRC, r + ".mp3")
        if not os.path.exists(src) or fa.duration(src) < 0.05:
            print(k, "missing", r); continue
        w = os.path.join(OUT, f"{k}_{r}.wav")
        fa.to_wav(src, w, extra="silenceremove=start_periods=1:start_threshold=-42dB,areverse,silenceremove=start_periods=1:start_threshold=-42dB,areverse")
        v = subprocess.run(["ffmpeg", "-i", w, "-af", "volumedetect", "-f", "null", "-"], capture_output=True, text=True)
        peak = float(re.search(r"max_volume: (-?[\d.]+) dB", v.stderr).group(1))
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", w, "-af", f"volume={-1.5 - peak:.1f}dB,acompressor=threshold=-16dB:ratio=2.5:attack=5:release=80:makeup=1", w + ".p.wav"], check=True)
        os.replace(w + ".p.wav", w); parts.append((r, w, fa.duration(w)))
    if not parts:
        man[k] = None; continue
    ins, filt, t, seq = [], [], 0.0, []
    for i, (r, w, d) in enumerate(parts):
        ins += ["-i", w]; filt.append(f"[{i}]adelay={int(t * 1000)}|{int(t * 1000)}[a{i}]"); seq.append({"rec": r, "t": round(t, 2), "d": round(d, 2)}); t += d + GAP
    total = t - GAP + 0.3
    filt.append("".join(f"[a{i}]" for i in range(len(parts))) + f"amix=inputs={len(parts)}:normalize=0,apad,atrim=0:{total:.2f}[o]")
    dst = os.path.join(OUT, k + ".wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(filt), "-map", "[o]", "-ar", str(fa.SR), dst], check=True)
    p = parselmouth.Sound(dst).to_pitch(pitch_floor=60, pitch_ceiling=400).selected_array["frequency"]; p = p[p > 0]
    f0 = int(np.median(p)) if len(p) else 0
    man[k] = {"len": round(total, 2), "seq": seq, "f0": f0, "voice": "female" if f0 > 170 else "male"}
    for r, _, _ in parts:
        m = META[r]; lic = (m["license"] or ["licence: see file page"])[0]; auth = m["author"] or "uploader on Wikimedia Commons"
        credits.append(f"{it['name']}: \"{m['title'][5:]}\" by {auth}, {lic}, via Wikimedia Commons, https://commons.wikimedia.org/wiki/{urllib.parse.quote(m['title'].replace(' ', '_'))}")
    print(k, man[k]["len"], "s", man[k]["voice"], [s["rec"] for s in seq])
json.dump(man, open(os.path.join(OUT, "manifest.json"), "w"), indent=1, ensure_ascii=False)
open(os.path.join(HERE, "out", "rules2_credits.txt"), "w").write("Audio credits (These Languages Break the Rules of Speech, Part 2)\n\n" + "\n".join(credits) + "\n")

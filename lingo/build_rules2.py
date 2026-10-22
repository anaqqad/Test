# Audio for "These Languages Break the Rules of Speech, Part 2": python3 build_rules2.py
# Each language gets a real speech sample: Wikitongues videos from Wikimedia Commons (cache/rules2n/src/<file>.webm, the
# 240p transcodes) cut from `start` for `len` seconds, loudness-matched with a fade; optionally a word recording first
# (`recs`, mp3 transcodes in cache/rules2n/src). Writes cache/audio/rules2/<key>.wav, manifest.json (durations, voice
# pitch, credits) and out/rules2_credits.txt.
import json, os, re, subprocess, urllib.parse
import numpy as np, parselmouth
import fetch_audio as fa

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "rules2.json")))
SRC = os.path.join(HERE, "cache", "rules2n", "src")
OUT = os.path.join(HERE, "cache", "audio", "rules2")
os.makedirs(OUT, exist_ok=True)
GAP = 0.7
# file key -> (Commons title, author, licence)
CREDITS = {
    "greenlandic": ("WIKITONGUES- Mark speaking Greenlandic.webm", "Wikitongues", "CC BY 3.0"),
    "georgian": ("WIKITONGUES- Mariam speaking Georgian.webm", "Wikitongues", "CC BY 3.0"),
    "kat_word": ("Ka-გვფრცქვნი-Nicodene-mom.ogg", "Nicodene", "CC BY-SA 4.0"),
    "hmong": ("May speaking Hmong Don.webm", "Wikitongues", "CC BY-SA 4.0"),
    "quechua": ("WIKITONGUES- Casiano speaking Quechua.webm", "Wikitongues", "CC BY-SA 4.0"),
    "lakota": ("WIKITONGUES- Junior speaking Lakota.webm", "Wikitongues", "CC BY 3.0"),
    "cherokee": ("WIKITONGUES- Hassan speaking Cherokee.webm", "Wikitongues", "CC BY-SA 4.0"),
    "nahuatl": ("WIKITONGUES- Yan speaking Huasteca Nahuatl.webm", "Wikitongues", "CC BY 3.0"),
    "basque": ("WIKITONGUES- Jon speaking Basque.webm", "Wikitongues", "CC BY 3.0"),
}
man, credits = {}, []
for it in D["items"]:
    k = it["key"]; parts = []
    for r in it.get("recs", []):
        src = os.path.join(SRC, r + ".mp3")
        if not os.path.exists(src) or os.path.getsize(src) < 2000 or fa.duration(src) < 0.05:
            print(k, "missing", r); continue
        w = os.path.join(OUT, f"{k}_{r}.wav")
        fa.to_wav(src, w, extra="silenceremove=start_periods=1:start_threshold=-42dB,areverse,silenceremove=start_periods=1:start_threshold=-42dB,areverse")
        v = subprocess.run(["ffmpeg", "-i", w, "-af", "volumedetect", "-f", "null", "-"], capture_output=True, text=True)
        peak = float(re.search(r"max_volume: (-?[\d.]+) dB", v.stderr).group(1))
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", w, "-af", f"volume={-1.5 - peak:.1f}dB,acompressor=threshold=-16dB:ratio=2.5:attack=5:release=80:makeup=1", w + ".p.wav"], check=True)
        os.replace(w + ".p.wav", w); parts.append((r, w, fa.duration(w)))
    c = it.get("clip")
    if c:
        src = os.path.join(SRC, c["file"] + ".webm")
        if not os.path.exists(src) or os.path.getsize(src) < 20000:
            print(k, "missing clip", c["file"])
        else:
            w = os.path.join(OUT, f"{k}_clip.wav"); L = c["len"]
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(c["start"]), "-t", str(L + 1), "-i", src, "-vn", "-af",
                            f"aresample={fa.SR},pan=mono|c0=c0,loudnorm=I=-17:TP=-2,apad,atrim=0:{L},afade=t=in:d=0.15,afade=t=out:st={L - 0.8}:d=0.8", "-ar", str(fa.SR), w], check=True)
            parts.append((c["file"], w, L))
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
        title, auth, lic = CREDITS[r]
        credits.append(f"{it['name']}: \"{title}\" by {auth}, {lic}, via Wikimedia Commons, https://commons.wikimedia.org/wiki/{urllib.parse.quote('File:' + title.replace(' ', '_'))}")
    print(k, man[k]["len"], "s", man[k]["voice"], f0, [s["rec"] for s in seq])
json.dump(man, open(os.path.join(OUT, "manifest.json"), "w"), indent=1, ensure_ascii=False)
open(os.path.join(HERE, "out", "rules2_credits.txt"), "w").write("Audio credits (These Languages Break the Rules of Speech, Part 2)\n\n" + "\n".join(credits) + "\n")

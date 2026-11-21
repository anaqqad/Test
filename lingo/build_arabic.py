# Audio for "Languages Arabic Speakers Can Almost Understand": python3 build_arabic.py
# Real recordings from Wikimedia Commons (Wikitongues interviews, a CC0 Aramaic recitation, Lingua Libre Maltese words).
# Writes cache/audio/arabic_understand/<slug>.wav, manifest.json and out/arabic_understand_credits.txt.
import json, os, subprocess, urllib.parse
import numpy as np
import fetch_audio as fa

HERE = os.path.dirname(os.path.abspath(__file__))
KEY = "arabic_understand"
OUT = os.path.join(HERE, "cache", "audio", KEY)
os.makedirs(OUT, exist_ok=True)
CLIPS = {  # name: (Commons file, start, end)
    "Hausa": ("WIKITONGUES- Abubakar speaking Hausa.webm", 71.1, 79.0),
    "Swahili": ("WIKITONGUES- Iddy speaking Swahili.webm", 28.4, 41.2),
    "Turkish": ("WIKITONGUES- Ela speaking Turkish.webm", 1.6, 11.6),
    "Persian": ("WIKITONGUES- Daniel speaking Farsi.webm", 19.6, 31.6),
    "Urdu": ("WIKITONGUES- Scarlett speaking Urdu.webm", 17.9, 27.4),
    "Hebrew": ("WIKITONGUES- Amir speaking Russian and Hebrew.webm", 89.0, 103.0),
    "Aramaic": ("Abundbshmayo.ogg", 0.0, 17.0),
}
MALTESE = ["aħna", "ktieb", "gżira", "belt", "ħobża", "aħmar", "mill-ġdid", "llejla"]  # Lingua Libre, speaker GħawdxiVeru
manifest, lines = {}, ["Audio credits (Languages Arabic Speakers Can Almost Understand)", ""]

def credit(name, meta):
    manifest.setdefault(name, {"sig": f"{KEY}|{name}", "credits": [], "captions": [], "start": 0})
    manifest[name]["credits"].append({"title": meta["title"], "artist": meta["artist"], "license": meta["license"], "page": meta["page"]})

# credits as listed on each Commons file page (kept here so a rebuild doesn't need the rate-limited API)
KNOWN = {"Hausa": ("Wikitongues, Inc.", "CC BY-SA 4.0"), "Swahili": ("Bogreudell", "CC BY-SA 4.0"), "Turkish": ("Wikitongues", "CC BY 3.0"),
         "Persian": ("Wikitongues, Tushar Rakheja", "CC BY-SA 4.0"), "Urdu": ("Wikitongues", "CC BY 3.0"),
         "Hebrew": ("Bogreudell", "CC BY-SA 4.0"), "Aramaic": ("PaddyMacConghaile", "CC0")}
import glob
for name, (f, s, e) in CLIPS.items():
    stem = f.replace(" ", "_")[:40]
    src = ([x for x in glob.glob(os.path.join(HERE, "cache", "raw", "*")) if os.path.basename(x).startswith(stem)] or [None])[0]
    meta = {"title": "File:" + f, "artist": KNOWN[name][0], "license": KNOWN[name][1],
            "page": "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(("File:" + f).replace(" ", "_"))}
    if src is None:
        src = fa.download(fa.info(f))
    need = round(e - s, 2)
    fa.to_wav(src, os.path.join(OUT, fa.slug(name) + ".wav"), s, need, extra=f"afade=t=in:d=0.15,afade=t=out:st={need - 0.4}:d=0.4,loudnorm=I=-18:TP=-2")
    credit(name, meta); manifest[name]["start"] = s
    lines.append(f'{name}: "{f}" by {meta["artist"]}, {meta["license"]}, via Wikimedia Commons, {meta["page"]}')
    print(name, need, "s from", s)

# Maltese: the words in a row with short gaps
parts, SR = [], 48000
for w in MALTESE:
    t = f"LL-Q9166 (mlt)-GħawdxiVeru-{w}.wav"; src = os.path.join(HERE, "incoming", "arabic", t)   # fetched via browser (Commons API rate limit)
    meta = {"title": "File:" + t, "artist": "GħawdxiVeru (Lingua Libre)", "license": "CC0",
            "page": "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(("File:" + t).replace(" ", "_"))}
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-ac", "1", "-ar", str(SR), "-af", "silenceremove=start_periods=1:start_threshold=-40dB,areverse,silenceremove=start_periods=1:start_threshold=-40dB,areverse", "-f", "f32le", "-"], capture_output=True, check=True).stdout
    parts += [np.frombuffer(raw, np.float32), np.zeros(int(SR * 0.55), np.float32)]
    credit("Maltese", meta)
seq = np.concatenate(parts)
tmp = os.path.join(OUT, "maltese_raw.f32"); seq.tofile(tmp)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", tmp, "-af", "aresample=48000,pan=stereo|c0=c0|c1=c0,loudnorm=I=-18:TP=-2", "-ar", "48000", os.path.join(OUT, "maltese.wav")], check=True)
os.remove(tmp)
lines.append("Maltese: Lingua Libre recordings by GħawdxiVeru (" + ", ".join(MALTESE) + "), CC BY-SA 4.0, via Wikimedia Commons")
print("Maltese", round(len(seq) / SR, 2), "s,", len(MALTESE), "words")
json.dump(manifest, open(os.path.join(OUT, "manifest.json"), "w"), indent=1, ensure_ascii=False)
open(os.path.join(HERE, "out", f"{KEY}_credits.txt"), "w").write("\n".join(lines) + "\n")

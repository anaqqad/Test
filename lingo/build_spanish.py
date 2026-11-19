# Audio for "Languages Spanish Speakers Can Almost Understand": python3 build_arabic.py
# Real recordings from Wikimedia Commons (Wikitongues interviews and a CC0 Galician radio interview).
# Writes cache/audio/spanish_understand/<slug>.wav, manifest.json and out/spanish_understand_credits.txt.
import json, os, subprocess, urllib.parse
import numpy as np
import fetch_audio as fa

HERE = os.path.dirname(os.path.abspath(__file__))
KEY = "spanish_understand"
OUT = os.path.join(HERE, "cache", "audio", KEY)
os.makedirs(OUT, exist_ok=True)
CLIPS = {  # name: (Commons file, start, end)
    "Romanian": ("WIKITONGUES- Raluca speaking Romanian.webm", 3.3, 21.0),
    "Sardinian": ("WIKITONGUES- Ricardo speaking Sardinian.webm", 32.0, 44.0),
    "Catalan": ("WIKITONGUES- Ona speaking Catalan.webm", 0.2, 15.2),
    "Italian": ("WIKITONGUES- Paola speaking Italian and Sicilian.webm", 8.0, 19.0),
    "Portuguese": ("WIKITONGUES- Sara speaking Portuguese.webm", 1.3, 13.8),
    "Galician": ("Galegos no baix -Ràdio Sant Boi -Amador Arias (29-05-2019).ogg", 0.0, 19.6),
    "Extremaduran": ("WIKITONGUES- Daniel speaking Extremaduran.webm", 10.7, 26.8),
    "Asturian": ("WIKITONGUES- Victor speaking Asturian.webm", 0.6, 9.2),
}
manifest, lines = {}, ["Audio credits (Languages Spanish Speakers Can Almost Understand)", ""]

def credit(name, meta):
    manifest.setdefault(name, {"sig": f"{KEY}|{name}", "credits": [], "captions": [], "start": 0})
    manifest[name]["credits"].append({"title": meta["title"], "artist": meta["artist"], "license": meta["license"], "page": meta["page"]})

# credits as listed on each Commons file page (kept here so a rebuild doesn't need the rate-limited API)
KNOWN = {"Romanian": ("Wikitongues, Nick Panzarella", "CC BY-SA 4.0"), "Sardinian": ("Wikitongues, Ricardo Germán", "CC BY-SA 4.0"),
         "Catalan": ("Wikitongues", "CC BY 3.0"), "Italian": ("Wikitongues, David Paleino", "CC BY-SA 4.0"),
         "Portuguese": ("Wikitongues, Guillem Belmar", "CC BY-SA 4.0"), "Galician": ("Ràdio Cornellà", "CC0"),
         "Extremaduran": ("Wikitongues, Guillem Belmar", "CC BY-SA 4.0"), "Asturian": ("Wikitongues, Daniel Bögre Udell", "CC BY-SA 4.0")}
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

json.dump(manifest, open(os.path.join(OUT, "manifest.json"), "w"), indent=1, ensure_ascii=False)
open(os.path.join(HERE, "out", f"{KEY}_credits.txt"), "w").write("\n".join(lines) + "\n")

# Audio for "Languages Italian Speakers Can Almost Understand": python3 build_italian.py
# New real recordings from Wikimedia Commons (Wikitongues and volunteers), downloaded into incoming/italian/ and kept as
# audio only (<name>.audio.ogg). Meanings: Commons subtitles (Neapolitan, Lombard: English; Sardinian: Italian, translated
# by us), Whisper transcript and translation checked by us (French). Sicilian, Friulian and Romansh have no translation:
# their cards give facts instead of a transcript.
# Mixed-in clips reused from the earlier videos (already cut and loudness-matched in cache/audio/<key>/):
# Spanish, Portuguese (portuguese_understand / spanish_understand), Catalan, Romanian, Occitan (french_understand).
# Writes cache/audio/italian_understand/<slug>.wav, manifest.json and out/italian_understand_credits.txt.
import json, os, shutil, subprocess, urllib.parse
import fetch_audio as fa

HERE = os.path.dirname(os.path.abspath(__file__))
KEY = "italian_understand"
SRC = os.path.join(HERE, "incoming", "italian")
OUT = os.path.join(HERE, "cache", "audio", KEY)
os.makedirs(OUT, exist_ok=True)
NEW = {  # name: (Commons file, [(start, end), ...])
    "Neapolitan": ("WIKITONGUES- Foffo speaking Neapolitan.webm", [(0.0, 25.0)]),
    "Sicilian": ("WIKITONGUES- Steven speaking Sicilian.webm", [(0.0, 25.0)]),
    "Lombard": ("WIKITONGUES- Pietro speaking Lombard.webm", [(2.3, 28.7)]),  # "Hello everyone ... Lombard"
    "Sardinian": ("WIKITONGUES- Ricardo speaking Sardinian.webm", [(0.0, 25.0)]),
    "Friulian": ("Wikitongues-Friulian-Moroldo.webm", [(0.0, 25.0)]),
    "French": ("WIKITONGUES- Clara speaking French.webm", [(0.0, 26.0)]),
    "Romansh": ("Romansh (Wikitongues).ogg", [(0.0, 25.0)]),
}
REUSED = {  # name: (cached wav, source manifest, key in that manifest)
    "Spanish": ("portuguese_understand", "Spanish"),
    "Catalan": ("spanish_understand", "Catalan"),
    "Portuguese": ("spanish_understand", "Portuguese"),
    "Romanian": ("spanish_understand", "Romanian"),
    "Occitan": ("french_understand", "Occitan"),
}
META = json.load(open(os.path.join(SRC, "meta.json")))
manifest, lines = {}, ["Audio credits (Languages Italian Speakers Can Almost Understand)", ""]
page_of = lambda f: "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(("File:" + f).replace(" ", "_"))
for name, (f, parts) in NEW.items():
    m = META[f]; page = page_of(f)
    src = os.path.join(SRC, f.rsplit(".", 1)[0] + ".audio.ogg"); dst = os.path.join(OUT, fa.slug(name) + ".wav")
    tmp = []
    for i, (s, e) in enumerate(parts):
        t = dst + f".part{i}.wav"; fa.to_wav(src, t, s, round(e - s, 2)); tmp.append(t)
    if len(tmp) == 1:
        os.replace(tmp[0], dst + ".raw.wav")
    else:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp[0], "-i", tmp[1], "-filter_complex", "acrossfade=d=0.25", dst + ".raw.wav"], check=True)
        [os.remove(t) for t in tmp]
    need = round(sum(e - s for s, e in parts) - 0.25 * (len(parts) - 1), 2)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", dst + ".raw.wav", "-af",
                    f"afade=t=in:d=0.15,afade=t=out:st={need - 0.4}:d=0.4,loudnorm=I=-18:TP=-2", "-ar", str(fa.SR), dst], check=True)
    os.remove(dst + ".raw.wav")
    artist = m["artist"].strip('"')
    manifest[name] = {"sig": f"{KEY}|{name}", "start": parts[0][0], "parts": parts, "captions": [],
                      "credits": [{"title": "File:" + f, "artist": artist, "license": m["license"], "page": page}]}
    lines.append(f'{name}: "{f.rsplit(".", 1)[0]}" by {artist}, {m["license"]}, via Wikimedia Commons, {page}')
    print(name, need, "s ->", fa.slug(name))
for name, (k, src_key) in REUSED.items():
    src_m = json.load(open(os.path.join(HERE, "cache", "audio", k, "manifest.json")))[src_key]
    shutil.copy(os.path.join(HERE, "cache", "audio", k, fa.slug(src_key) + ".wav"), os.path.join(OUT, fa.slug(name) + ".wav"))
    manifest[name] = {"sig": f"{KEY}|{name}", "start": src_m.get("start", 0), "parts": src_m.get("parts"), "captions": [],
                      "credits": src_m["credits"]}
    c = src_m["credits"][0]
    lines.append(f'{name}: "{c["title"][5:].rsplit(".", 1)[0]}" by {c["artist"]}, {c["license"]}, via Wikimedia Commons, {c["page"]}')
    print(name, "reused from", k)
json.dump(manifest, open(os.path.join(OUT, "manifest.json"), "w"), indent=1, ensure_ascii=False)
open(os.path.join(HERE, "out", f"{KEY}_credits.txt"), "w").write("\n".join(lines) + "\n")

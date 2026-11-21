# Audio for "Hear These Languages Before They Disappear, Part 2": python3 build_extinct2.py
# Wikitongues videos from Wikimedia Commons (cache/extinct2/src, the 240p transcodes; the originals are throttled).
# Each language gets the speech from START for the length of its segment, loudness-matched, with a fade.
# Writes cache/audio/extinct2/<slug>.wav, manifest.json (credits) and out/extinct2_credits.txt.
import json, os, re, subprocess, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "cache", "extinct2", "src")
OUT = os.path.join(HERE, "cache", "audio", "extinct2")
os.makedirs(OUT, exist_ok=True)
slug = lambda s: re.sub(r"[^\w]+", "_", s, flags=re.U).strip("_").lower()
ITEMS = {
 "Ainu": ("ainu", 2.0, 3, "WIKITONGUES- Teruyo speaking Ainu.webm", "Wikitongues", "CC BY 3.0"),
 "Miyako": ("miyako", 2.0, 3, "WIKITONGUES- Hiroyuki speaking Miyako.webm", "Wikitongues", "CC BY-SA 4.0"),
 "Mendriq": ("mendriq", 1.0, 3, "Ida Mendriq (subtitled).webm", "Ultron90", "CC BY-SA 4.0"),
 "Lehali": ("lehali", 2.0, 3, "WIKITONGUES- Anna speaking Tehali.webm", "Wikitongues", "CC BY-SA 4.0"),
 "Kensiu": ("kensiu", 1.0, 3, "Iskandar cakap Kensiu.webm", "Farouk Azim", "CC BY-SA 4.0"),
 "Laz": ("laz", 2.0, 3, "WIKITONGUES- Soner speaking Laz.webm", "Wikitongues", "CC BY 3.0"),
 "Northern Sami": ("sami", 2.0, 3, "WIKITONGUES- Irena speaking Northern Sami.webm", "Wikitongues", "CC BY 3.0"),
 "Bildts": ("bildts", 2.0, 3, "WIKITONGUES- Gerard speaking Bildts.webm", "Wikitongues", "CC BY-SA 4.0"),
}
manifest, lines = {}, ["Audio credits (Hear These Languages Before They Disappear, Part 2)", ""]
for name, (k, start, ncards, title, artist, lic) in ITEMS.items():
    need = round(1.4 + 5.0 * ncards + 1.2, 2)
    dst = os.path.join(OUT, slug(name) + ".wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(start), "-t", str(need + 1), "-i", os.path.join(SRC, k + ".webm"), "-vn", "-af",
                    f"aresample=48000,pan=stereo|c0=c0|c1=c0,loudnorm=I=-17:TP=-2,apad,atrim=0:{need},afade=t=out:st={need - 0.8}:d=0.8", "-ar", "48000", dst], check=True)
    page = "https://commons.wikimedia.org/wiki/" + urllib.parse.quote("File:" + title.replace(" ", "_"))
    manifest[name] = {"sig": "extinct2|" + name, "credits": [{"title": "File:" + title, "artist": artist, "license": lic, "page": page}], "captions": [], "start": start}
    lines.append(f'{name}: "{title}" by {artist}, {lic}, via Wikimedia Commons, {page}')
    print(name, need, "s from", start)
json.dump(manifest, open(os.path.join(OUT, "manifest.json"), "w"), indent=1, ensure_ascii=False)
open(os.path.join(HERE, "out", "extinct2_credits.txt"), "w").write("\n".join(lines) + "\n")

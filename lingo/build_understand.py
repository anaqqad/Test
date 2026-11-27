# Audio for "Languages English Speakers Can Almost Understand (Part 1)": python3 build_understand.py
# Sources: Wikitongues videos on Wikimedia Commons (audio kept in incoming/understand). Each clip runs from start to end.
# and loudness-matched.
# Writes cache/audio/isolates/<slug>.wav, manifest.json and out/isolates_credits.txt.
import json, os, subprocess, urllib.parse
import fetch_audio as fa

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "incoming", "understand")
OUT = os.path.join(HERE, "cache", "audio", "understand")
os.makedirs(OUT, exist_ok=True)
W = "WIKITONGUES- {}.wav"
CLIPS = {  # name: (source file, start, end, Commons title, author, licence)
    "Guyanese Creole": (W.format("Sandra speaking English and Guyanese Creole"), 17.0, 25.9, "WIKITONGUES- Sandra speaking English and Guyanese Creole.webm"),
    "Afro-Seminole Creole": (W.format("Bertha speaking Seminole Creole"), 67.3, 80.2, "WIKITONGUES- Bertha speaking Seminole Creole.webm"),
    "Doric Scots": (W.format("David speaking Doric Scots and English"), 59.6, 69.1, "WIKITONGUES- David speaking Doric Scots and English.webm"),
    "Tok Pisin": (W.format("Priscilla speaking Tok Pisin"), 0.0, 12.4, "WIKITONGUES- Priscilla speaking Tok Pisin.webm"),
    "West Frisian": (W.format("Sjoukje speaking West Frisian"), 0.0, 9.3, "WIKITONGUES- Sjoukje speaking West Frisian.webm"),
}
CRED = json.load(open(os.path.join(HERE, "understand_credits.json")))
YOUTUBE = {}
page = lambda t: "https://commons.wikimedia.org/wiki/" + urllib.parse.quote("File:" + t.replace(" ", "_"))
manifest, lines = {}, ["Audio credits (Languages English Speakers Can Almost Understand, Part 1)", ""]
for name, (f, start, end, title) in CLIPS.items():
    author, lic = CRED[title]
    NEED = round(end - start, 2)
    src = os.path.join(SRC, f)
    if not os.path.exists(src):
        print(name, "missing", f); manifest[name] = None; continue
    dst = os.path.join(OUT, fa.slug(name) + ".wav")
    fa.to_wav(src, dst, start, NEED, extra=f"afade=t=in:d=0.15,afade=t=out:st={NEED - 0.4}:d=0.4,loudnorm=I=-18:TP=-2")
    yt = YOUTUBE.get(name)
    link = yt or page(title)
    manifest[name] = {"sig": "understand|" + name, "credits": [{"title": title if yt else "File:" + title, "artist": author, "license": lic, "page": link}], "captions": [], "start": start}
    lines.append(f'{name}: "{title}" by {author}, {lic} (Creative Commons Attribution), {"YouTube" if yt else "via Wikimedia Commons"}, {link}')
    print(name, NEED, "s from", start)
json.dump(manifest, open(os.path.join(OUT, "manifest.json"), "w"), indent=1, ensure_ascii=False)
open(os.path.join(HERE, "out", "understand_credits.txt"), "w").write("\n".join(lines) + "\n")

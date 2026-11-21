# Audio for "What English Sounded Like in the 1800s": python3 build_oldvoices.py
# Sources: Wikimedia Commons recordings kept in incoming/oldvoices. Each clip runs from start to end, faded and loudness-matched.
# Writes cache/audio/oldvoices/<slug>.wav, manifest.json and out/oldvoices_credits.txt.
import json, os, urllib.parse
import fetch_audio as fa

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "incoming", "oldvoices")
OUT = os.path.join(HERE, "cache", "audio", "oldvoices")
os.makedirs(OUT, exist_ok=True)
CLIPS = {  # name: (Commons file, start, end, author, licence); wax cylinders 1888-1890, all public domain
    "Alfred Tennyson": ("LightBrigade-Tennyson.ogg", 0.0, 10.4, "Alfred Tennyson", "Public domain"),
    "P. T. Barnum": ("PT Barnum Phonograph.wav", 20.2, 41.9, "P. T. Barnum", "Public domain"),
    "Robert Browning": ('Robert Browning recites "How They Brought The Good News From Ghent To Aix".ogg', 0.0, 35.0, "Robert Browning", "Public domain"),
    "Walt Whitman": ("Walt Whitman - America.ogg", 0.0, 36.3, "Walt Whitman", "Public domain"),
    "Florence Nightingale": ("Florence Nightingale voice - 1576A 2nd Rendition.ogg", 13.8, 35.4, "Florence Nightingale", "Public domain"),
    "Benjamin Harrison": ("Benjamin Harrison Voice (1889).ogg", 0.0, 28.0, "Benjamin Harrison", "Public domain"),
    "Arthur Sullivan": ("Arthur Sullivan - wax cylinder recording.ogg", 38.7, 67.3, "Arthur Sullivan (speech), George Gouraud (recording)", "Public domain"),
}
page = lambda t: "https://commons.wikimedia.org/wiki/" + urllib.parse.quote("File:" + t.replace(" ", "_"))
PRE = {}
manifest, lines = {}, ["Audio credits (What English Sounded Like in the 1800s)", ""]
for name, (f, start, end, author, lic) in CLIPS.items():
    need = round(end - start, 2)
    dst = os.path.join(OUT, fa.slug(name) + ".wav")
    fa.to_wav(os.path.join(SRC, f), dst, start, need, extra=PRE.get(name, "") + f"afade=t=in:d=0.15,afade=t=out:st={need - 0.4}:d=0.4,loudnorm=I=-18:TP=-2")
    manifest[name] = {"sig": "oldvoices|" + name, "credits": [{"title": "File:" + f, "artist": author, "license": lic, "page": page(f)}], "captions": [], "start": start}
    lines.append(f'{name}: "{f}" by {author}, {lic}, via Wikimedia Commons, {page(f)}')
    print(name, need, "s from", start)
json.dump(manifest, open(os.path.join(OUT, "manifest.json"), "w"), indent=1, ensure_ascii=False)
open(os.path.join(HERE, "out", "oldvoices_credits.txt"), "w").write("\n".join(lines) + "\n")

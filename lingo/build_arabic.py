# Audio for "Why Arabs Can't Understand Each Other": python3 build_arabic.py
# Sources: Wikimedia Commons recordings kept in incoming/arabic. Each clip runs from start to end, faded and loudness-matched.
# Writes cache/audio/arabic/<slug>.wav, manifest.json and out/arabic_credits.txt.
import json, os, urllib.parse
import fetch_audio as fa

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "incoming", "arabic")
OUT = os.path.join(HERE, "cache", "audio", "arabic")
os.makedirs(OUT, exist_ok=True)
CLIPS = {  # name: (Commons file, start, end, author, licence); videos were converted to .wav (same name)
    "Egyptian Arabic": ("Anonymous 20200622 arz.ogg", 0.0, 6.0, "Wikitongues", "CC BY-SA 4.0"),
    "Syrian Arabic": ("WIKITONGUES- David speaking Syrian Arabic.webm", 0.0, 8.7, "Wikitongues, Tujar Rakheja", "CC BY-SA 4.0"),
    "Iraqi Arabic": ("WIKITONGUES- Mahmoud speaking Iraqi Arabic.webm", 0.0, 11.7, "Bogreudell", "CC BY-SA 4.0"),
    "Tunisian Arabic": ("WIKITONGUES- Mounir speaking Tunisian Arabic.webm", 8.6, 17.9, "Wikitongues", "CC BY 3.0"),
    "Algerian Arabic": ("WIKITONGUEs- Fayçal speaking Algerian Arabic.webm", 0.0, 10.1, "Wikitongues, Anass Sedrati", "CC BY-SA 4.0"),
    "Moroccan Darija": ("WIKITONGUES- Nawal speaking Moroccan Arabic.webm", 0.0, 16.1, "Wikitongues, Kristen Tcherneshoff", "CC BY-SA 4.0"),
    "Standard Arabic": ("Internet In Algeria Arabic Wikipedia spoken article.ogg", 68.5, 79.2, "Riadismet at Arabic Wikipedia", "Public domain"),
}
page = lambda t: "https://commons.wikimedia.org/wiki/" + urllib.parse.quote("File:" + t.replace(" ", "_"))
PRE = {}
manifest, lines = {}, ["Audio credits (Why Arabs Can't Understand Each Other)", ""]
for name, (f, start, end, author, lic) in CLIPS.items():
    need = round(end - start, 2)
    dst = os.path.join(OUT, fa.slug(name) + ".wav")
    fa.to_wav(os.path.join(SRC, f.replace(".webm", ".wav")), dst, start, need, extra=PRE.get(name, "") + f"afade=t=in:d=0.15,afade=t=out:st={need - 0.4}:d=0.4,loudnorm=I=-18:TP=-2")
    manifest[name] = {"sig": "arabic|" + name, "credits": [{"title": "File:" + f, "artist": author, "license": lic, "page": page(f)}], "captions": [], "start": start}
    lines.append(f'{name}: "{f}" by {author}, {lic}, via Wikimedia Commons, {page(f)}')
    print(name, need, "s from", start)
json.dump(manifest, open(os.path.join(OUT, "manifest.json"), "w"), indent=1, ensure_ascii=False)
open(os.path.join(HERE, "out", "arabic_credits.txt"), "w").write("\n".join(lines) + "\n")

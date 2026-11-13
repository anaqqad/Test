# Audio for "Languages English Speakers Can Almost Understand, Part 2": python3 build_understand2.py
# Sources: Wikimedia Commons recordings kept in incoming/understand2. Each clip runs from start to end, faded and loudness-matched.
# Writes cache/audio/understand2/<slug>.wav, manifest.json and out/understand2_credits.txt.
import json, os, urllib.parse
import fetch_audio as fa

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "incoming", "understand")
OUT = os.path.join(HERE, "cache", "audio", "understand2")
os.makedirs(OUT, exist_ok=True)
CLIPS = {  # name: (Commons file, start, end, author, licence); videos were converted to .wav (same name)
    "Bislama": ("WIKITONGUES- Toukala speaking Bislama.webm", 2.3, 10.5, "Wikitongues", "CC BY 3.0"),
    "Afrikaans": ("Farren speaking Afrikaans.webm", 39.3, 53.1, "Wikitongues Inc", "CC BY-SA 4.0"),
    "Shetlandic": ("WIKITONGUES- Christine speaking Shetlandic.webm", 528.3, 540.0, "Christine De Luca, Wikitongues", "CC BY 3.0"),
    "Nigerian Pidgin": ("Tochi speaking Nigerian Pidgin.webm", 43.3, 56.0, "Wikitongues, Inc", "CC0"),
    "Gullah": ("WIKITONGUES- Caroline speaking Gullah and English.webm", 519.3, 533.9, "Wikitongues", "CC BY 3.0"),
}
page = lambda t: "https://commons.wikimedia.org/wiki/" + urllib.parse.quote("File:" + t.replace(" ", "_"))
PRE = {}
manifest, lines = {}, ["Audio credits (Languages English Speakers Can Almost Understand, Part 2)", ""]
for name, (f, start, end, author, lic) in CLIPS.items():
    need = round(end - start, 2)
    dst = os.path.join(OUT, fa.slug(name) + ".wav")
    fa.to_wav(os.path.join(SRC, f.replace(".webm", ".wav")), dst, start, need, extra=PRE.get(name, "") + f"afade=t=in:d=0.15,afade=t=out:st={need - 0.4}:d=0.4,loudnorm=I=-18:TP=-2")
    manifest[name] = {"sig": "understand2|" + name, "credits": [{"title": "File:" + f, "artist": author, "license": lic, "page": page(f)}], "captions": [], "start": start}
    lines.append(f'{name}: "{f}" by {author}, {lic}, via Wikimedia Commons, {page(f)}')
    print(name, need, "s from", start)
json.dump(manifest, open(os.path.join(OUT, "manifest.json"), "w"), indent=1, ensure_ascii=False)
open(os.path.join(HERE, "out", "understand2_credits.txt"), "w").write("\n".join(lines) + "\n")

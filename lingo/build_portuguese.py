# Audio for "Languages Portuguese Speakers Can Almost Understand": python3 build_portuguese.py
# Real recordings from Wikimedia Commons (Wikitongues interviews, a Galician radio interview, a Mirandese poem reading,
# a Fala school video, an Aruba Wikipedia video), downloaded with the browser into incoming/portuguese/.
# Every language has a clear link to Portuguese. Cape Verdean Creole was dropped: the only video mixes Portuguese and
# Creole, and the Creole could not be verified.
# Writes cache/audio/portuguese_understand/<slug>.wav, manifest.json and out/portuguese_understand_credits.txt.
import json, os, urllib.parse
import fetch_audio as fa

HERE = os.path.dirname(os.path.abspath(__file__))
KEY = "portuguese_understand"
SRC = os.path.join(HERE, "incoming", "portuguese")
OUT = os.path.join(HERE, "cache", "audio", KEY)
os.makedirs(OUT, exist_ok=True)
CLIPS = {  # name: (Commons file, start, end) — quotes checked with Whisper (word timestamps + translate)
    "Fala": ("Fala en la III Convivencia Intercentros del Parque Cultural de la Sierra de Gata.webm", 77.6, 99.5),
    "Mirandese": ("Lhiçon de Giografie.wav", 0.0, 13.9),
    "Leonese": ("WIKITONGUES- José Benito speaking Leonese.webm", 0.0, 15.5),
    "Spanish": ("WIKITONGUES- Azariah speaking Spanish.webm", 1.2, 16.6),
    "Papiamento": ("Episodio 1 Introduccion Wikipedia riba Aruba (na Papiamento).webm", 5.2, 24.6),
    "Galician": ("Galegos no baix -Ràdio Sant Boi -Amador Arias (29-05-2019).ogg", 153.6, 168.4),
}
EXTRA = json.load(open(os.path.join(HERE, "incoming", "portuguese", "extra_clips.json"))) if os.path.exists(os.path.join(SRC, "extra_clips.json")) else {}
CLIPS.update({k: tuple(v) for k, v in EXTRA.items()})
META = json.load(open(os.path.join(SRC, "meta.json")))  # licence + author as listed on each Commons file page
manifest, lines = {}, ["Audio credits (Languages Portuguese Speakers Can Almost Understand)", ""]
for name, (f, s, e) in CLIPS.items():
    m = META[f]
    page = "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(("File:" + f).replace(" ", "_"))
    need = round(e - s, 2)
    fa.to_wav(os.path.join(SRC, f.replace("/", "_").replace('"', "_")), os.path.join(OUT, fa.slug(name) + ".wav"), s, need,
              extra=f"afade=t=in:d=0.15,afade=t=out:st={need - 0.4}:d=0.4,loudnorm=I=-18:TP=-2")
    artist = m["artist"].strip('"')
    manifest[name] = {"sig": f"{KEY}|{name}", "start": s, "captions": [],
                      "credits": [{"title": "File:" + f, "artist": artist, "license": m["license"], "page": page}]}
    lines.append(f'{name}: "{f.rsplit(".", 1)[0]}" by {artist}, {m["license"]}, via Wikimedia Commons, {page}')
    print(name, need, "s from", s)
json.dump(manifest, open(os.path.join(OUT, "manifest.json"), "w"), indent=1, ensure_ascii=False)
open(os.path.join(HERE, "out", f"{KEY}_credits.txt"), "w").write("\n".join(lines) + "\n")

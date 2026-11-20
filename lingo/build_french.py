# Audio for "Languages French Speakers Can Almost Understand": python3 build_french.py
# Real recordings from Wikimedia Commons (Wikitongues interviews, RFI "Yvan Amar" creole interviews), downloaded with
# the browser into incoming/french/ (Commons API rate limit). Every language here has a clear link to French
# (owner, 2026-11-20: "only the meaningful ones", no viewer can say "there's no link").
# Writes cache/audio/french_understand/<slug>.wav, manifest.json and out/french_understand_credits.txt.
import json, os, urllib.parse
import fetch_audio as fa

HERE = os.path.dirname(os.path.abspath(__file__))
KEY = "french_understand"
SRC = os.path.join(HERE, "incoming", "french")
OUT = os.path.join(HERE, "cache", "audio", KEY)
os.makedirs(OUT, exist_ok=True)
CLIPS = {  # name: (Commons file, start, end) — quotes checked with Whisper (transcribe + translate)
    "Jèrriais": ("Geraint speaking Jèrriais.webm", 9.3, 25.6),
    "Norman": ("Jean Avenel 20201006 Nrf.webm", 9.6, 33.0),
    "Picard": ("Sasha speaking Picard.webm", 0.0, 16.0),
    "Louisiana Creole": ("The Louisiana Creole language, casually spoken - Taalib speaking Kouri-Vini - Wikitongues.webm", 65.7, 84.0),
    "Haitian Creole": ("WIKITONGUES- Castelline speaking Haitian Creole.webm", 56.0, 67.0),
    "Occitan": ("Paulina speaking Gascon.webm", 0.2, 15.2),
    "Catalan": ("WIKITONGUES- Guillem speaking Catalan.webm", 0.1, 13.1),
}
EXTRA = json.load(open(os.path.join(HERE, "incoming", "french", "extra_clips.json"))) if os.path.exists(os.path.join(SRC, "extra_clips.json")) else {}
CLIPS.update({k: tuple(v) for k, v in EXTRA.items()})
META = json.load(open(os.path.join(SRC, "meta.json")))  # licence + author as listed on each Commons file page
manifest, lines = {}, ["Audio credits (Languages French Speakers Can Almost Understand)", ""]
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

# Audio for "Languages Dutch Speakers Can Almost Understand": python3 build_dutch.py
# Real recordings from Wikimedia Commons (Wikitongues), downloaded with the browser into incoming/dutch/ and kept as
# audio only (<name>.audio.ogg). Meanings: Commons English subtitles (West Frisian), Commons Sranan subtitles translated
# (Sranan), Whisper transcripts checked for coherence (Brabantian/Helmonds, Bildts, Afrikaans, Gronings).
# Dropped: Tiens Flemish (proverbs, no reliable meaning), West Flemish (Bontje: overlapping conversation), Twents and
# East Frisian Low Saxon (no reliable transcript), Stephan and Simon (Frisian conversation, no subtitles).
# Writes cache/audio/dutch_understand/<slug>.wav, manifest.json and out/dutch_understand_credits.txt.
import json, os, urllib.parse
import fetch_audio as fa

HERE = os.path.dirname(os.path.abspath(__file__))
KEY = "dutch_understand"
SRC = os.path.join(HERE, "incoming", "dutch")
OUT = os.path.join(HERE, "cache", "audio", KEY)
os.makedirs(OUT, exist_ok=True)
CLIPS = {  # name: (Commons file, start, end)
    "Brabantian": ("WIKITONGUES- Jan speaking Brabants.webm", 22.6, 43.2),  # after "now I'll just start": in Helmonds
    "Bildts": ("WIKITONGUES- Anna speaking Bildts.webm", 0.0, 21.8),
    "Afrikaans": ("WIKITONGUES- Alaric speaking Afrikaans.webm", 0.0, 26.6),
    "Gronings": ("WIKITONGUES- Theo speaking Gronings.webm", 0.0, 19.2),
    "West Frisian": ("WIKITONGUES- Sjoukje speaking West Frisian.webm", 11.8, 34.6),  # new part (other videos used 0-14 s)
    "Sranan Tongo": ("WIKITONGUES- Hans speaking Sranan.webm", 0.6, 25.9),
}
META = json.load(open(os.path.join(SRC, "meta.json")))
manifest, lines = {}, ["Audio credits (Languages Dutch Speakers Can Almost Understand)", ""]
for name, (f, s, e) in CLIPS.items():
    m = META[f]
    page = "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(("File:" + f).replace(" ", "_"))
    need = round(e - s, 2)
    fa.to_wav(os.path.join(SRC, f.rsplit(".", 1)[0] + ".audio.ogg"), os.path.join(OUT, fa.slug(name) + ".wav"), s, need,
              extra=f"afade=t=in:d=0.15,afade=t=out:st={need - 0.4}:d=0.4,loudnorm=I=-18:TP=-2")
    artist = m["artist"].strip('"')
    manifest[name] = {"sig": f"{KEY}|{name}", "start": s, "captions": [],
                      "credits": [{"title": "File:" + f, "artist": artist, "license": m["license"], "page": page}]}
    lines.append(f'{name}: "{f.rsplit(".", 1)[0]}" by {artist}, {m["license"]}, via Wikimedia Commons, {page}')
    print(name, need, "s from", s, "->", fa.slug(name))
json.dump(manifest, open(os.path.join(OUT, "manifest.json"), "w"), indent=1, ensure_ascii=False)
open(os.path.join(HERE, "out", f"{KEY}_credits.txt"), "w").write("\n".join(lines) + "\n")

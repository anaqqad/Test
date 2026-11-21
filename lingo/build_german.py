# Audio for "Languages German Speakers Can Almost Understand": python3 build_german.py
# Sources: Wikimedia Commons recordings (downloaded/cached by fetch_audio). Each clip runs from start to end, faded and loudness-matched.
# Writes cache/audio/german/<slug>.wav, manifest.json and out/german_credits.txt.
import json, os
import fetch_audio as fa

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "cache", "audio", "german")
os.makedirs(OUT, exist_ok=True)
CLIPS = {  # name: (Commons file, start, end)
    "Luxembourgish": ("WIKITONGUES- Mark speaking Luxembourgish.webm", 0.0, 8.4),
    "Alsatian": ("WIKITONGUES- Dominique speaking Alsatian.webm", 0.0, 10.2),
    "Swiss German": ("WIKITONGUES- Fabia speaking Swiss German.webm", 0.2, 12.3),
    "Yiddish": ("WIKITONGUES- Suri speaking Yiddish.webm", 2.0, 11.4),
    "Limburgish": ("WIKITONGUES- Carolien speaking Limburgish.webm", 3.4, 16.6),
    "Dutch": ("WIKITONGUES- Eva speaking Dutch.webm", 0.0, 12.6),
    "Afrikaans": ("WIKITONGUES- Roussow speaking Afrikaans.webm", 4.0, 13.0),
    "West Frisian": ("WIKITONGUES- Sjoukje speaking West Frisian.webm", 0.2, 14.3),
}
manifest, lines = {}, ["Audio credits (Languages German Speakers Can Almost Understand)", ""]
for name, (f, start, end) in CLIPS.items():
    meta = fa.info(f)
    src = fa.download(meta)
    need = round(end - start, 2)
    dst = os.path.join(OUT, fa.slug(name) + ".wav")
    fa.to_wav(src, dst, start, need, extra=f"afade=t=in:d=0.15,afade=t=out:st={need - 0.4}:d=0.4,loudnorm=I=-18:TP=-2")
    manifest[name] = {"sig": "german|" + name, "credits": [{"title": meta["title"], "artist": meta["artist"], "license": meta["license"], "page": meta["page"]}], "captions": [], "start": start}
    lines.append(f'{name}: "{f}" by {meta["artist"]}, {meta["license"]}, via Wikimedia Commons, {meta["page"]}')
    print(name, need, "s from", start)
json.dump(manifest, open(os.path.join(OUT, "manifest.json"), "w"), indent=1, ensure_ascii=False)
open(os.path.join(HERE, "out", "german_credits.txt"), "w").write("\n".join(lines) + "\n")

# Audio for "Language Isolates be like": python3 build_isolates.py
# Sources in cache/isolates/src: Creative Commons (CC BY) YouTube videos downloaded by the owner. Speech clips are cut from `start` for the length of the segment
# and loudness-matched.
# Writes cache/audio/isolates/<slug>.wav, manifest.json and out/isolates_credits.txt.
import json, os, subprocess, urllib.parse
import fetch_audio as fa

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "cache", "isolates", "src")
OUT = os.path.join(HERE, "cache", "audio", "isolates")
os.makedirs(OUT, exist_ok=True)
NEED = round(1.4 + 5.0 * 3 + 1.2, 2)  # story segment with 3 cards
CLIPS = {  # name: (source file, start, title, author, licence)
    "Burushaski": ("burushaski.m4a", 112.0, "A COVID-19 survivor's story in Burushaski - Izhar Hunzai", "virallanguages", "CC BY"),
    "Mapudungun": ("mapudungun.m4a", 12.0, "WIKITONGUES: Victor speaking Mapudungun", "Wikitongues", "CC BY"),
    "Sandawe": ("sandawe.m4a", 194.0, "Sandawe audio: sad_word-list_1991_01", "UCLA Phonetics Lab", "CC BY"),
    "Warao": ("warao.m4a", 36.0, "Warao - Genesis 33.1-16", "ScriptureEarth", "CC BY"),
    "Tiwi": ("tiwi.webm", 29.0, "Tiwi audio: tiw_word-list_1976_01", "UCLA Phonetics Lab", "CC BY"),
}
YOUTUBE = {"Burushaski": "https://www.youtube.com/watch?v=U_-cSan4r_E", "Mapudungun": "https://www.youtube.com/watch?v=DcPu6zLpZoQ",
           "Sandawe": "https://www.youtube.com/watch?v=MP4ps6_32y4", "Warao": "https://www.youtube.com/watch?v=Re2Td8BHgaI",
           "Tiwi": "https://www.youtube.com/watch?v=FceqHZa8X3E"}
page = lambda t: "https://commons.wikimedia.org/wiki/" + urllib.parse.quote("File:" + t.replace(" ", "_"))
manifest, lines = {}, ["Audio credits (Language Isolates be like)", ""]
for name, (f, start, title, author, lic) in CLIPS.items():
    src = os.path.join(SRC, f)
    if not os.path.exists(src):
        print(name, "missing", f); manifest[name] = None; continue
    dst = os.path.join(OUT, fa.slug(name) + ".wav")
    fa.to_wav(src, dst, start, NEED, extra=f"afade=t=in:d=0.3,afade=t=out:st={NEED - 0.8}:d=0.8,loudnorm=I=-18:TP=-2")
    yt = YOUTUBE.get(name)
    link = yt or page(title)
    manifest[name] = {"sig": "isolates|" + name, "credits": [{"title": title if yt else "File:" + title, "artist": author, "license": lic, "page": link}], "captions": [], "start": start}
    lines.append(f'{name}: "{title}" by {author}, {lic} (Creative Commons Attribution), YouTube, {link}')
    print(name, NEED, "s from", start)
json.dump(manifest, open(os.path.join(OUT, "manifest.json"), "w"), indent=1, ensure_ascii=False)
open(os.path.join(HERE, "out", "isolates_credits.txt"), "w").write("\n".join(lines) + "\n")

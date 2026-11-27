# Audio for "Language Isolates be like (Part 2)": python3 build_isolates2.py
# Sources in cache/isolates2/src: Creative Commons YouTube videos downloaded by the owner, plus Karuk from Wikimedia Commons. Speech clips are cut from `start` for the length of the segment
# and loudness-matched.
# Writes cache/audio/isolates/<slug>.wav, manifest.json and out/isolates_credits.txt.
import json, os, subprocess, urllib.parse
import fetch_audio as fa

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "cache", "isolates2", "src")
OUT = os.path.join(HERE, "cache", "audio", "isolates2")
os.makedirs(OUT, exist_ok=True)
NEED = round(1.4 + 5.0 * 3 + 1.2, 2)  # story segment with 3 cards
CLIPS = {  # name: (source file, start, title, author, licence)
    "Purépecha": ("purepecha.m4a", 341.2, "Aprende los saludos en Purépecha--- Tutorial 5 parte", "Michoacán Intercultural", "CC BY"),
    "Ticuna": ("ticuna.webm", 8.3, "Abel Antonio Santos - tikuna - #ActivismoLenguasCO", "Rising Voices", "CC BY"),
    "Hadza": ("hadza.mp4", 2.0, "Hadza audio: hts_story_1991_01", "UCLA Phonetics Lab", "CC BY"),
    "Haida": ("haida.mp4", 0.4, "Haida Language: How is the Weather Today?", "X̱aad Kíl", "CC BY"),
    "Karuk": ("karuk.webm", 32.0, "Conversational Karuk Language Part 1.webm", "Julian Lang", "CC BY 3.0"),
}
YOUTUBE = {"Purépecha": "https://www.youtube.com/watch?v=3rnkCjvO0kg", "Ticuna": "https://www.youtube.com/watch?v=u2nvEfLybv4",
           "Hadza": "https://www.youtube.com/watch?v=IeFQs6SCd-s", "Haida": "https://www.youtube.com/watch?v=WiMYKegVxhQ"}
page = lambda t: "https://commons.wikimedia.org/wiki/" + urllib.parse.quote("File:" + t.replace(" ", "_"))
manifest, lines = {}, ["Audio credits (Language Isolates be like, Part 2)", ""]
for name, (f, start, title, author, lic) in CLIPS.items():
    src = os.path.join(SRC, f)
    if not os.path.exists(src):
        print(name, "missing", f); manifest[name] = None; continue
    dst = os.path.join(OUT, fa.slug(name) + ".wav")
    fa.to_wav(src, dst, start, NEED, extra=f"afade=t=in:d=0.3,afade=t=out:st={NEED - 0.8}:d=0.8,loudnorm=I=-18:TP=-2")
    yt = YOUTUBE.get(name)
    link = yt or page(title)
    manifest[name] = {"sig": "isolates2|" + name, "credits": [{"title": title if yt else "File:" + title, "artist": author, "license": lic, "page": link}], "captions": [], "start": start}
    lines.append(f'{name}: "{title}" by {author}, {lic} (Creative Commons Attribution), {"YouTube" if yt else "via Wikimedia Commons"}, {link}')
    print(name, NEED, "s from", start)
json.dump(manifest, open(os.path.join(OUT, "manifest.json"), "w"), indent=1, ensure_ascii=False)
open(os.path.join(HERE, "out", "isolates2_credits.txt"), "w").write("\n".join(lines) + "\n")

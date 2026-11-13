# Audio for "Languages Turkish Speakers Can Almost Understand": python3 build_turkic.py
# Sources: Wikimedia Commons recordings kept in incoming/turkic. Each clip runs from start to end, faded and loudness-matched.
# Writes cache/audio/turkic/<slug>.wav, manifest.json and out/turkic_credits.txt.
import json, os, urllib.parse
import fetch_audio as fa

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "incoming", "turkic")
OUT = os.path.join(HERE, "cache", "audio", "turkic")
os.makedirs(OUT, exist_ok=True)
CLIPS = {  # name: (Commons file, start, end, author, licence)
    "Kyrgyz": ("An example of a dialogue in Kyrgyz. Two friends are communicating.wav", 0.0, 17.6, "ПервыйЧеловекВКосмосн", "CC0"),
    "Kazakh": ("Qazaqsha zhyl sanau.ogg", 0.0, 6.9, "Tmrtlght", "CC BY-SA 4.0"),
    "Uzbek": ("Farhodning jasorati.ogg", 13.4, 20.3, "Madina Ibodullayeva", "CC BY-SA 4.0"),
    "Tatar": ("Article 1 in Tatar.flac", 0.0, 12.2, "Törekuğlı & Bulat Şəymi", "CC BY 4.0"),
    "Azerbaijani": ("Qazax ləhcəsində nağıl.ogg", 2.0, 8.9, "Ulvimamedov57", "CC BY-SA 4.0"),
}
page = lambda t: "https://commons.wikimedia.org/wiki/" + urllib.parse.quote("File:" + t.replace(" ", "_"))
manifest, lines = {}, ["Audio credits (Languages Turkish Speakers Can Almost Understand)", ""]
for name, (f, start, end, author, lic) in CLIPS.items():
    need = round(end - start, 2)
    dst = os.path.join(OUT, fa.slug(name) + ".wav")
    fa.to_wav(os.path.join(SRC, f), dst, start, need, extra=f"afade=t=in:d=0.15,afade=t=out:st={need - 0.4}:d=0.4,loudnorm=I=-18:TP=-2")
    manifest[name] = {"sig": "turkic|" + name, "credits": [{"title": "File:" + f, "artist": author, "license": lic, "page": page(f)}], "captions": [], "start": start}
    lines.append(f'{name}: "{f}" by {author}, {lic}, via Wikimedia Commons, {page(f)}')
    print(name, need, "s from", start)
json.dump(manifest, open(os.path.join(OUT, "manifest.json"), "w"), indent=1, ensure_ascii=False)
open(os.path.join(HERE, "out", "turkic_credits.txt"), "w").write("\n".join(lines) + "\n")

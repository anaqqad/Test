# Audio for "Languages Russian Speakers Can Almost Understand": python3 build_slavic.py
# Sources: Wikimedia Commons recordings kept in incoming/slavic. Each clip runs from start to end, faded and loudness-matched.
# Writes cache/audio/slavic/<slug>.wav, manifest.json and out/slavic_credits.txt.
import json, os, urllib.parse
import fetch_audio as fa

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "incoming", "slavic")
OUT = os.path.join(HERE, "cache", "audio", "slavic")
os.makedirs(OUT, exist_ok=True)
CLIPS = {  # name: (Commons file, start, end, author, licence); Wikitongues videos were converted to .wav (same name)
    "Czech": ("Boleslav I.ogg", 10.0, 21.9, "Ludek (speaker), Czech Wikipedia authors", "Public domain"),
    "Polish": ("WIKITONGUES- Marta speaking Polish.webm", 0.0, 14.0, "Wikitongues, Marta Sawicka", "CC BY-SA 4.0"),
    "Serbian": ("Glas-.ogg", 0.0, 8.4, "JanaIlic1979", "CC0"),
    "Bulgarian": ("Dobrovolets.ogg", 0.6, 10.4, "Dbogdev", "CC BY 2.5"),
    "Ukrainian": ("WIKITONGUES- Vira speaking Ukrainian.webm", 0.0, 11.3, "Wikitongues, Kristen Tcherneshoff", "CC BY-SA 4.0"),
    "Belarusian": ("WIKITONGUES- Uladzislau speaking Belarusian.webm", 0.0, 10.0, "Wikitongues, Antonio Alamillo", "CC BY-SA 4.0"),
}
page = lambda t: "https://commons.wikimedia.org/wiki/" + urllib.parse.quote("File:" + t.replace(" ", "_"))
PRE = {"Bulgarian": "highpass=f=80:poles=2,bandreject=f=60:width_type=h:w=6,bandreject=f=120:width_type=h:w=6,bandreject=f=180:width_type=h:w=6,"}  # 60 Hz mains hum in the source
manifest, lines = {}, ["Audio credits (Languages Russian Speakers Can Almost Understand)", ""]
for name, (f, start, end, author, lic) in CLIPS.items():
    need = round(end - start, 2)
    dst = os.path.join(OUT, fa.slug(name) + ".wav")
    fa.to_wav(os.path.join(SRC, f.replace(".webm", ".wav")), dst, start, need, extra=PRE.get(name, "") + f"afade=t=in:d=0.15,afade=t=out:st={need - 0.4}:d=0.4,loudnorm=I=-18:TP=-2")
    manifest[name] = {"sig": "slavic|" + name, "credits": [{"title": "File:" + f, "artist": author, "license": lic, "page": page(f)}], "captions": [], "start": start}
    lines.append(f'{name}: "{f}" by {author}, {lic}, via Wikimedia Commons, {page(f)}')
    print(name, need, "s from", start)
json.dump(manifest, open(os.path.join(OUT, "manifest.json"), "w"), indent=1, ensure_ascii=False)
open(os.path.join(HERE, "out", "slavic_credits.txt"), "w").write("\n".join(lines) + "\n")

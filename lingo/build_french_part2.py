# Audio for "Languages French Speakers Can Almost Understand (Part 2)": python3 build_french_part2.py
# Real recordings: Wikitongues / YouTube Creative Commons uploads (see credits), cut in incoming/french2/ (16 kHz wav).
# No translations are used: each card gives facts about the language only.
import json, os, subprocess
import fetch_audio as fa

HERE = os.path.dirname(os.path.abspath(__file__))
KEY = "french_part2"
SRC = os.path.join(HERE, "incoming", "french2")
OUT = os.path.join(HERE, "cache", "audio", KEY)
os.makedirs(OUT, exist_ok=True)
CLIPS = {  # name: (source wav, credit line)
    "Breton": ("breton_0_25.wav", 'Breton: "WIKITONGUES: Jean Luc speaking Breton" by Wikitongues, CC BY 3.0 (YouTube), https://www.youtube.com/watch?v=29euYj0k1Kk'),
    "Corsican": ("corsican_0_25.wav", 'Corsican: "WIKITONGUES: Paulu speaking Corsican" by Wikitongues, CC BY 3.0 (YouTube)'),
    "Walloon": ("walloon_52_77.wav", 'Walloon: "Romain Berger, professeur de wallon" by Walloon Immersion, CC BY 3.0 (YouTube), https://www.youtube.com/watch?v=LdQgFF-rDUs'),
    "Alsatian": ("alsatian_0_25.wav", 'Alsatian: "WIKITONGUES: Dominique speaking Alsatian" by Wikitongues, Kristen Tcherneshoff, CC BY-SA 4.0'),
    "Franco-Provençal": ("franco_60_85.wav", 'Franco-Provençal: "Cornetta - Francoprovençal" by Webécole, CC BY 3.0 (YouTube), https://www.youtube.com/watch?v=-vSUXPnm5mo'),
}
manifest, lines = {}, ["Audio credits (Languages French Speakers Can Almost Understand, Part 2)", ""]
for name, (wav, credit) in CLIPS.items():
    dst = os.path.join(OUT, fa.slug(name) + ".wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(SRC, wav), "-af",
                    "afade=t=in:d=0.15,afade=t=out:st=24.6:d=0.4,loudnorm=I=-18:TP=-2", "-ar", str(fa.SR), dst], check=True)
    manifest[name] = {"sig": f"{KEY}|{name}", "start": 0, "captions": [], "credits": [{"title": credit, "artist": "", "license": "", "page": ""}]}
    lines.append(credit)
    print(name, fa.slug(name))
json.dump(manifest, open(os.path.join(OUT, "manifest.json"), "w"), indent=1, ensure_ascii=False)
open(os.path.join(HERE, "out", f"{KEY}_credits.txt"), "w").write("\n".join(lines) + "\n")

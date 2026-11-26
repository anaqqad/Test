# Audio for "American Accents be like (Part 1)": python3 build_us_accents.py
# Real public speeches from Wikimedia Commons (US federal works, public domain; the Tornillo recording is CC BY 3.0),
# downloaded into incoming/accents/recent/ and kept as audio only (<name>.audio.ogg). English speech, so no translation:
# the reveal card quotes the speech. Writes cache/audio/us_accents/<slug>.wav, manifest.json and out/us_accents_credits.txt.
import json, os, subprocess, urllib.parse, glob
import fetch_audio as fa

HERE = os.path.dirname(os.path.abspath(__file__))
KEY = "us_accents"
SRC = os.path.join(HERE, "incoming", "accents", "recent")
OUT = os.path.join(HERE, "cache", "audio", KEY)
os.makedirs(OUT, exist_ok=True)
CLIPS = {  # name: (Commons stem, [(start, end)])
    "New York": ("President Trump Delivers Remarks at the 2020 National Christmas Tree Lighting", [(0.5, 25.5)]),
    "Georgia": ("Senator Raphael Warnock speaks in support of the nomination of Ketanji Brown Jackson to the Supreme Court", [(0.0, 25.0)]),
    "Illinois": ("State of the Union Address (January 25, 2011) Barack Obama (WhiteHouse.gov)", [(0.0, 25.0)]),
    "Pennsylvania": ("Joe Biden gives remarks on the Inflation Reduction Act", [(0.0, 25.0)]),
    "California": ("Vice President Harris Selma Commemoration Service", [(1.0, 26.0)]),
}
META = json.load(open(os.path.join(SRC, "meta.json")))
manifest, lines = {}, ["Audio credits (American Accents be like, Part 1)", ""]
for name, (stem, parts) in CLIPS.items():
    src = os.path.join(SRC, stem + ".audio.ogg")
    mkey = [k for k in META if k.rsplit(".", 1)[0] == stem][0]; m = META[mkey]
    page = m["page"]; dst = os.path.join(OUT, fa.slug(name) + ".wav")
    tmp = []
    for i, (s, e) in enumerate(parts):
        t = dst + f".part{i}.wav"; fa.to_wav(src, t, s, round(e - s, 2)); tmp.append(t)
    os.replace(tmp[0], dst + ".raw.wav") if len(tmp) == 1 else None
    need = round(sum(e - s for s, e in parts), 2)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", dst + ".raw.wav", "-af",
                    f"afade=t=in:d=0.15,afade=t=out:st={need - 0.4}:d=0.4,loudnorm=I=-18:TP=-2", "-ar", str(fa.SR), dst], check=True)
    os.remove(dst + ".raw.wav")
    artist = m["artist"].strip('"')
    manifest[name] = {"sig": f"{KEY}|{name}", "start": parts[0][0], "parts": parts, "captions": [],
                      "credits": [{"title": "File:" + mkey, "artist": artist, "license": m["license"], "page": page}]}
    lines.append(f'{name}: "{stem}" by {artist}, {m["license"]}, via Wikimedia Commons, {page}')
    print(name, need, "s ->", fa.slug(name))
json.dump(manifest, open(os.path.join(OUT, "manifest.json"), "w"), indent=1, ensure_ascii=False)
open(os.path.join(HERE, "out", f"{KEY}_credits.txt"), "w").write("\n".join(lines) + "\n")

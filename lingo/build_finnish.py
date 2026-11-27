# Audio for "Languages Finnish Speakers Can Almost Understand": python3 build_finnish.py
# Real recordings from Wikimedia Commons, downloaded with the browser into incoming/finnish/ and kept as audio only
# (<name>.audio.ogg). Meanings: Commons English subtitles (Estonian, Livvi), the Ludic text and English translation on
# the file page plus Commons Russian subtitles (Ludic), Whisper transcripts checked for coherence (Võro, Veps,
# Siberian Ingrian Finnish, Hungarian).
# Not found on Commons: Meänkieli, Kven, Livonian, Votic, Izhorian (only lectures about them), Seto.
# Writes cache/audio/finnish_understand/<slug>.wav, manifest.json and out/finnish_understand_credits.txt.
import json, os, subprocess, urllib.parse
import fetch_audio as fa

HERE = os.path.dirname(os.path.abspath(__file__))
KEY = "finnish_understand"
SRC = os.path.join(HERE, "incoming", "finnish")
OUT = os.path.join(HERE, "cache", "audio", KEY)
os.makedirs(OUT, exist_ok=True)
CLIPS = {  # name: (Commons file, [(start, end), ...]); two parts are joined with a short crossfade
    "Estonian": ("WIKITONGUES- Liisi speaking Estonian.webm", [(1.5, 23.7)]),  # after "In Estonian then"
    "Võro": ("WIKITONGUES- Toomas speaking Võro.webm", [(0.0, 26.3)]),
    "Livvi Karelian": ("Livvi-Karelian dialect and VepKar corpus by Tatiana Boiko, 2018.webm", [(0.3, 27.3)]),
    "Ludic": ("Ludic language by Alexandra Rodionova, 2018.webm", [(0.3, 28.4)]),  # Ludic part; Russian from 40 s
    "Veps": ("Listen to the Veps language of Karelia - Eniisi speaking Vepsian - Wikitongues.webm", [(0.0, 25.7)]),
    # the ABC-book picture (45-59 s) and the dog stealing the bread (78-89 s); 59-78 s is unclear and left out
    "Siberian Ingrian Finnish": ("SiberianIngrianFinnish MAP-49 Ubaleht 2022-07-19.webm", [(45.0, 59.0), (77.7, 89.0)]),
    "Hungarian": ("WIKITONGUES- Orsolya speaking Hungarian.webm", [(3.1, 27.9)]),  # native speaker (Gabriel: 6-day learner)
}
META = json.load(open(os.path.join(SRC, "meta.json")))
manifest, lines = {}, ["Audio credits (Languages Finnish Speakers Can Almost Understand)", ""]
for name, (f, parts) in CLIPS.items():
    m = META[f]
    page = "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(("File:" + f).replace(" ", "_"))
    src = os.path.join(SRC, f.rsplit(".", 1)[0] + ".audio.ogg"); dst = os.path.join(OUT, fa.slug(name) + ".wav")
    tmp = []
    for i, (s, e) in enumerate(parts):
        t = dst + f".part{i}.wav"; fa.to_wav(src, t, s, round(e - s, 2)); tmp.append(t)
    if len(tmp) == 1:
        os.replace(tmp[0], dst + ".raw.wav")
    else:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp[0], "-i", tmp[1], "-filter_complex", "acrossfade=d=0.25", dst + ".raw.wav"], check=True)
        [os.remove(t) for t in tmp]
    need = round(sum(e - s for s, e in parts) - 0.25 * (len(parts) - 1), 2)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", dst + ".raw.wav", "-af",
                    f"afade=t=in:d=0.15,afade=t=out:st={need - 0.4}:d=0.4,loudnorm=I=-18:TP=-2", "-ar", str(fa.SR), dst], check=True)
    os.remove(dst + ".raw.wav")
    s = parts[0][0]
    artist = m["artist"].strip('"')
    manifest[name] = {"sig": f"{KEY}|{name}", "start": s, "parts": parts, "captions": [],
                      "credits": [{"title": "File:" + f, "artist": artist, "license": m["license"], "page": page}]}
    lines.append(f'{name}: "{f.rsplit(".", 1)[0]}" by {artist}, {m["license"]}, via Wikimedia Commons, {page}')
    print(name, need, "s from", s, "->", fa.slug(name))
json.dump(manifest, open(os.path.join(OUT, "manifest.json"), "w"), indent=1, ensure_ascii=False)
open(os.path.join(HERE, "out", f"{KEY}_credits.txt"), "w").write("\n".join(lines) + "\n")

# Audio for "How Different Do Chinese Dialects Sound": python3 build_chinese.py
# Real recordings from Wikimedia Commons (Wikitongues interviews and a public-domain Mandarin speaking clock), downloaded
# with the browser into incoming/chinese/ and kept as audio only (<name>.audio.ogg) to save disk space.
# Meanings: Commons subtitles (Shanghainese, Henan, Guiyang: English; Linhai: Chinese, first lines), Timothy's own English
# transcript on the file page (Penang Hokkien), Whisper transcripts checked for coherence (Yunnan, Siyi Yue, clock).
# Dropped: Hakka, Gan (Hukou), Wenling Wu, Medan Hokkien (no reliable meaning); "Menlu/Ramzy/Tricia ... Min" are Minangkabau.
# Writes cache/audio/chinese_dialects/<slug>.wav, manifest.json and out/chinese_dialects_credits.txt.
import json, os, urllib.parse
import fetch_audio as fa

HERE = os.path.dirname(os.path.abspath(__file__))
KEY = "chinese_dialects"
SRC = os.path.join(HERE, "incoming", "chinese")
OUT = os.path.join(HERE, "cache", "audio", KEY)
os.makedirs(OUT, exist_ok=True)
CLIPS = {  # name: (Commons file, start, end); local copy is <file minus extension>.audio.ogg for videos
    "Standard Mandarin": ("Chinese speaking clock female.oga", 0.8, 17.0),
    "Henan Dialect": ("WIKITONGUES- Ying speaking Henan Chinese.webm", 61.0, 85.2),
    "Guiyang Dialect": ("WIKITONGUES- Changjiu and Chaofen speaking Guiyangese.webm", 0.0, 23.7),
    "Yunnan Dialect": ("WIKITONGUES- Tao speaking Yunnan Mandarin with Thai and Taiwanese accent.webm", 0.0, 25.5),
    "Shanghainese": ("WIKITONGUES- Ivy speaking Shanghainese.webm", 1.0, 24.6),
    "Linhai Dialect": ("WIKITONGUES Charles speaking Linhainese 吴语临海方言.webm", 1.6, 21.0),
    "Siyi Yue": ("WIKITONGUES- Joseph speaking Siyi Yue.webm", 0.0, 24.0),
    "Penang Hokkien": ("WIKITONGUES- Timothy speaking Penang Hokkien.webm", 0.0, 24.0),
}
EXTRA = json.load(open(os.path.join(HERE, "incoming", "chinese", "extra_clips.json"))) if os.path.exists(os.path.join(SRC, "extra_clips.json")) else {}
CLIPS.update({k: tuple(v) for k, v in EXTRA.items()})
META = json.load(open(os.path.join(SRC, "meta.json")))  # licence + author as listed on each Commons file page
manifest, lines = {}, ["Audio credits (How Different Do Chinese Dialects Sound)", ""]
for name, (f, s, e) in CLIPS.items():
    m = META[f]
    page = "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(("File:" + f).replace(" ", "_"))
    need = round(e - s, 2)
    local = f.rsplit(".", 1)[0] + ".audio.ogg" if f.endswith(".webm") else f
    fa.to_wav(os.path.join(SRC, local), os.path.join(OUT, fa.slug(name) + ".wav"), s, need,
              extra=f"afade=t=in:d=0.15,afade=t=out:st={need - 0.4}:d=0.4,loudnorm=I=-18:TP=-2")
    artist = m["artist"].strip('"')
    manifest[name] = {"sig": f"{KEY}|{name}", "start": s, "captions": [],
                      "credits": [{"title": "File:" + f, "artist": artist, "license": m["license"], "page": page}]}
    lines.append(f'{name}: "{f.rsplit(".", 1)[0]}" by {artist}, {m["license"]}, via Wikimedia Commons, {page}')
    print(name, need, "s from", s)
json.dump(manifest, open(os.path.join(OUT, "manifest.json"), "w"), indent=1, ensure_ascii=False)
open(os.path.join(HERE, "out", f"{KEY}_credits.txt"), "w").write("\n".join(lines) + "\n")

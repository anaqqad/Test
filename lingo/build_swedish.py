# Audio for "Languages Swedish Speakers Can Almost Understand": python3 build_swedish.py
# Real recordings from Wikimedia Commons, downloaded with the browser into incoming/swedish/ (videos kept as <name>.audio.ogg).
# Meanings: SLS archive transcripts on the file pages (Närpes, Eckerö: dialect + standard Swedish), Commons English
# subtitles (Icelandic), the Wikipedia article text (Danish Spoken Wikipedia), the Rundata reading of G 134 plus the
# modern-Swedish reading by the same runologist (Runic Swedish), the Poetic Edda text of Reginsmál st. 1-2 (Old Norse),
# Whisper transcripts checked for coherence (Norwegian, Kristiansund: he says he is a grandfather).
# Not found on Commons/Lingua Libre as speech: Faroese (single words only), Elfdalian, Gutnish, Scanian, Jutlandic.
# Writes cache/audio/swedish_understand/<slug>.wav, manifest.json and out/swedish_understand_credits.txt.
import json, os, urllib.parse
import fetch_audio as fa

HERE = os.path.dirname(os.path.abspath(__file__))
KEY = "swedish_understand"
SRC = os.path.join(HERE, "incoming", "swedish")
OUT = os.path.join(HERE, "cache", "audio", KEY)
os.makedirs(OUT, exist_ok=True)
CLIPS = {  # name: (Commons file, start, end); local copy is <file minus extension>.audio.ogg for videos
    "Norwegian": ("Kristiansund1.2.ogg", 0.0, 26.0),
    "Åland Swedish": ("Finland Swedish Eckerö Åland dialect 1971.ogg", 0.0, 20.8),
    "Danish": ("Da-Solen.ogg", 29.6, 54.0),
    "Närpes Dialect": ("Finland Swedish Närpes Österbotten dialect 1982.ogg", 0.9, 21.6),
    "Icelandic": ("WIKITONGUES- Ljóni speaking Icelandic.webm", 0.9, 25.2),
    "Runic Swedish": ("G-134-runsvenska.opus", 0.0, 18.6),
    "Old Norse": ("Jackson speaking Old Norse.webm", 12.9, 37.2),
}
META = json.load(open(os.path.join(SRC, "meta.json")))  # licence + author as listed on each Commons file page
ARTIST = {  # the file page's author field is empty or "Unkown" for the SLS archive recordings
    "Finland Swedish Eckerö Åland dialect 1971.ogg": "Society of Swedish Literature in Finland (SLS 2269 1971:30; speaker Gustav Adolf Mattsson, interviewer Per-Henrik Solstrand)",
    "Finland Swedish Närpes Österbotten dialect 1982.ogg": "Society of Swedish Literature in Finland (SLS 2269 1982:68; speaker Edvin Nixhoim (as spelled on the file page), interviewer Ann-Marie Ivars)",
    "G-134-runsvenska.opus": "Maja Bäckvall, Swedish National Heritage Board",
}
manifest, lines = {}, ["Audio credits (Languages Swedish Speakers Can Almost Understand)", ""]
for name, (f, s, e) in CLIPS.items():
    m = META[f]
    page = "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(("File:" + f).replace(" ", "_"))
    need = round(e - s, 2)
    local = f.rsplit(".", 1)[0] + ".audio.ogg" if f.endswith(".webm") else f
    fa.to_wav(os.path.join(SRC, local), os.path.join(OUT, fa.slug(name) + ".wav"), s, need,
              extra=f"afade=t=in:d=0.15,afade=t=out:st={need - 0.4}:d=0.4,loudnorm=I=-18:TP=-2")
    artist = ARTIST.get(f, m["artist"].strip('"'))
    manifest[name] = {"sig": f"{KEY}|{name}", "start": s, "captions": [],
                      "credits": [{"title": "File:" + f, "artist": artist, "license": m["license"], "page": page}]}
    lines.append(f'{name}: "{f.rsplit(".", 1)[0]}" by {artist}, {m["license"]}, via Wikimedia Commons, {page}')
    print(name, need, "s from", s)
json.dump(manifest, open(os.path.join(OUT, "manifest.json"), "w"), indent=1, ensure_ascii=False)
open(os.path.join(HERE, "out", f"{KEY}_credits.txt"), "w").write("\n".join(lines) + "\n")

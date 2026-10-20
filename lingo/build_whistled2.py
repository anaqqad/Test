# Audio for "Whistled Languages be like, Part 2": python3 build_whistled2.py
# The sources are YouTube videos the uploaders gave the owner permission to use (cache/whistled2/src, links in
# links.txt). Only the whistled stretches are used (ranges found from the spectrograms and the subtitles);
# the on-screen translations become the captions. Writes cache/audio/whistled2/<slug>.wav, manifest.json and
# out/whistled2_credits.txt in the same shape fetch_audio.py produces, so render.mjs plays them as usual.
import json, os, re, subprocess
import fetch_audio as fa

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "cache", "whistled2", "src")
OUT = os.path.join(HERE, "cache", "audio", "whistled2")
os.makedirs(OUT, exist_ok=True)
slug = lambda s: re.sub(r"[^\w]+", "_", s, flags=re.U).strip("_").lower()  # same rule as render.mjs

ITEMS = {
 "Chinantec": {"ncards": 4, "src": [("mazatec_2_part3_1.mp4", [[76.3, 88.8]]), ("chinantec.mp4", [[0.2, 10.3]])],
   "captions": [(0.3, 2.0, "OK."), (2.2, 2.9, "What are you going to do tomorrow?"), (5.5, 2.3, "When noon comes?"), (8.2, 3.3, "I'm not going to do anything."),
                (13.0, 3.2, "Go and get your brother Sixto and we'll go over."), (16.3, 1.4, "Huh?"), (18.0, 2.8, "Go and get your brother Sixto. Over."), (21.0, 1.2, "OK, over."), (22.2, 1.5, "OK, over.")],
   "credit": {"title": "Chiflidos en la neblina (Chinantec whistled conversation) and Whistle Ex8, YouTube videos by Mark Sicoli", "artist": "Mark Sicoli", "license": "used with the uploader's permission", "page": "https://www.youtube.com/watch?v=QPuE0UMEMEs and https://www.youtube.com/watch?v=lRWy868lQpE"}},
 "Hmong": {"ncards": 4, "src": [("hmong.mp4", [[429.0, 450.6]])],
   "captions": [(0.5, 3.5, "I am going to the farm."), (4.5, 5.5, "Going to the farm, why do you ask?"), (11.0, 6.5, "I am going to wander around my rice fields."), (18.5, 3.5, "Hey, I am going to the farm.")],
   "credit": {"title": "Birdsong: the dying whistled language of the Hmong people in northern Laos, YouTube video by The Guardian", "artist": "The Guardian", "license": "used with permission", "page": "https://www.youtube.com/watch?v=_KIYwCieaMs"}},
 "Pirahã": {"ncards": 5, "src": [("piraha.mp4", [[10.8, 35.2]])],
   "captions": [(0.2, 4.5, "There's a monkey. Right above us."), (7.2, 3.6, "I see him."), (12.6, 3.6, "He will be very fast."), (17.2, 2.8, "Will you shoot him?"), (21.2, 3.0, "I will sneak close.")],
   "credit": {"title": "piraha, YouTube video uploaded by Cathy Lightfoot", "artist": "Cathy Lightfoot", "license": "used with the uploader's permission", "page": "https://www.youtube.com/watch?v=XyceRHzoMdM"}},
 "Wayãpi": {"ncards": 3, "src": [("wayapi_2.mp4", [[21.0, 35.5]])],
   "captions": [(0.6, 6.0, "oloota ole ia lupi: Let's leave together by canoe!"), (7.0, 6.5, "elapa alaa: I take my rifle!")],
   "credit": {"title": "A world of sound in the Amazon, wildlife imitations and whistled speech of the Wayãpi people, YouTube video by Labo LEEISA (CNRS, French Guiana), based on the research of Julien Meyer and Damien Davy", "artist": "Labo LEEISA", "license": "used with permission", "page": "https://www.youtube.com/watch?v=0rGkGw2l7p4"}},
}

manifest, lines = {}, ["Audio credits (Whistled Languages be like, Part 2)", ""]
for name, it in ITEMS.items():
    need = round(1.4 + 5.0 * it["ncards"] + 1.2, 2)
    parts, ins, k = [], [], 0
    for i, (f, ranges) in enumerate(it["src"]):
        ins += ["-i", os.path.join(SRC, f)]
        for a, b in ranges:
            parts.append(f"[{i}:a]atrim={a}:{b},asetpts=PTS-STARTPTS,apad=pad_dur=0.6[p{k}]"); k += 1
    filt = ";".join(parts) + ";" + "".join(f"[p{j}]" for j in range(k)) + f"concat=n={k}:v=0:a=1,aresample=48000,pan=stereo|c0=c0|c1=c0,loudnorm=I=-16:TP=-1.5,apad,atrim=0:{need},afade=t=out:st={need - 0.8}:d=0.8[o]"
    dst = os.path.join(OUT, slug(name) + ".wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", filt, "-map", "[o]", "-ar", "48000", dst], check=True)
    total = sum(b - a for _, r in it["src"] for a, b in r)
    manifest[name] = {"sig": "whistled2|" + name, "credits": [it["credit"]], "captions": [{"t": t, "d": d, "text": s} for t, d, s in it["captions"]], "ranges": [r for _, rs in it["src"] for r in rs]}
    lines.append(f"{name}: {it['credit']['title']}, {it['credit']['license']}, {it['credit']['page']}")
    print(name, f"whistle {total:.1f}s in a {need}s segment")
json.dump(manifest, open(os.path.join(OUT, "manifest.json"), "w"), indent=1, ensure_ascii=False)
open(os.path.join(HERE, "out", "whistled2_credits.txt"), "w").write("\n".join(lines) + "\n")

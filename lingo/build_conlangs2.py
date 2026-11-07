# Audio for "People Actually Speak These Made-Up Languages (Part 2)": python3 build_conlangs2.py
# Sources are Commons mp3 transcodes in cache/conlangs2/src (the originals are throttled). Speech clips are cut from
# `start` for the length of the segment and loudness-matched; Láadan is a sequence of single-word Lingua Libre
# recordings (captioned on screen). Writes cache/audio/conlangs2/<slug>.wav, manifest.json and out/conlangs2_credits.txt.
import json, os, subprocess, urllib.parse
import fetch_audio as fa

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "cache", "conlangs2", "src")
OUT = os.path.join(HERE, "cache", "audio", "conlangs2")
os.makedirs(OUT, exist_ok=True)
NEED = round(1.4 + 5.0 * 3 + 1.2, 2)  # story segment with 3 cards
LDN_WORDS = ["Láadan", "osháana", "héeya", "lóolo", "shebasheb", "ramíili", "dóhin", "híya", "rahen", "mime"]
CLIPS = {  # name: (source file, start, title, author, licence)
    "Interlingua": ("interlingua_yt.m4a", 8.0, "Populo (People) - article from the Interlingua Wikipedia", "mithradates", "used with permission"),
    "Lingua Franca Nova": ("lfn2.mp3", 0.0, "Introdui1.ogg", "lingua-franca-nova.net", "GFDL, CC BY-SA 3.0"),
    "Uropi": ("uropi.mp3", 0.0, "PontMirabo3.ogg", "Joël Landais, creator of Uropi", "public domain"),
}
YOUTUBE = {"Interlingua": "https://www.youtube.com/watch?v=tGCdGSX5fBc"}  # owner got permission from the uploader
page = lambda t: "https://commons.wikimedia.org/wiki/" + urllib.parse.quote("File:" + t.replace(" ", "_"))
manifest, lines = {}, ["Audio credits (People Actually Speak These Made-Up Languages, Part 2)", ""]
for name, (f, start, title, author, lic) in CLIPS.items():
    src = os.path.join(SRC, f)
    if not os.path.exists(src):
        print(name, "missing", f); manifest[name] = None; continue
    dst = os.path.join(OUT, fa.slug(name) + ".wav")
    fa.to_wav(src, dst, start, NEED, extra=f"afade=t=in:d=0.3,afade=t=out:st={NEED - 0.8}:d=0.8,loudnorm=I=-18:TP=-2")
    yt = YOUTUBE.get(name)
    link = yt or page(title)
    manifest[name] = {"sig": "conlangs2|" + name, "credits": [{"title": title if yt else "File:" + title, "artist": author, "license": lic, "page": link}], "captions": [], "start": start}
    lines.append(f'{name}: "{title}" by {author}, {lic}, ' + (f"{link}" if yt else f"via Wikimedia Commons, {link}"))
    print(name, NEED, "s from", start)
# Láadan: single-word recordings one after another, captioned (like Klingon and Volapük in Part 1)
SEQS = {
    "Láadan": ([(f"ldn_{w}.mp3", w, f"LL-Q35757 (ldn)-Arlo Barnes-{w}.wav", "Arlo Barnes (Lingua Libre)", "CC0") for w in LDN_WORDS], 1),
}
for name, (words, repeat) in SEQS.items():
    parts, caps, credits, t = [], [], {}, 0.6
    for f, w, title, author, lic in words * repeat:
        src = os.path.join(SRC, f)
        if not os.path.exists(src):
            continue
        p = os.path.join(OUT, f"{fa.slug(name)}_{len(parts)}.wav")
        fa.to_wav(src, p, extra="silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,loudnorm=I=-18:TP=-2")
        d = fa.duration(p)
        if t + d > NEED - 0.4:
            break
        caps.append({"t": round(t, 2), "d": round(d, 2), "text": w}); parts.append((t, p)); t += d + 0.9
        credits[title] = {"title": "File:" + title, "artist": author, "license": lic, "page": page(title)}
    dst = os.path.join(OUT, fa.slug(name) + ".wav")
    ins, filt = [], []
    for i, (st, p) in enumerate(parts):
        ins += ["-i", p]; filt.append(f"[{i}]adelay={int(st * 1000)}|{int(st * 1000)}[a{i}]")
    filt.append("".join(f"[a{i}]" for i in range(len(parts))) + f"amix=inputs={len(parts)}:normalize=0,apad,atrim=0:{NEED}[o]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(filt), "-map", "[o]", "-ar", str(fa.SR), dst], check=True)
    manifest[name] = {"sig": "conlangs2|" + name, "credits": list(credits.values()), "captions": caps}
    for c in credits.values():
        lines.append(f'{name}: "{c["title"][5:]}" by {c["artist"]}, {c["license"]}, via Wikimedia Commons, {c["page"]}')
    print(name, len(caps), "words")
json.dump(manifest, open(os.path.join(OUT, "manifest.json"), "w"), indent=1, ensure_ascii=False)
open(os.path.join(HERE, "out", "conlangs2_credits.txt"), "w").write("\n".join(lines) + "\n")

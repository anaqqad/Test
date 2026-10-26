# Audio for "People Actually Speak These Made-Up Languages (Part 3)": python3 build_conlangs3.py
# Sources in cache/conlangs3/src: a subscriber's song (used with permission), Creative Commons (CC BY) YouTube videos
# downloaded by the owner, and Commons word recordings. Speech clips are cut from `start` for the length of the segment
# and loudness-matched; Solresol is a sequence of single-word recordings (captioned on screen).
# Writes cache/audio/conlangs3/<slug>.wav, manifest.json and out/conlangs3_credits.txt.
import json, os, subprocess, urllib.parse
import fetch_audio as fa

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "cache", "conlangs3", "src")
OUT = os.path.join(HERE, "cache", "audio", "conlangs3")
os.makedirs(OUT, exist_ok=True)
NEED = round(1.4 + 5.0 * 3 + 1.2, 2)  # story segment with 3 cards
CLIPS = {  # name: (source file, start, title, author, licence)
    "Kunyotóri'an": ("kunyotorian_catlover82.mp3", 0.8, "Song about eight cats in Modern Latin Kunyotóri'an", "catlover82 (@orion_cat823)", "used with permission"),
    "Occidental": ("occidental_paulineauster.weba", 1.6, "Dorlota parla Interlingue-Occidental - Dorlota speaks Interlingue-Occidental", "Pauline Auster", "CC BY"),
    "Interslavic": ("interslavic_thecandle.m4a", 87.0, "Interslavic language", "The candle", "CC BY"),
    "Kotava": ("kotava_lucekotavusik.m4a", 0.7, "Inde Va Kotava Al Ravé", "Luce kotavusik", "CC BY"),
    "Pandunia": ("pandunia_ristokupsala.m4a", 2.3, "mi salama dunia", "Risto Kupsala", "CC BY"),
}
YOUTUBE = {"Occidental": "https://www.youtube.com/watch?v=0IdbAmu4Mek", "Interslavic": "https://www.youtube.com/watch?v=topy2bN0Um8",
           "Kotava": "https://www.youtube.com/watch?v=8PZOHH6YHPA", "Pandunia": "https://www.youtube.com/watch?v=TgO8AwX4OCU",
           }
page = lambda t: "https://commons.wikimedia.org/wiki/" + urllib.parse.quote("File:" + t.replace(" ", "_"))
manifest, lines = {}, ["Audio credits (People Actually Speak These Made-Up Languages, Part 3)", ""]
for name, (f, start, title, author, lic) in CLIPS.items():
    src = os.path.join(SRC, f)
    if not os.path.exists(src):
        print(name, "missing", f); manifest[name] = None; continue
    dst = os.path.join(OUT, fa.slug(name) + ".wav")
    fa.to_wav(src, dst, start, NEED, extra=f"afade=t=in:d=0.3,afade=t=out:st={NEED - 0.8}:d=0.8,loudnorm=I=-18:TP=-2")
    yt = YOUTUBE.get(name)
    link = yt or page(title)
    manifest[name] = {"sig": "conlangs3|" + name, "credits": [{"title": title if yt else "File:" + title, "artist": author, "license": lic, "page": link}], "captions": [], "start": start}
    if name == "Kunyotóri'an":
        manifest[name]["credits"] = [{"title": title, "artist": author, "license": lic, "page": ""}]
        lines.append(f"{name}: audio sample and song in Modern Latin Kunyotóri'an shared by {author}, {lic}")
    else:
        lines.append(f'{name}: "{title}" by {author}, {lic} (Creative Commons Attribution), YouTube, {link}')
    print(name, NEED, "s from", start)
# Solresol: single-word recordings one after another, captioned (like Láadan in Part 2)
SOL = [("sol_Solresolsolresolwav", "solresol"), ("sol_Siredorewav", "siredore"), ("sol_Solsolwav", "solsol"), ("sol_Sisidorewav", "sisidore"),
       ("sol_Solsiwav", "solsi"), ("sol_Sollasilawav", "sollasila"), ("sol_Solsowav", "sol"), ("sol_Sisisswav", "sisi")]
SOL_TITLE = {"sol_Solresolsolresolwav": "Solresol (solresol).wav", "sol_Siredorewav": "Siredore.wav", "sol_Solsolwav": "Solsol.wav", "sol_Sisidorewav": "Sisidore.wav",
             "sol_Solsiwav": "Solsi.wav", "sol_Sollasilawav": "Sollasila.wav", "sol_Solsowav": "Sol (so).wav", "sol_Sisisswav": "Sisi (ss).wav"}
def isaudio(p):
    p = os.path.join(SRC, p)
    return os.path.exists(p) and (open(p, "rb").read(4)[:3] in (b"RIF", b"ID3") or open(p, "rb").read(1) == b"\xff")
def solfile(stem):  # the .wav original if it downloaded, else the Commons mp3 transcode
    for ext in (".wav", ".mp3"):
        p = os.path.join(SRC, stem + ext)
        if os.path.exists(p) and open(p, "rb").read(4)[:3] in (b"RIF", b"ID3") or (os.path.exists(p) and open(p, "rb").read(1) == b"\xff"):
            return stem + ext
    return stem + ".wav"
SEQS = {
    "Solresol": ([(solfile(f), w, SOL_TITLE[f], "Luce Vergneaux (Kotavusik)", "CC BY-SA 4.0") for f, w in SOL if isaudio(solfile(f))], 2),
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
    manifest[name] = {"sig": "conlangs3|" + name, "credits": list(credits.values()), "captions": caps}
    for c in credits.values():
        lines.append(f'{name}: "{c["title"][5:]}" by {c["artist"]}, {c["license"]}, via Wikimedia Commons, {c["page"]}')
    print(name, len(caps), "words")
json.dump(manifest, open(os.path.join(OUT, "manifest.json"), "w"), indent=1, ensure_ascii=False)
open(os.path.join(HERE, "out", "conlangs3_credits.txt"), "w").write("\n".join(lines) + "\n")

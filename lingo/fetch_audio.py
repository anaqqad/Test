"""Download free-licensed language recordings from Wikimedia Commons and cut one clip per segment.

  python3 fetch_audio.py [video ...]      -> cache/audio/<video>/<i>.wav + cache/audio/<video>/manifest.json

Sources are Wikitongues donations, Lingua Libre word recordings and other Commons files (CC0 / CC BY / CC BY-SA /
public domain). Each clip's author and licence go into the manifest and into out/<video>_credits.txt, which must be
pasted into the YouTube description (CC BY / BY-SA require attribution).
"""
import json, os, random, re, subprocess, sys, time, html, urllib.error, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "cache")
UA = {"User-Agent": "LingoDudeVideoBot/0.1 (educational videos; https://github.com/anaqqad/Test)"}
SR = 48000


def api(**p):
    p["format"] = "json"
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(p)
    for i in range(6):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60))
        except Exception as e:
            time.sleep(3 * (i + 1))
    raise RuntimeError("API failed: " + url)


def info(title):
    title = title if title.startswith("File:") else "File:" + title
    d = api(action="query", titles=title, prop="imageinfo|videoinfo", iiprop="url|extmetadata|size|mediatype", viprop="derivatives")
    page = list(d["query"]["pages"].values())[0]
    if "imageinfo" not in page:
        return None
    ii = page["imageinfo"][0]
    # videos: download the smallest transcode (we only need the soundtrack), not the HD original
    ders = [x for x in (page.get("videoinfo") or [{}])[0].get("derivatives", []) if "webm" in x.get("type", "") and x.get("bandwidth")]
    if title.lower().endswith(".webm") and ders:
        ii["url"] = min(ders, key=lambda x: x["bandwidth"])["src"]
    md = ii.get("extmetadata", {})
    strip = lambda s: re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s or ""))).strip()
    return {
        "title": page["title"], "url": ii["url"], "size": ii.get("size", 0),
        "artist": strip(md.get("Artist", {}).get("value", "")) or "unknown",
        "license": strip(md.get("LicenseShortName", {}).get("value", "")),
        "page": "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(page["title"].replace(" ", "_")),
    }


def search_title(q):
    d = api(action="query", list="search", srsearch=q, srnamespace=6, srlimit=5)
    hits = d["query"]["search"]
    return hits[0]["title"] if hits else None


def download(meta):
    os.makedirs(os.path.join(CACHE, "raw"), exist_ok=True)
    ext = os.path.splitext(urllib.parse.urlparse(meta["url"]).path)[1]
    path = os.path.join(CACHE, "raw", re.sub(r"[^\w.-]", "_", meta["title"][5:])[:80] + ext)
    if not os.path.exists(path):
        for i in range(8):
            try:
                with urllib.request.urlopen(urllib.request.Request(meta["url"], headers=UA), timeout=300) as r, open(path + ".part", "wb") as f:
                    while chunk := r.read(1 << 20):
                        f.write(chunk)
                os.replace(path + ".part", path)
                break
            except urllib.error.HTTPError as e:
                wait = int(e.headers.get("Retry-After") or 0) or 60 * (i + 1)
                print(f"    HTTP {e.code}, waiting {wait}s")
                time.sleep(wait)
            except Exception:
                time.sleep(10 * (i + 1))
        else:
            raise RuntimeError("download failed: " + meta["url"])
        time.sleep(8)
    return path


def to_wav(src, dst, start=0.0, dur=None, extra=""):
    cmd = ["ffmpeg", "-v", "error", "-y", "-ss", str(start), "-i", src]
    if dur:
        cmd += ["-t", str(dur)]
    af = "aresample=48000,pan=stereo|c0=c0|c1=c0" + ("," + extra if extra else "")
    subprocess.run(cmd + ["-vn", "-af", af, "-ar", str(SR), dst], check=True)


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path], capture_output=True, text=True).stdout
    return float(out.strip() or 0)


_model = None


def slug(name):
    return re.sub(r"[^\w]+", "_", name).strip("_").lower()


def pick_start(path, need, avoid=("en",)):
    """Start of the `need`-second stretch that Whisper finds least likely to be in an `avoid` language (English intros,
    or e.g. Malay for a Kensiu speaker who also speaks Malay). Silence counts as bad too."""
    global _model
    from faster_whisper import WhisperModel
    import numpy as np
    if _model is None:
        _model = WhisperModel("base", device="cpu", compute_type="int8")
    total = duration(path)
    tmp = os.path.join(CACHE, "probe.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", path, "-t", "600", "-vn", "-ac", "1", "-ar", "16000", tmp], check=True)
    audio = np.frombuffer(open(tmp, "rb").read()[44:], dtype=np.int16).astype(np.float32) / 32768
    step, win = 5, 10
    scores = []
    for t in range(0, max(1, int(min(total, 600) - win)), step):
        seg = audio[t * 16000:(t + win) * 16000]
        if len(seg) < 16000 or np.sqrt((seg ** 2).mean()) < 0.01:
            scores.append((t, 1.0, "silence"))
            continue
        lang, prob, allp = _model.detect_language(seg)
        bad = sum(p for l, p in allp if l in avoid)
        scores.append((t, bad, lang))
    k = max(1, int(round((need - win) / step)) + 1)
    best = min(range(max(1, len(scores) - k + 1)), key=lambda i: (sum(x[1] for x in scores[i:i + k]) / len(scores[i:i + k]), scores[i][0]))
    run = scores[best:best + k]
    print(f"    auto start {run[0][0]}s, avoid={','.join(avoid)} score={sum(x[1] for x in run) / len(run):.2f} ({', '.join(x[2] for x in run)})")
    return run[0][0]


def seg_duration(video, item):
    n = len(item["cards"])
    return 11.0 if video["layout"] == "ranking" else round(1.4 + 5.0 * n + 1.2, 2)


def build_sequence(metas, dst, need, repeat=1, gap=0.55):
    parts, caps, t = [], [], 0.6
    metas = metas * repeat
    tmpdir = os.path.join(CACHE, "seq")
    os.makedirs(tmpdir, exist_ok=True)
    for i, m in enumerate(metas):
        p = os.path.join(tmpdir, f"{i}.wav")
        to_wav(download(m), p, extra="silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse")
        d = duration(p)
        if t + d > need - 0.4:
            break
        word = re.sub(r"\.\w+$", "", m["title"][5:])
        word = word.split("-")[-1] if word.startswith("LL-") else word
        caps.append({"t": round(t, 2), "d": round(d, 2), "text": word})
        parts.append((t, p))
        t += d + gap
    inputs, filt = [], []
    for i, (st, p) in enumerate(parts):
        inputs += ["-i", p]
        filt.append(f"[{i}]adelay={int(st * 1000)}|{int(st * 1000)}[a{i}]")
    mixin = "".join(f"[a{i}]" for i in range(len(parts)))
    filt.append(f"{mixin}amix=inputs={len(parts)}:normalize=0,apad,atrim=0:{need}[out]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(filt), "-map", "[out]", "-ar", str(SR), dst], check=True)
    return caps


def ll_titles(code):
    titles, cont = [], {}
    while True:
        d = api(action="query", list="categorymembers", cmtitle=f"Category:Lingua Libre pronunciation-{code}", cmlimit=500, cmtype="file", **cont)
        titles += [m["title"] for m in d["query"]["categorymembers"]]
        if "continue" not in d or len(titles) >= 3000:
            return titles
        cont = {"cmcontinue": d["continue"]["cmcontinue"]}


def process(vkey, video):
    outdir = os.path.join(CACHE, "audio", vkey)
    os.makedirs(outdir, exist_ok=True)
    manifest_path = os.path.join(outdir, "manifest.json")
    manifest = json.load(open(manifest_path)) if os.path.exists(manifest_path) else {}
    for i, item in enumerate(video["items"]):
        a, need, key = item.get("audio"), seg_duration(video, item), item["name"]
        if not a:
            manifest[key] = None
            continue
        sig = json.dumps(a, sort_keys=True, ensure_ascii=False) + f"|{need}"
        dst = os.path.join(outdir, slug(item["name"]) + ".wav")
        if manifest.get(key, {}) and manifest[key].get("sig") == sig and os.path.exists(dst):
            continue
        print(f"[{vkey}] {item['name']}")
        try:
            if "file" in a:
                m = info(a["file"]) or (a.get("search") and info(search_title(a["search"]) or ""))
                if not m:
                    raise RuntimeError("not found: " + a["file"])
                src = download(m)
                if a.get("ranges"):  # only the stretches in the language itself (skip spoken translations)
                    parts = "".join(f"[0]atrim={x}:{y},asetpts=PTS-STARTPTS,apad=pad_dur=0.5[p{k}];" for k, (x, y) in enumerate(a["ranges"]))
                    cat = "".join(f"[p{k}]" for k in range(len(a["ranges"]))) + f"concat=n={len(a['ranges'])}:v=0:a=1,aresample=48000,pan=stereo|c0=c0|c1=c0,apad,atrim=0:{need},afade=t=out:st={need - 0.8}:d=0.8,loudnorm=I=-18:TP=-2[o]"
                    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-filter_complex", parts + cat, "-map", "[o]", "-ar", str(SR), dst], check=True)
                    manifest[key] = {"sig": sig, "credits": [m], "captions": [], "ranges": a["ranges"]}
                    json.dump(manifest, open(manifest_path, "w"), indent=1, ensure_ascii=False)
                    continue
                start = pick_start(src, need, tuple(a.get("avoid", ["en"]))) if a.get("start") == "auto" else float(a.get("start", 0))
                to_wav(src, dst, start, need, extra=f"afade=t=in:d=0.4,afade=t=out:st={need - 0.8}:d=0.8,loudnorm=I=-18:TP=-2")
                manifest[key] = {"sig": sig, "credits": [m], "captions": [], "start": start}
            else:
                if "ll" in a:
                    titles = ll_titles(a["ll"])
                    want = a.get("words")
                    chosen = []
                    if want:
                        for w in want:
                            hit = [t for t in titles if t.rsplit("-", 1)[-1].rsplit(".", 1)[0].lower() == w.lower()]
                            if hit:
                                chosen.append(hit[0])
                    rnd = random.Random(item["name"])
                    pool = [t for t in titles if len(t.rsplit("-", 1)[-1]) < 18 and not re.search(r"\d", t.rsplit("-", 1)[-1])]
                    while len(chosen) < a.get("n", 6) and pool:
                        chosen.append(pool.pop(rnd.randrange(len(pool))))
                    titles = chosen
                else:
                    titles = a["seq"]
                metas = [m for m in (info(t) for t in titles) if m]
                caps = build_sequence(metas, dst, need, a.get("repeat", 1))
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", dst, "-af", "loudnorm=I=-18:TP=-2", "-ar", str(SR), dst + ".n.wav"], check=True)
                os.replace(dst + ".n.wav", dst)
                used = {c["text"] for c in caps}
                manifest[key] = {"sig": sig, "credits": [m for m in metas if any(m["title"][5:].startswith(u) or u in m["title"] for u in used)], "captions": caps}
        except Exception as e:
            print("   !! audio failed:", e)
            manifest[key] = None
        json.dump(manifest, open(manifest_path, "w"), indent=1, ensure_ascii=False)
    # credits file
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    lines = [f"Audio credits ({video['title']} {video.get('part', '')})", ""]
    for i, item in enumerate(video["items"]):
        e = manifest.get(item["name"])
        for c in (e or {}).get("credits", []):
            lines.append(f"{item['name']}: \"{c['title'][5:]}\" by {c['artist']}, {c['license']}, via Wikimedia Commons, {c['page']}")
    open(os.path.join(HERE, "out", f"{vkey}_credits.txt"), "w").write("\n".join(lines) + "\n")


if __name__ == "__main__":
    videos = json.loads(subprocess.run(["node", "-e", "import('./videos.mjs').then(m=>console.log(JSON.stringify(m.VIDEOS)))"], cwd=HERE, capture_output=True, text=True, check=True).stdout)
    for k in sys.argv[1:] or videos:
        process(k, videos[k])

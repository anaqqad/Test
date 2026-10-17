# Audio for the "most similar languages" video: python3 fetch_pairs.py [pair ...]
# For each pair, each test word is played in language A then language B (real Lingua Libre recordings from Wikimedia
# Commons, one speaker per language where possible). Writes cache/audio/similar/<pair>.wav, manifest.json (captions with
# the side that is speaking, credits) and out/similar_credits.txt. Word lists: similar_pairs.json; found recordings:
# cache/similar_found.json (from the scratchpad search, copied here so the build is reproducible).
import json, os, re, subprocess, sys
import fetch_audio as fa

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "cache", "audio", "similar")
os.makedirs(OUT, exist_ok=True)
PAIRS = json.load(open(os.path.join(HERE, "similar_pairs.json")))
FOUND = json.load(open(os.path.join(HERE, "cache", "similar_found.json")))
GAP_AB, GAP_WORDS, LEAD = 0.45, 1.0, 0.8
SR = fa.SR


def speaker(title):
    m = re.match(r"^File:LL-Q\d+ \(\w+\)-([^-]+)-", title)
    return m.group(1) if m else ""


def choose(code, words):
    """one recording per word, preferring the speaker who recorded the most of this pair's words"""
    hits = {w: FOUND.get(f"{code}|{w}", []) for w in words}
    count = {}
    for w, ts in hits.items():
        for t in ts:
            count[speaker(t)] = count.get(speaker(t), 0) + 1
    order = sorted(count, key=lambda s: -count[s])
    picked = {}
    for w, ts in hits.items():
        for s in order:
            t = next((x for x in ts if speaker(x) == s), None)
            if t:
                picked[w] = t
                break
    return picked


def ll_meta(title):
    """Lingua Libre files need no API call: always CC BY-SA 4.0, speaker in the name, URL from the md5 path."""
    import hashlib, urllib.parse
    name = title[5:].replace(" ", "_")
    h = hashlib.md5(name.encode()).hexdigest()
    q = urllib.parse.quote(name)  # the transcoded mp3 is served without the throttling the originals get
    return {"title": title, "url": f"https://upload.wikimedia.org/wikipedia/commons/transcoded/{h[0]}/{h[:2]}/{q}/{q}.mp3",
            "url_orig": f"https://upload.wikimedia.org/wikipedia/commons/{h[0]}/{h[:2]}/{q}",
            "artist": speaker(title) + " (Lingua Libre)", "license": "CC BY-SA 4.0",
            "page": "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_"))}


def fetch(m):
    """curl with our user agent; Commons throttles bursts, so pace the requests and back off on 429"""
    import time
    os.makedirs(os.path.join(fa.CACHE, "raw"), exist_ok=True)
    path = os.path.join(fa.CACHE, "raw", re.sub(r"[^\w.-]", "_", m["title"][5:])[:80] + ".mp3")
    if os.path.exists(path) and os.path.getsize(path) > 500:
        return path
    hdr = os.path.join(fa.CACHE, "raw", "_hdr.txt")
    # the mp3 transcode answers 429 + "retry-after: 10" while Commons generates it, then 200; the originals
    # answer 429 + "retry-after: 600", so they are only tried once, at the very end
    for i in range(26):
        url = m["url"] if i < 25 else m["url_orig"]
        r = subprocess.run(["curl", "-s", "-D", hdr, "-w", "%{http_code}", "-A", fa.UA["User-Agent"], "-o", path, url], capture_output=True, text=True)
        if r.stdout == "200" and os.path.getsize(path) > 500 and fa.duration(path) > 0.05:
            time.sleep(3)
            return path
        if os.path.exists(path):
            os.remove(path)  # an error page or a truncated file
        ra = re.search(r"(?im)^retry-after:\s*(\d+)", open(hdr).read() if os.path.exists(hdr) else "")
        wait = min(120, int(ra.group(1)) + 2) if ra else 15
        print(f"    HTTP {r.stdout}, waiting {wait}s", flush=True)
        time.sleep(wait)
    return None


def clip(title, dst):
    m = ll_meta(title)
    src = fetch(m)
    if not src:
        return None
    try:
        fa.to_wav(src, dst, extra="silenceremove=start_periods=1:start_threshold=-42dB,areverse,silenceremove=start_periods=1:start_threshold=-42dB,areverse,loudnorm=I=-18:TP=-2")
    except subprocess.CalledProcessError:
        print("    unreadable file, skipped:", title, flush=True)
        return None
    return m


def build(pk, p):
    words = p["words"]
    pa, pb = choose(p["a"], [w[0] for w in words]), choose(p["b"], [w[1] for w in words])
    parts, caps, credits, t = [], [], [], LEAD
    tmp = os.path.join(fa.CACHE, "seq_pairs")
    os.makedirs(tmp, exist_ok=True)
    for i, (wa, wb, same) in enumerate(words):
        if wa not in pa or wb not in pb:
            print(f"  skip {wa}/{wb}: no recording")
            continue
        row = {"a": wa, "b": wb, "same": same, "t": round(t, 2)}
        for side, title in (("a", pa[wa]), ("b", pb[wb])):
            dst = os.path.join(tmp, f"{pk}_{i}_{side}.wav")
            m = clip(title, dst)
            if not m:
                print("  missing", title)
                continue
            d = fa.duration(dst)
            caps.append({"side": side, "t": round(t, 2), "d": round(d, 2), "text": wa if side == "a" else wb, "i": len([r for r in parts if r[2] == "row"])})
            parts.append((t, dst, "clip"))
            credits.append(m)
            t += d + (GAP_AB if side == "a" else 0)
        parts.append((t, None, "row"))
        row["end"] = round(t, 2)
        t += GAP_WORDS
    clips = [(st, pth) for st, pth, k in parts if k == "clip"]
    ins, filt = [], []
    for i, (st, pth) in enumerate(clips):
        ins += ["-i", pth]
        filt.append(f"[{i}]adelay={int(st * 1000)}|{int(st * 1000)}[a{i}]")
    total = t + 0.5
    filt.append("".join(f"[a{i}]" for i in range(len(clips))) + f"amix=inputs={len(clips)}:normalize=0,apad,atrim=0:{total:.2f}[out]")
    dst = os.path.join(OUT, pk + ".wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(filt), "-map", "[out]", "-ar", str(SR), dst], check=True)
    # fix the row index on captions (row = word pair number among the ones that were found)
    k, last = -1, None
    for c in caps:
        if c["text"] != last or c["side"] == "a":
            if c["side"] == "a":
                k += 1
        c["i"] = k
        last = c["text"]
    seen, uniq = set(), []
    for m in credits:
        if m["title"] not in seen:
            seen.add(m["title"]); uniq.append(m)
    return {"captions": caps, "credits": uniq, "len": round(total, 2), "words": [{"a": wa, "b": wb, "same": s} for wa, wb, s in words if wa in pa and wb in pb]}


if __name__ == "__main__":
    mpath = os.path.join(OUT, "manifest.json")
    manifest = json.load(open(mpath)) if os.path.exists(mpath) else {}
    for pk in sys.argv[1:] or PAIRS:
        print(f"[{pk}]")
        try:
            manifest[pk] = build(pk, PAIRS[pk])
            print(f"  {len(manifest[pk]['words'])} word pairs, {manifest[pk]['len']}s")
        except Exception as e:
            print("  !! failed:", e)
        json.dump(manifest, open(mpath, "w"), indent=1, ensure_ascii=False)
    lines = ["Audio credits (Languages That Are Basically the Same)", ""]
    for pk, e in manifest.items():
        for c in e.get("credits", []):
            lines.append(f"{pk}: \"{c['title'][5:]}\" by {c['artist']}, {c['license']}, via Wikimedia Commons, {c['page']}")
    open(os.path.join(HERE, "out", "similar_credits.txt"), "w").write("\n".join(lines) + "\n")

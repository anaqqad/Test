"""Download the best-quality archive.org copy of each film into assets/footage/<out>.mp4 (owner's rule: never the 512kb copy).
Small h.264 copies are downloaded as they are; big masters (MPEG2, 720p/1080p .mov/.mp4) are downloaded (8 parallel byte
ranges), re-encoded to a compact progressive h.264 (deinterlaced, at most 1280 wide), and the master is deleted. Usage: python tools/fetch_footage.py [out ...]"""
import json, subprocess, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets/footage"; OUT.mkdir(parents=True, exist_ok=True)
# identifier | file name (prefix) | out | mode: copy or encode
FILMS = """111-OF-51|111-OF-51.mp4|negro_soldier_1944|copy
111-of-14-r1|111-of-14-r1.mp4|teamwork_1946|copy
111-adc-8872|111-adc-8872.mp4|seattle_poe_1951|copy
gov.archives.arc.23655|gov.archives.arc.23655.mpeg|tunisian_campaign_1943|encode
gov.fdr.273|gov.fdr.273.mpeg|fdr_tour_1942|encode
1945-06-25_President_on_Tour|1945-06-25_President_on_Tour.mpeg|president_tour_1945|encode
1945-05-31_US_War_Dead_Honored_On_Memorial_Day|1945-05-31_US_War_Dead_Honored_On_Memorial_Day.mp4|memorial_day_1945|copy"""

UA = "WWIIFrontlinesResearch/1.0"


def download(url, path, parts=8):
    """archive.org sometimes serves one connection at ~1 MB/s; 8 byte ranges in parallel are many times faster."""
    head = subprocess.run(["curl", "-sIL", "-A", UA, url], capture_output=True, text=True).stdout
    size = int([l.split(":")[1] for l in head.lower().splitlines() if l.startswith("content-length")][-1])
    step = -(-size // parts)
    chunks = [path.with_suffix(f".r{i}") for i in range(parts)]
    procs = [subprocess.Popen(["curl", "-sSL", "--retry", "8", "-A", UA, "-r", f"{i * step}-{min(size, (i + 1) * step) - 1}", "-o", str(c), url])
             for i, c in enumerate(chunks)]
    if any(p.wait() for p in procs):
        raise SystemExit(f"download failed: {url}")
    with open(path, "wb") as out:
        for c in chunks:
            out.write(c.read_bytes()); c.unlink()
    if path.stat().st_size != size:
        raise SystemExit(f"size mismatch: {path}")


want = set(sys.argv[1:])
for line in FILMS.splitlines():
    ident, name, out, mode = line.split("|")
    dst = OUT / f"{out}.mp4"
    if (want and out not in want) or (dst.exists() and dst.stat().st_size > 1e6):
        continue
    files = json.load(urllib.request.urlopen(f"https://archive.org/metadata/{ident}/files", timeout=60))["result"]
    name = next(f["name"] for f in files if f["name"].startswith(name))
    url = f"https://archive.org/download/{ident}/{urllib.request.quote(name)}"
    tmp = dst.with_suffix(".part.mp4")
    print(f"{out}: {mode} {name}", flush=True)
    if mode == "copy":
        download(url, tmp)
    else:
        src = dst.with_suffix(".src" + Path(name).suffix)  # download first: streaming the master through ffmpeg crawled
        download(url, src)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-an",
                        "-vf", "bwdif=mode=send_frame:deint=interlaced,scale='min(1280,iw)':-2",
                        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p", str(tmp)], check=True)
        src.unlink()
    if tmp.stat().st_size < 1e6:  # a dropped stream can end "successfully" with an empty file
        tmp.unlink(); print("  failed, run again"); continue
    tmp.replace(dst)
    print(f"  -> {dst.stat().st_size / 1e6:.0f} MB", flush=True)

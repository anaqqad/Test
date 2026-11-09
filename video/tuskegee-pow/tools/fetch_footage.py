"""Download the best-quality archive.org copy of each film into assets/footage/<out>.mp4 (owner's rule: never the 512kb copy).
Small h.264 copies are downloaded as they are; big masters (MPEG2, 720p/1080p .mov/.mp4) are downloaded (8 parallel byte
ranges), re-encoded to a compact progressive h.264 (deinterlaced, at most 1280 wide), and the master is deleted. Usage: python tools/fetch_footage.py [out ...]"""
import json, subprocess, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets/footage"; OUT.mkdir(parents=True, exist_ok=True)
# identifier | file name (prefix) | out | mode: copy or encode
FILMS = """342-sfp-151_HD_2Mbps|342-sfp-151_HD_2Mbps.mp4|wings_1945|copy
RedTails19440910|Red Tails - Awards To 332nd Fighter Group|red_tails_1944|copy
111-adc-9839|111-adc-9839.mp4|queen_mary_1945|copy
111-adc-4198|111-adc-4198.mp4|moosburg_1945|copy
CB-17|CB-17 Combat Bulletin 17|combat_bulletin_17|copy
ADC-4009|ADC-4009.mov|prisoners_freed_1945|encode
ADC-4544b|ADC-4544b.mov|dachau_services_1945|encode
80052ADayWithTheA36s|80052 A Day With The A-36's.mov|a36_day|encode
TF13384TargetForToday1944|TF 1-3384 Target For Today 1944.mp4|target_today_1944|copy
NegroCol1944|NegroCol1944.mpeg|negro_colleges_1944|encode
fc-fc-965a-b|fc-fc-965a-b.mp4|detroit_1935|copy"""

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

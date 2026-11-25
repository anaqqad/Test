"""Download the best-quality archive.org copy of each film into assets/footage/<out>.mp4 (owner's rule: never the 512kb copy).
Small h.264 copies are downloaded as they are; big masters (MPEG2, 720p/1080p .mov/.mp4) are downloaded (8 parallel byte
ranges), re-encoded to a compact progressive h.264 (deinterlaced, at most 1280 wide), and the master is deleted. Usage: python tools/fetch_footage.py [out ...]"""
import json, subprocess, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets/footage"; OUT.mkdir(parents=True, exist_ok=True)
# identifier | file name (prefix) | out | mode: copy or encode
FILMS = """NPC-740|NPC-740|jpow_noumea_a|encode
NPC-738|NPC-738|jpow_noumea_b|encode
NPC-744|NPC-744|jpow_noumea_c|encode
428-npc-6897|428-npc-6897|jpow_saipan|encode
NPC-5315|NPC-5315|jpow_airman|encode
NPC-10134|NPC-10134|jp_newsreel42|encode
NPC-322|428-npc-322|jp_navy_review|encode
F06933|F06933|jp_radio_tokyo|encode
428-npc-8925|428-npc-8925|jpow_capture45|encode
111-of-10-r2|111-of-10-r2|know_enemy_r2|encode
ARC-38964|ARC-38964|au_veterans43|encode
OurEnemy1943|OurEnemy1943|our_enemy|encode"""

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


import shutil, time
def wait_space(gb=1.0):
    while shutil.disk_usage(ROOT).free < gb * 1e9:  # the PC's page file swings free space; wait instead of failing
        print(f"  waiting for disk space ({shutil.disk_usage(ROOT).free / 1e9:.1f} GB free)", flush=True); time.sleep(60)

want = set(sys.argv[1:])
for line in FILMS.splitlines():
    ident, name, out, mode = line.split("|")
    dst = OUT / f"{out}.mp4"
    if (want and out not in want) or (dst.exists() and dst.stat().st_size > 1e6):
        continue
    if ident.startswith("http"):  # direct file (NARA catalog, Wikimedia Commons)
        url = ident; name = Path(ident).name
    else:
        files = json.load(urllib.request.urlopen(f"https://archive.org/metadata/{ident}/files", timeout=60))["result"]
        cands = [f for f in files if f["name"].startswith(name) and "512kb" not in f["name"]
                 and f["name"].lower().endswith((".mov", ".mp4", ".mpeg", ".mpg", ".m4v", ".avi"))]
        name = max(cands, key=lambda f: int(f.get("size", 0)))["name"]  # best quality = biggest video file
        url = f"https://archive.org/download/{ident}/{urllib.request.quote(name)}"
    tmp = dst.with_suffix(".part.mp4")
    wait_space()
    print(f"{out}: {mode} {name}", flush=True)
    if mode == "copy":
        download(url, tmp, 1 if "wikimedia" in url else 8)
    else:
        src = dst.with_suffix(".src" + Path(name).suffix)  # download first: streaming the master through ffmpeg crawled
        if not (src.exists() and src.stat().st_size > 1e6):
            download(url, src, 1 if "wikimedia" in url else 8)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-c:a", "aac", "-b:a", "96k",
                        "-vf", "bwdif=mode=send_frame:deint=interlaced,scale='min(1280,iw)':-2",
                        "-c:v", "libx264", "-preset", "fast", "-crf", "21", "-pix_fmt", "yuv420p", str(tmp)], check=True)
        src.unlink()
    if tmp.stat().st_size < 1e6:  # a dropped stream can end "successfully" with an empty file
        tmp.unlink(); print("  failed, run again"); continue
    tmp.replace(dst)
    print(f"  -> {dst.stat().st_size / 1e6:.0f} MB", flush=True)

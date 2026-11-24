"""Download the best-quality archive.org copy of each film into assets/footage/<out>.mp4 (owner's rule: never the 512kb copy).
Small h.264 copies are downloaded as they are; big masters (MPEG2, 720p/1080p .mov/.mp4) are downloaded (8 parallel byte
ranges), re-encoded to a compact progressive h.264 (deinterlaced, at most 1280 wide), and the master is deleted. Usage: python tools/fetch_footage.py [out ...]"""
import json, subprocess, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets/footage"; OUT.mkdir(parents=True, exist_ok=True)
# identifier | file name (prefix) | out | mode: copy or encode
FILMS = """MN-9034G|MN-9034G|navy_victory_bulletin|encode
https://catalog.archives.gov/medialz/mopix/111/adc/111-adc-5163.mp4|x|mo_adc5163|encode
https://catalog.archives.gov/medialz/mopix/428/NPC/428-npc-14510.mp4|x|mo_14510|encode
JapaneseSignFinalSurrender1945|Japanese Sign Final Surrender|un_signing|encode
https://catalog.archives.gov/medialz/mopix/428/NPC/428-npc-14506.mp4|x|mo_14506|encode
428-npc-14518|428-npc-14518|mo_14518|encode
https://catalog.archives.gov/medialz/mopix/428/NPC/428-npc-14519.mp4|x|mo_14519|encode
https://catalog.archives.gov/medialz/mopix/428/NPC/428-npc-14513.mp4|x|mo_14513|encode
111-adc-9888|111-adc-9888|mo_adc9888|encode
gov.archives.arc.39078|gov.archives.arc.39078|un_landing|encode
TheArmy-NavyScreenMagazine68|Surrender In The Pacific|screen_mag68|encode
https://catalog.archives.gov/medialz/mopix/428/NPC/428-npc-14557.mp4|x|pow_rescue_tokyo|encode
ReleasedUSPrisonersOfWar|Cs-4554|pow_yokohama|encode
https://catalog.archives.gov/medialz/mopix/428/NPC/428-npc-14615.mp4|x|shinagawa_camp|encode
111-adc-5188|111-adc-5188|wainwright_manila|encode
111-adc-2992|111-adc-2992|atsugi_adc2992|encode
NPC-15471|428-npc-15471|white_bettys|encode
NPC-15559|NPC-15559|fleet_fuji|encode
CS-9405|CS-9405|atsugi_colour|encode
428-npc-15493|428-npc-15493|ashore_japan|encode"""

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

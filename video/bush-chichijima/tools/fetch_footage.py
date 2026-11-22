"""Download the best-quality archive.org copy of each film into assets/footage/<out>.mp4 (owner's rule: never the 512kb copy).
Small h.264 copies are downloaded as they are; big masters (MPEG2, 720p/1080p .mov/.mp4) are downloaded (8 parallel byte
ranges), re-encoded to a compact progressive h.264 (deinterlaced, at most 1280 wide), and the master is deleted. Usage: python tools/fetch_footage.py [out ...]"""
import json, subprocess, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets/footage"; OUT.mkdir(parents=True, exist_ok=True)
# identifier | file name (prefix) | out | mode: copy or encode
FILMS = """https://upload.wikimedia.org/wikipedia/commons/d/dd/George_Bush_Rescued_at_Sea_by_the_USS_Finback_-_02_September_1944.webm|x|finback_rescue_1944|encode
NPC-1521|NPC-1521.mov|san_jacinto_1944|encode
https://catalog.archives.gov/medialz/mopix/428/NPC/428-npc-7784.mp4|x|san_jacinto_attack_1945|encode
NPC-800|NPC-800.mov|independence_tbf_1943|encode
NPC-6523|NPC-6523.mov|independence_ops_1944|encode
428-npc-4369|428-npc-4369|tang_lifeguard_1944|encode
NPC-8646|NPC-8646.mov|aviator_rescue_1945|encode
428-npc-14153|428-npc-14153|tigrone_guam_1945|encode
https://catalog.archives.gov/medialz/mopix/428/NPC/428-npc-17059.mp4|x|chichi_surrender_a|encode
https://catalog.archives.gov/medialz/mopix/428/NPC/428-npc-17060.mp4|x|chichi_surrender_b|encode
https://catalog.archives.gov/medialz/mopix/428/NPC/428-npc-17062.mp4|x|chichi_surrender_c|encode
CS-2599|CS-2599.mov|chichi_b24_1944|encode
CS-3618|CS-3618.mov|chichi_b24_1945|encode
111-adc-1817|111-adc-1817|chichi_bombing_1944|encode
NPC-2658|NPC-2658.mov|fighting_lady_out_a|encode
NPC-2661|NPC-2661.mov|fighting_lady_out_b|encode
NPC-1469|NPC-1469.mov|kwajalein_strike_1944|encode
NPC-5074|NPC-5074.mov|wolverine_training_1943|encode
https://catalog.archives.gov/medialz/presidential-libraries/reagan/video-5730544/6-19-1986-667.mp4|x|bush_interview_1986|encode
https://upload.wikimedia.org/wikipedia/commons/e/e7/MT3897_-_President_Bush_is_Interviewed_Regarding_his_World_War_Two_Service_-_02_June_1992.webm|x|bush_stinnett_1992|encode
https://upload.wikimedia.org/wikipedia/commons/1/1e/MT3192_President_Bush_Discusses_His_World_War_Two_Experiences_During_an_Address_to_POW-MIA_Families.webm|x|bush_powmia_1992|encode"""

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

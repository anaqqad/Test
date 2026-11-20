"""Download the best-quality archive.org copy of each film into assets/footage/<out>.mp4 (owner's rule: never the 512kb copy).
Small h.264 copies are downloaded as they are; big masters (MPEG2, 720p/1080p .mov/.mp4) are downloaded (8 parallel byte
ranges), re-encoded to a compact progressive h.264 (deinterlaced, at most 1280 wide), and the master is deleted. Usage: python tools/fetch_footage.py [out ...]"""
import json, subprocess, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets/footage"; OUT.mkdir(parents=True, exist_ok=True)
# identifier | file name (prefix) | out | mode: copy or encode
FILMS = """RescuePrisonersLosBanos|CS-3274 Rescue Allied Prisoners Los Banos Luzon Philippine Islands.mp4|losbanos_rescue_1945|copy
111-adc-3487|111-adc-3487.mp4|losbanos_camp_feb1945|copy
111-adc-3616|111-adc-3616.mp4|losbanos_bilibid_1945|copy
111-adc-4629|111-adc-4629.mp4|airborne_jump_lipa_1945|copy
111-adc-3349|111-adc-3349.mp4|paratroop_corregidor_1945|copy
111-adc-3367|111-adc-3367.mp4|santo_tomas_internees_1945|copy
1945-03-01_Santo_Tomas_Prisoners_Liberated|1945-03-01_Santo_Tomas_Prisoners_Liberated.mpeg|santo_tomas_newsreel_1945|encode
20784PeopleOfPhilippinesPt1Mos|20784 People Of Philippines Pt1_mos.mov|philippines_travelogue_1940s|encode
InterviewingPhilippineInternees1945|Interviewing Philippine Internees 1945.mp4|internee_interviews_1945|copy

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
    files = json.load(urllib.request.urlopen(f"https://archive.org/metadata/{ident}/files", timeout=60))["result"]
    name = next(f["name"] for f in files if f["name"].startswith(name))
    url = f"https://archive.org/download/{ident}/{urllib.request.quote(name)}"
    tmp = dst.with_suffix(".part.mp4")
    wait_space()
    print(f"{out}: {mode} {name}", flush=True)
    if mode == "copy":
        download(url, tmp)
    else:
        src = dst.with_suffix(".src" + Path(name).suffix)  # download first: streaming the master through ffmpeg crawled
        if not (src.exists() and src.stat().st_size > 1e6):
            download(url, src)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-an",
                        "-vf", "bwdif=mode=send_frame:deint=interlaced,scale='min(1280,iw)':-2",
                        "-c:v", "libx264", "-preset", "fast", "-crf", "20", "-pix_fmt", "yuv420p", str(tmp)], check=True)
        src.unlink()
    if tmp.stat().st_size < 1e6:  # a dropped stream can end "successfully" with an empty file
        tmp.unlink(); print("  failed, run again"); continue
    tmp.replace(dst)
    print(f"  -> {dst.stat().st_size / 1e6:.0f} MB", flush=True)

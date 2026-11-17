"""Download the best-quality archive.org copy of each film into assets/footage/<out>.mp4 (owner's rule: never the 512kb copy).
Small h.264 copies are downloaded as they are; big masters (MPEG2, 720p/1080p .mov/.mp4) are downloaded (8 parallel byte
ranges), re-encoded to a compact progressive h.264 (deinterlaced, at most 1280 wide), and the master is deleted. Usage: python tools/fetch_footage.py [out ...]"""
import json, subprocess, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets/footage"; OUT.mkdir(parents=True, exist_ok=True)
# identifier | file name (prefix) | out | mode: copy or encode
FILMS = """gov.archives.arc.2773|gov.archives.arc.2773.mpeg|p38_flight_1943|encode
17DaysTh1945|17DaysTh1945.mp4|seventeen_days_1945|copy
PersonalHealthInTheJungle|TF 8-2057 Personal Health In The Jungle.mp4|jungle_health_1944|copy
JungleManeuversInThePacific|Jungle Maneuvers In The Pacific 1945.mp4|jungle_maneuvers_1945|copy
submarine-warfare-1946|Submarine Warfare (1946).mp4|submarine_warfare_1946|copy
NPC-3844|428-npc-3844|silent_service_1945|encode
NPC-15514|NPC-15514.mov|submarine_film_1945|encode
111-adc-3330|111-adc-3330.mp4|rescued_pows_leyte_1945|copy
111-adc-3381|111-adc-3381.mp4|bataan_nurses_1945|copy
111-adc-3273|111-adc-3273.mp4|cebu_prisoners_1945|copy
ADC-4065|ADC-4065.mov|baguio_mindanao_1945|encode
ADC-4068a|ADC-4068a.mov|parachute_mindanao_1945|encode
ADC-4473b|ADC-4473b.mov|evac_mindanao_1945|encode
111-adc-3613|111-adc-3613.mp4|mindanao_san_roque_1945|copy
111-adc-3334|111-adc-3334.mp4|rice_line_manila_1945|copy
gov.archives.arc.39053|gov.archives.arc.39053.mpeg|corregidor_newsreel_1945|encode
ARC-39033|ARC-39033.mov|macarthur_returns_1944|encode
1945-03-01_Santo_Tomas_Prisoners_Liberated|1945-03-01_Santo_Tomas_Prisoners_Liberated.mpeg|santo_tomas_1945|encode"""

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

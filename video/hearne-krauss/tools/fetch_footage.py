"""Download the best-quality archive.org copy of each film into assets/footage/<out>.mp4 (owner's rule: never the 512kb copy).
Small h.264 copies are downloaded as they are; big masters (MPEG2, 720p/1080p .mov/.mp4) are read straight from the
stream and re-encoded to a compact progressive h.264 (deinterlaced, at most 1280 wide), so the 1 GB originals never
touch the disk. Usage: python tools/fetch_footage.py [out ...]"""
import json, subprocess, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets/footage"; OUT.mkdir(parents=True, exist_ok=True)
# identifier | file name (prefix) | out | mode: copy or encode
FILMS = """Aroundth1940|Aroundth1940.mp4|around_the_world_in_new_york_1940|copy
Arteries1941|Arteries1941.mp4|arteries_of_new_york_1941|copy
TroopTra1943|TroopTra1943.mp4|troop_train_1943|copy
Children1940|Children1940.mp4|children_must_learn_1940|copy
TheRiver_201503|96.1 The River.mp4|the_river_1937|copy
CEP163|CEP163.mpg|cotton_cultivation_1937|encode
CEP165|CEP165.mpg|cotton_bales_1937|encode
gov.archives.arc.23655|gov.archives.arc.23655.mpeg|tunisian_campaign_1943|encode
ADC-140|111-adc-140|prisoners_shipped_adc140|encode
FB-164|FB-164 Controlling German Prisoners Of War c1944.mov|controlling_german_pows_1944|encode
FB-203|FB-203 The General Hospital 1945.mov|general_hospital_1945|encode
1945-05-31_US_War_Dead_Honored_On_Memorial_Day|1945-05-31_US_War_Dead_Honored_On_Memorial_Day.mp4|memorial_day_1945|copy
0320_Inside_Story_of_Modern_Gasoline_The_21_01_00_00|0320_Inside_Story_of_Modern_Gasoline_The_21_01_00_00.mp4|modern_gasoline_1946|copy"""

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
        subprocess.run(["curl", "-sSL", "--retry", "5", "-o", str(tmp), url], check=True)
    else:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-reconnect", "1", "-reconnect_streamed", "1", "-i", url, "-an",
                        "-vf", "bwdif=mode=send_frame:deint=interlaced,scale='min(1280,iw)':-2",
                        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p", str(tmp)], check=True)
    if tmp.stat().st_size < 1e6:  # a dropped stream can end "successfully" with an empty file
        tmp.unlink(); print("  failed, run again"); continue
    tmp.replace(dst)
    print(f"  -> {dst.stat().st_size / 1e6:.0f} MB", flush=True)

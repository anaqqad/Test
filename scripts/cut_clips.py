#!/usr/bin/env python3
"""Cut public-domain film clips for a reel spec.

Usage:
    python scripts/cut_clips.py data/reel-<slug>.json <folder with the downloaded source films>

The spec lists clips under "clips": {"<key>": {"file": "<local file name>", "commons": "File:<title>",
"start": <seconds>, "dur": <seconds>}}. The source films come from Wikimedia Commons and must be
public domain there (check the file page first). Each clip is cut to an H.264 MP4 at 30 fps without
sound (the reel has its own narration and music).

Output:
    public/pd/<spec.id>/clips/<key>.mp4
    public/pd/<spec.id>/clips/clips.json   width, height, source title, URL and time range per key
"""
from __future__ import annotations

import json
import subprocess
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def probe(path: Path) -> tuple[int, int]:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,sample_aspect_ratio", "-of", "json", str(path)],
        capture_output=True, text=True, check=True,
    ).stdout
    s = json.loads(out)["streams"][0]
    return int(s["width"]), int(s["height"])


def main() -> None:
    spec_path, src_dir = Path(sys.argv[1]), Path(sys.argv[2])
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    out_dir = ROOT / "public" / "pd" / spec["id"] / "clips"
    out_dir.mkdir(parents=True, exist_ok=True)
    meta = {}
    for key, c in spec.get("clips", {}).items():
        dst = out_dir / f"{key}.mp4"
        src = src_dir / c["file"]
        # square pixels, 30 fps, slightly sharpened; no audio
        # optional "speed" < 1 plays the clip in slow motion (a short shot stretched to fit a beat)
        speed = float(c.get("speed", 1))
        vf = f"setpts=PTS/{speed},scale=trunc(iw*sar/2)*2:ih,setsar=1,fps=30,unsharp=5:5:0.4"
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-ss", str(c["start"]), "-t", str(c["dur"]), "-i", str(src), "-an", "-vf", vf,
             "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(dst)],
            check=True,
        )
        w, h = probe(dst)
        seconds = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(dst)],
                                       capture_output=True, text=True, check=True).stdout.strip())
        title = c["commons"]
        meta[key] = {
            "width": w, "height": h, "seconds": round(seconds, 3), "title": title, "start": c["start"], "dur": c["dur"],
            "source": "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_")),
            "license": "Public domain",
        }
        print(f"  ok {key}: {title} @ {c['start']}s +{c['dur']}s ({w}x{h})")
    (out_dir / "clips.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""QC for a rendered MathDoc: one frame per beat on a contact sheet + pacing and loudness report.

Usage:
    python3 scripts/qc_mathdoc.py data/mathdoc-eratosthenes.json out/mathdoc-eratosthenes.mp4

Writes out/<id>.contact.jpg and out/<id>.qc.json and prints a summary. Each tile shows the
beat id, its start time and length and the narration it covers, so you can check at a glance
that every clause has its own picture and that nothing is blank or mistimed.
Frames are grabbed just before each cut, when all of the beat's cue animations have fired.
Uses Remotion's bundled ffmpeg (npx remotion ffmpeg), so no extra install is needed.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
TW, TH, COLS = 480, 270, 4


def ffmpeg(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["npx", "remotion", "ffmpeg", "-hide_banner", *args], cwd=ROOT, capture_output=True, text=True)


def main() -> None:
    spec = json.loads(Path(sys.argv[1]).read_text())
    video = Path(sys.argv[2])
    tl = json.loads((ROOT / "public" / "generated" / spec["id"] / "timeline.json").read_text())
    fps = tl["fps"]
    texts = {b["id"]: b["text"] for b in spec["beats"]}
    font = ImageFont.load_default(size=17)
    tiles = []
    with tempfile.TemporaryDirectory() as tmp:
        for i, b in enumerate(tl["beats"]):
            t = (b["endFrame"] - 4) / fps  # last frames: every cue has fired
            png = Path(tmp) / f"{i}.png"
            ffmpeg("-y", "-ss", f"{t:.3f}", "-i", str(video), "-frames:v", "1", "-vf", f"scale={TW}:{TH}", str(png))
            frame = Image.open(png).convert("RGB") if png.exists() else Image.new("RGB", (TW, TH), "red")
            tile = Image.new("RGB", (TW, TH + 92), (18, 18, 18))
            tile.paste(frame, (0, 0))
            d = ImageDraw.Draw(tile)
            start, dur = b["startFrame"] / fps, (b["endFrame"] - b["startFrame"]) / fps
            d.text((6, TH + 4), f"#{i + 1} {b['id']}  {start:.1f}s  ({dur:.1f}s)", fill=(255, 220, 90), font=font)
            for k, line in enumerate(textwrap.wrap(texts.get(b["id"], ""), 52)[:3]):
                d.text((6, TH + 26 + k * 20), line, fill=(230, 230, 230), font=font)
            tiles.append(tile)

    rows = (len(tiles) + COLS - 1) // COLS
    sheet = Image.new("RGB", (COLS * TW, rows * (TH + 92)), (0, 0, 0))
    for i, tile in enumerate(tiles):
        sheet.paste(tile, ((i % COLS) * TW, (i // COLS) * (TH + 92)))
    out_sheet = video.with_suffix(".contact.jpg")
    sheet.save(out_sheet, quality=88)

    # Remotion's ffmpeg build has loudnorm (not ebur128); its measurement pass reports input loudness
    loud = ffmpeg("-nostats", "-i", str(video), "-vn", "-af", "loudnorm=print_format=json", "-f", "null", "-").stderr
    lufs = re.findall(r'"input_i" : "(-?[\d.]+)"', loud)
    peak = re.findall(r'"input_tp" : "(-?[\d.]+)"', loud)
    durations = [(b["endFrame"] - b["startFrame"]) / fps for b in tl["beats"]]
    total = tl["durationInFrames"] / fps
    words = [len(texts.get(b["id"], "").split()) for b in tl["beats"]]
    report = {
        "video": str(video),
        "durationSeconds": round(total, 2),
        "beats": len(durations),
        "beatsPerMinute": round(len(durations) / (total / 60), 1),
        "beatSeconds": {"mean": round(sum(durations) / len(durations), 2), "min": round(min(durations), 2), "max": round(max(durations), 2)},
        "wordsPerBeat": round(sum(words) / len(words), 1),
        "wpm": tl.get("wpm"),
        "integratedLUFS": float(lufs[-1]) if lufs else None,
        "truePeakDBFS": float(peak[-1]) if peak else None,
        "contactSheet": str(out_sheet),
    }
    video.with_suffix(".qc.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()

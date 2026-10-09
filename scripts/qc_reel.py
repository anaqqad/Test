#!/usr/bin/env python3
"""QC for a vertical Reel: safe zones, cover frame, captions, length, script, loudness.

Usage:
    python3 scripts/qc_reel.py data/reel-robert-smalls.json [out/reel-robert-smalls.mp4]

1. Safe zones (always). Facebook covers the bottom 20 % of a Reel (caption, music line) and the
   right 15 % (like / comment / share buttons); anything touching the left or top edge is cut off.
   The composition is rendered in QC mode
   ("qc": true): every caption, title and label is painted solid magenta and every face box cyan, on black, at
   1/4 scale, every frame. Any masked pixel in the bottom 20 % or right 15 %, or text touching the left/top edge, is a failure, reported
   per beat with the first offending time.
2. Cover frame: frame 0 must already carry the hook text, and a face when the opening picture has one\n   (it is the cover still).
3. Captions: 2-4 words on screen at a time (same chunking as src/reel/Captions.tsx).
4. Script: 140-170 words; length 45-75 s (from timeline.json).
5. With a rendered video: integrated loudness (target -14 LUFS +/- 1) and true peak (<= -1 dBTP),
   plus a contact sheet out/<id>.contact.jpg with one frame per beat.
6. With a rendered video: audible hook. The voice must start within 0.15 s (no silent lead-in) and the
   first 3 s must be at least as loud as the whole reel (-1 LU), because viewers decide in the first second.

Writes out/<id>.qc.json and exits 1 if any check fails.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
SCALE = 0.25
BOTTOM, RIGHT = 0.80, 0.85  # Facebook's overlays start here (fractions of height / width)
MAX_WORDS, MAX_CHARS, PAUSE = 4, 28, 0.35  # keep in step with src/reel/Captions.tsx


def masks(img: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """(text mask, face mask): magenta = captions/titles/labels, cyan = faces."""
    r, g, b = img[..., 0].astype(int), img[..., 1].astype(int), img[..., 2].astype(int)
    return (r > 170) & (b > 170) & (g < 90), (g > 170) & (b > 170) & (r < 90)


def render_mask(spec_path: Path, spec: dict, tmp: Path) -> list[Path]:
    props = dict(spec, qc=True)
    props_file = tmp / "props.json"
    props_file.write_text(json.dumps(props))
    out = tmp / "frames"
    cmd = ["npx", "remotion", "render", "Reel", str(out), "--sequence", "--image-format=png", f"--scale={SCALE}", f"--props={props_file}", "--log=error"]
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(f"QC render failed:\n{r.stderr[-2000:]}")
    return sorted(out.glob("*.png"), key=lambda p: int(re.findall(r"\d+", p.stem)[-1]))


def balanced(items: list, k: int) -> list[list]:
    out, i = [], 0
    for g in range(k):
        size = -(-(len(items) - i) // (k - g))
        out.append(items[i : i + size])
        i += size
    return out


def chunk_words(words: list[dict]) -> list[list[dict]]:
    """Mirror of chunkWords in src/reel/Captions.tsx."""
    chars = lambda ws: len(" ".join(w["text"] for w in ws))  # noqa: E731
    phrases, cur = [], []
    for i, w in enumerate(words):
        cur.append(w)
        nxt = words[i + 1] if i + 1 < len(words) else None
        if not nxt or re.search(r"[.,!?;:]$", w["text"]) or nxt["start"] - w["end"] > PAUSE:
            phrases.append(cur)
            cur = []
    merged: list[list[dict]] = []
    for i, p in enumerate(phrases):
        if len(p) == 1 and merged and len(merged[-1]) < MAX_WORDS:
            merged[-1].extend(p)
        elif len(p) == 1 and i + 1 < len(phrases):
            phrases[i + 1] = p + phrases[i + 1]
        else:
            merged.append(p)
    out = []
    for p in merged:
        k = -(-len(p) // MAX_WORDS)
        while k < len(p) // 2 and any(chars(g) > MAX_CHARS for g in balanced(p, k)):
            k += 1
        out.extend(balanced(p, k))
    return out


def ffmpeg(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["npx", "remotion", "ffmpeg", "-hide_banner", *args], cwd=ROOT, capture_output=True, text=True)


def contact_sheet(spec: dict, tl: dict, video: Path) -> Path:
    tw, th, cols = 270, 480, 6
    font = ImageFont.load_default(size=15)
    texts = {b["id"]: b["text"] for b in spec["beats"]}
    tiles = []
    with tempfile.TemporaryDirectory() as tmp:
        for i, b in enumerate(tl["beats"]):
            t = (b["startFrame"] + min(45, (b["endFrame"] - b["startFrame"]) // 2)) / tl["fps"]
            png = Path(tmp) / f"{i}.png"
            ffmpeg("-y", "-ss", f"{t:.3f}", "-i", str(video), "-frames:v", "1", "-vf", f"scale={tw}:{th}", str(png))
            frame = Image.open(png).convert("RGB") if png.exists() else Image.new("RGB", (tw, th), "red")
            tile = Image.new("RGB", (tw, th + 70), (18, 18, 18))
            tile.paste(frame, (0, 0))
            d = ImageDraw.Draw(tile)
            d.text((4, th + 4), f"#{i + 1} {b['id']} {b['startFrame'] / tl['fps']:.1f}s", fill=(226, 178, 74), font=font)
            words = texts.get(b["id"], "")
            d.text((4, th + 24), words[:34], fill=(230, 230, 230), font=font)
            d.text((4, th + 44), words[34:68], fill=(230, 230, 230), font=font)
            tiles.append(tile)
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw, rows * (th + 70)))
    for i, tile in enumerate(tiles):
        sheet.paste(tile, ((i % cols) * tw, (i // cols) * (th + 70)))
    out = video.with_suffix(".contact.jpg")
    sheet.save(out, quality=86)
    return out


def audible_hook(video: Path) -> dict:
    import numpy as np
    import pyloudnorm
    import soundfile

    with tempfile.TemporaryDirectory() as tmp:
        wav = Path(tmp) / "a.wav"
        ffmpeg("-y", "-i", str(video), "-vn", "-ac", "1", "-ar", "48000", str(wav))
        audio, sr = soundfile.read(str(wav))
    win = int(0.01 * sr)
    rms = np.sqrt(np.convolve(audio**2, np.ones(win) / win, mode="valid"))
    loud = np.nonzero(rms > 10 ** (-30 / 20))[0]
    onset = round(float(loud[0]) / sr, 2) if loud.size else None
    # both measured on the same mono downmix, so they compare like with like
    meter = pyloudnorm.Meter(sr)
    first3 = float(meter.integrated_loudness(audio[: 3 * sr]))
    whole = float(meter.integrated_loudness(audio))
    ok = onset is not None and onset <= 0.15 and first3 >= whole - 1
    return {"ok": ok, "voiceOnsetSeconds": onset, "first3sVsWholeLU": round(first3 - whole, 2), "target": "voice by 0.15 s; first 3 s >= whole - 1 LU"}


def main() -> None:
    spec_path = Path(sys.argv[1])
    spec = json.loads(spec_path.read_text())
    video = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else None
    tl_path = ROOT / "public" / "generated" / spec["id"] / "timeline.json"
    tl = json.loads(tl_path.read_text()) if tl_path.exists() else None
    fps = spec.get("fps", 30)
    checks: dict[str, dict] = {}

    # 1 + 2: safe zones and cover frame, from the QC mask render
    with tempfile.TemporaryDirectory() as tmp:
        frames = render_mask(spec_path, spec, Path(tmp))
        violations: dict[str, dict] = {}
        beats = tl["beats"] if tl else None
        cover_text = cover_face = False
        for n, f in enumerate(frames):
            text, face = masks(np.asarray(Image.open(f).convert("RGB")))
            m = text | face
            h, w = m.shape
            bottom = int(m[int(h * BOTTOM) :, :].sum())
            right = int(m[: int(h * BOTTOM), int(w * RIGHT) :].sum())
            # text running off the left or top edge is cut off too
            edge = int(text[:, : max(1, int(w * 0.02))].sum() + text[: max(1, int(h * 0.02)), :].sum())
            if n == 0:
                cover_text = bool(text.sum() > 50)
                cover_face = bool(face.sum() > 200)
            if bottom or right or edge:
                beat = next((b["id"] for b in beats if b["startFrame"] <= n < b["endFrame"]), "?") if beats else "(no timeline)"
                v = violations.setdefault(beat, {"firstSecond": round(n / fps, 2), "lastSecond": 0.0, "frames": 0, "maxPixelsBottom": 0, "maxPixelsRight": 0, "maxPixelsAtEdge": 0})
                v["lastSecond"] = round(n / fps, 2)
                v["frames"] += 1
                v["maxPixelsBottom"] = max(v["maxPixelsBottom"], bottom)
                v["maxPixelsRight"] = max(v["maxPixelsRight"], right)
                v["maxPixelsAtEdge"] = max(v["maxPixelsAtEdge"], edge)
        checks["safeZones"] = {"ok": not violations, "framesChecked": len(frames), "scale": SCALE, "violations": violations}
        v0 = spec["beats"][0]["visual"]
        needs_face = bool(spec.get("faces", {}).get(v0.get("image") or v0.get("then") or ""))
        checks["coverFrame"] = {"ok": cover_text and (cover_face or not needs_face), "hookText": cover_text, "face": cover_face, "faceExpected": needs_face}

    # 3 + 4: captions, script and length
    words = sum(len(b["text"].split()) for b in spec["beats"])
    checks["scriptWords"] = {"ok": 140 <= words <= 170, "words": words, "target": "140-170"}
    if tl:
        hidden = {b["id"] for b in spec["beats"] if b.get("captions") is False}
        sizes = [len(c) for b in tl["beats"] if b["id"] not in hidden for c in chunk_words(b["words"])]
        bad = [s for s in sizes if not 2 <= s <= 4]
        checks["captions"] = {"ok": not bad, "chunks": len(sizes), "wordsPerChunk": {"min": min(sizes), "max": max(sizes)}, "outside2to4": len(bad)}
        secs = tl["durationInFrames"] / tl["fps"]
        checks["length"] = {"ok": 45 <= secs <= 75, "seconds": round(secs, 2), "target": "45-75"}
        checks["timeline"] = {"ok": True, "engine": tl.get("engine", "estimate"), "wpm": tl.get("wpm")}
        # quick hook: the spoken hook line ends within 2.5 s and is at most 8 words (owner, 2026-10-09)
        hook = tl["beats"][0]
        hook_end = hook["words"][-1]["end"] if hook["words"] else 0.0
        checks["quickHook"] = {"ok": hook_end <= 2.5 and len(hook["words"]) <= 8, "spokenSeconds": round(hook_end, 2),
                               "words": len(hook["words"]), "target": "<= 2.5 s, <= 8 words"}
    else:
        checks["timeline"] = {"ok": False, "note": "no timeline.json yet (narration not generated)"}

    # 5: loudness and contact sheet from the rendered video
    if video and video.exists():
        loud = ffmpeg("-nostats", "-i", str(video), "-vn", "-af", "loudnorm=print_format=json", "-f", "null", "-").stderr
        lufs = re.findall(r'"input_i" : "(-?[\d.]+)"', loud)
        peak = re.findall(r'"input_tp" : "(-?[\d.]+)"', loud)
        li = float(lufs[-1]) if lufs else None
        tp = float(peak[-1]) if peak else None
        checks["loudness"] = {"ok": li is not None and abs(li + 14) <= 1 and tp is not None and tp <= -0.9, "integratedLUFS": li, "truePeakDBTP": tp, "target": "-14 LUFS, <= -1 dBTP"}
        checks["audibleHook"] = audible_hook(video)
        if tl:
            checks["contactSheet"] = {"ok": True, "file": str(contact_sheet(spec, tl, video))}

    ok = all(c["ok"] for c in checks.values())
    report = {"spec": str(spec_path), "ok": ok, "checks": checks}
    out = ROOT / "out" / f"{spec['id']}.qc.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()

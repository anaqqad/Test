#!/usr/bin/env python3
"""Re-edit a voiced long-form spec without calling a TTS API: drop beats, add pauses, change tempo.

Usage:
    python scripts/rework_doc_audio.py data/doc-robert-smalls.json --tempo 0.94 --gap 1.2 --tail 4

Starts from public/generated/<id>/narration.voiced.wav + timeline.voiced.json (the untouched voice
recording; created from narration.wav / timeline.json on first run). Keeps only the beats still in
the spec, in spec order, each with its original audio span (from its cut point to the next beat's).
Inserts `gap` seconds of silence before every beat that starts a section, adds `tail` at the end,
then time-stretches the whole narration by `tempo` with ffmpeg atempo (pitch preserved) and scales
every word and cut time to match. Writes narration.wav and timeline.json; run make_music.py and
mix_mathdoc.py afterwards.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

import numpy as np
import soundfile as sf

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--tempo", type=float, default=1.0)
    ap.add_argument("--gap", type=float, default=1.0)
    ap.add_argument("--tail", type=float, default=3.0)
    a = ap.parse_args()
    spec = json.loads(Path(a.spec).read_text(encoding="utf-8"))
    out = ROOT / "public" / "generated" / spec["id"]
    wav, tl = out / "narration.wav", out / "timeline.json"
    wav0, tl0 = out / "narration.voiced.wav", out / "timeline.voiced.json"
    if not wav0.exists():
        shutil.copy(wav, wav0)
        shutil.copy(tl, tl0)
    audio, sr = sf.read(wav0, always_2d=True)
    t0 = json.loads(tl0.read_text(encoding="utf-8"))
    fps = t0["fps"]
    voiced = t0["beats"]
    span = {}
    for i, b in enumerate(voiced):
        s = 0.0 if i == 0 else b["startFrame"] / fps
        e = voiced[i + 1]["startFrame"] / fps if i + 1 < len(voiced) else len(audio) / sr
        span[b["id"]] = (s, e, b)

    pieces, beats, pos = [], [], 0.0  # pos: seconds in the new (unstretched) narration
    for i, sb in enumerate(spec["beats"]):
        if sb["id"] not in span:
            raise SystemExit(f"beat {sb['id']} has no voiced audio; its text must be voiced first")
        s, e, vb = span[sb["id"]]
        start = pos
        if i and sb.get("section"):
            pieces.append(np.zeros((int(round(a.gap * sr)), audio.shape[1]), dtype=audio.dtype))
            pos += a.gap
        seg = audio[int(round(s * sr)) : int(round(e * sr))]
        pieces.append(seg)
        words = [{"text": w["text"], "start": pos + (w["start"] - s), "end": pos + (w["end"] - s)} for w in vb["words"]]
        pos += len(seg) / sr
        beats.append({"id": sb["id"], "start": start, "cues": vb.get("cues", {}), "words": words})
    pieces.append(np.zeros((int(round(a.tail * sr)), audio.shape[1]), dtype=audio.dtype))
    joined = np.concatenate(pieces)

    with tempfile.TemporaryDirectory() as td:
        src, dst = Path(td) / "in.wav", Path(td) / "out.wav"
        sf.write(src, joined, sr)
        if abs(a.tempo - 1.0) > 1e-6:
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-af", f"atempo={a.tempo}", str(dst)], check=True)
        else:
            shutil.copy(src, dst)
        new, sr2 = sf.read(dst, always_2d=True)
    sf.write(wav, new, sr2)

    k = 1.0 / a.tempo
    total = int(round(len(new) / sr2 * fps))
    out_beats = []
    for i, b in enumerate(beats):
        sf_ = 0 if i == 0 else int(round(b["start"] * k * fps))
        out_beats.append({
            "id": b["id"],
            "startFrame": sf_,
            "endFrame": 0,
            "cues": b["cues"],
            "words": [{"text": w["text"], "start": round(w["start"] * k, 3), "end": round(w["end"] * k, 3)} for w in b["words"]],
        })
    for i, b in enumerate(out_beats):
        b["endFrame"] = out_beats[i + 1]["startFrame"] if i + 1 < len(out_beats) else total
    tl.write_text(json.dumps({"fps": fps, "durationInFrames": total, "beats": out_beats}, indent=1), encoding="utf-8")
    words = sum(len(b["words"]) for b in out_beats)
    secs = len(new) / sr2
    print(f"{len(out_beats)} beats, {words} words, {secs:.1f}s ({int(secs // 60)}:{int(secs % 60):02d}), {words / (secs / 60):.0f} wpm overall")


if __name__ == "__main__":
    main()

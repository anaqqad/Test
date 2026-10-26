#!/usr/bin/env python3
"""Lengthen a voiced spec without re-voicing it: insert silence before each section and at the end.

Usage:
    python scripts/pad_sections.py data/doc-robert-smalls.json --gap 2.0 --tail 4.0

Used for long-form docs that land a few seconds under 8:00 (YouTube mid-rolls need 8:00+).
Reads public/generated/<id>/narration.wav and timeline.json, keeps the originals as
narration.voiced.wav / timeline.voiced.json (and always starts from those), inserts `gap`
seconds of silence at the cut point of every beat that starts a section (except the first beat),
adds `tail` seconds at the end, shifts every later word and beat, and writes both files back.
It never calls a TTS API. Run make_music.py and mix_mathdoc.py afterwards.
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

import numpy as np
import soundfile as sf

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--gap", type=float, default=2.0)
    ap.add_argument("--tail", type=float, default=0.0)
    a = ap.parse_args()
    spec = json.loads(Path(a.spec).read_text(encoding="utf-8"))
    out = ROOT / "public" / "generated" / spec["id"]
    wav, tl = out / "narration.wav", out / "timeline.json"
    wav0, tl0 = out / "narration.voiced.wav", out / "timeline.voiced.json"
    if not wav0.exists():
        shutil.copy(wav, wav0)
        shutil.copy(tl, tl0)
    audio, sr = sf.read(wav0, always_2d=True)
    t = json.loads(tl0.read_text(encoding="utf-8"))
    fps = t["fps"]
    sections = {b["id"] for i, b in enumerate(spec["beats"]) if i and b.get("section")}

    pieces, last, shift = [], 0, 0.0
    for b in t["beats"]:
        if b["id"] in sections:
            at = b["startFrame"] / fps  # cut point: in the pause before the beat's first word
            i = int(round((at - shift) * sr))
            pieces.append(audio[last:i])
            pieces.append(np.zeros((int(round(a.gap * sr)), audio.shape[1]), dtype=audio.dtype))
            last = i
            shift += a.gap
        if shift:
            b["startFrame"] = int(round(b["startFrame"] + (shift - (a.gap if b["id"] in sections else 0)) * fps)) if b["id"] in sections else int(round(b["startFrame"] + shift * fps))
            for w in b["words"]:
                w["start"] = round(w["start"] + shift, 3)
                w["end"] = round(w["end"] + shift, 3)
    pieces.append(audio[last:])
    pieces.append(np.zeros((int(round(a.tail * sr)), audio.shape[1]), dtype=audio.dtype))
    new = np.concatenate(pieces)

    # A section beat's picture starts when the silence starts (so the chapter card holds through
    # the pause); every beat ends where the next one starts.
    beats = t["beats"]
    for i, b in enumerate(beats):
        b["endFrame"] = beats[i + 1]["startFrame"] if i + 1 < len(beats) else int(round(len(new) / sr * fps))
    t["durationInFrames"] = beats[-1]["endFrame"]
    sf.write(wav, new, sr)
    tl.write_text(json.dumps(t, indent=1), encoding="utf-8")
    print(f"{len(sections)} sections padded by {a.gap}s, tail {a.tail}s: {len(audio) / sr:.1f}s -> {len(new) / sr:.1f}s")


if __name__ == "__main__":
    main()

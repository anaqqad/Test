#!/usr/bin/env python3
"""Re-cut a finished MathDoc without re-voicing it: new beat splits, and optional audio edits.

Usage:
    python3 scripts/retime_mathdoc.py data/mathdoc-sand.json --audio <mix.wav or final .mp4> \
        [--cut 15.62:15.86 ...]

Use it when the narration is final but the pictures change: a beat split into several faster
cuts, a word removed from the soundtrack (a mispronounced "a"), new cue words. It never calls
a TTS API.

How:
  1. Reads the word timings from public/generated/<id>/timeline.json (written by tts_mathdoc.py).
  2. Removes each --cut range (seconds) from the soundtrack with a 12 ms equal-power crossfade.
     Words inside a cut are dropped, and every later word moves earlier by the cut length.
  3. Walks the spec's beats in order and assigns them consecutive words. A beat's text must be
     exactly the next words of the narration (punctuation is ignored), so a beat can be split
     or merged freely but the words can't change. A mismatch stops with the position.
  4. Writes timeline.json (cuts 0.1 s before each beat's first word, cues on their words) and
     mix.wav (48 kHz stereo, the soundtrack the MathDoc composition plays).

The original timeline is kept as timeline.voiced.json so the script can be re-run with other
splits; it always starts from that file.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import tempfile
from pathlib import Path

import numpy as np
import soundfile as sf

ROOT = Path(__file__).resolve().parent.parent
CUT_LEAD = 0.1  # same as tts_mathdoc.py: the picture changes just before the word
XFADE = 0.012
SR = 48000


def norm(w: str) -> str:
    return re.sub(r"[^a-z0-9]", "", w.lower())


def load_audio(path: Path) -> np.ndarray:
    if path.suffix.lower() == ".wav":
        audio, sr = sf.read(path, dtype="float32", always_2d=True)
        if sr != SR:
            raise SystemExit(f"{path}: expected {SR} Hz, got {sr}")
        return audio
    with tempfile.TemporaryDirectory() as tmp:
        wav = Path(tmp) / "a.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(path), "-vn", "-ac", "2", "-ar", str(SR), "-c:a", "pcm_f32le", str(wav)], check=True)
        audio, _ = sf.read(wav, dtype="float32", always_2d=True)
    return audio


def cut_audio(audio: np.ndarray, cuts: list[tuple[float, float]]) -> np.ndarray:
    """Remove ranges, latest first so earlier indices stay valid; equal-power crossfade at each join."""
    n = int(XFADE * SR)
    ramp = (np.sin(np.linspace(0, np.pi / 2, n)) ** 2)[:, None]
    for c0, c1 in sorted(cuts, reverse=True):
        i0, i1 = int(c0 * SR), int(c1 * SR)
        join = audio[i0 - n : i0] * ramp[::-1] + audio[i1 - n : i1] * ramp
        audio = np.concatenate([audio[: i0 - n], join, audio[i1:]])
    return audio


def shift(t: float, cuts: list[tuple[float, float]]) -> float | None:
    """Film time after the cuts, or None if t falls inside a cut."""
    out = t
    for c0, c1 in cuts:
        if c0 <= t < c1:
            return None
        if t >= c1:
            out -= c1 - c0
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--audio", required=True, help="the voiced soundtrack: mix.wav or the rendered .mp4")
    ap.add_argument("--cut", action="append", default=[], help="start:end in seconds of the original soundtrack")
    args = ap.parse_args()

    spec = json.loads(Path(args.spec).read_text())
    fps = spec.get("fps", 30)
    out_dir = ROOT / "public" / "generated" / spec["id"]
    voiced = out_dir / "timeline.voiced.json"
    if not voiced.exists():
        voiced.write_text((out_dir / "timeline.json").read_text())
    old = json.loads(voiced.read_text())
    cuts = [tuple(float(x) for x in c.split(":")) for c in args.cut]

    # every spoken word, in order, moved by the cuts (words inside a cut disappear)
    words = []
    for b in old["beats"]:
        for w in b["words"]:
            s, e = shift(w["start"], cuts), shift(w["end"], cuts)
            if s is None or e is None:
                print(f"  cut: '{w['text']}' at {w['start']:.2f}s")
                continue
            words.append({"text": w["text"], "start": round(s, 3), "end": round(e, 3)})

    beats = []
    k = 0
    for beat in spec["beats"]:
        mine = []
        for token in beat["text"].split():
            if k >= len(words) or norm(words[k]["text"]) != norm(token):
                heard = words[k]["text"] if k < len(words) else "<end>"
                raise SystemExit(f"beat '{beat['id']}': script says '{token}', narration has '{heard}' (word {k})")
            mine.append(words[k])
            k += 1
        cues = {}
        for name, cue_word in (beat.get("cues") or {}).items():
            hit = next((w for w in mine if norm(w["text"]) == norm(cue_word)), None)
            if hit is None:
                raise SystemExit(f"beat '{beat['id']}': cue word '{cue_word}' is not in its text")
            cues[name] = round(hit["start"] * fps)
        beats.append({"id": beat["id"], "words": mine, "cues": cues})
    if k != len(words):
        raise SystemExit(f"narration has {len(words) - k} words after the last beat: '{words[k]['text']}' ...")

    removed = sum(c1 - c0 for c0, c1 in cuts)
    duration = old["durationInFrames"] - round(removed * fps)
    starts = [0] + [max(0, round((b["words"][0]["start"] - CUT_LEAD) * fps)) for b in beats[1:]]
    for i, b in enumerate(beats):
        b["startFrame"] = starts[i]
        b["endFrame"] = starts[i + 1] if i + 1 < len(beats) else duration
        if b["endFrame"] - b["startFrame"] < 12:
            print(f"  ! beat '{b['id']}' is only {b['endFrame'] - b['startFrame']} frames")

    audio = cut_audio(load_audio(Path(args.audio)), cuts)
    audio = np.pad(audio, ((0, max(0, round(duration / fps * SR) - len(audio))), (0, 0)))[: round(duration / fps * SR)]
    sf.write(out_dir / "mix.wav", audio, SR, subtype="PCM_24")

    total = duration / fps
    timeline = {**old, "durationInFrames": duration, "words": len(words), "wpm": round(len(words) / (total / 60), 1), "beats": beats}
    timeline["retimed"] = {"from": voiced.name, "audio": Path(args.audio).name, "cuts": cuts}
    (out_dir / "timeline.json").write_text(json.dumps(timeline, indent=1) + "\n")
    print(f"{len(beats)} beats, {len(words)} words, {total:.1f}s (removed {removed:.2f}s) -> {out_dir}")


if __name__ == "__main__":
    main()

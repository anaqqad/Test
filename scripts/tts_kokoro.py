#!/usr/bin/env python3
"""Generate narration + timed captions for a video spec using Kokoro (local, free, Apache-2.0).

Usage:
    python3 scripts/tts_kokoro.py data/american-mall.json

Each narration chunk of each scene is synthesized separately so caption timing is exact
(no speech recognition needed). Output:

    public/generated/<spec.id>/<scene.id>.wav
    public/generated/<spec.id>/narration.json   (read by the Remotion composition)

If a scene's narration would overrun its duration, the speaking rate is raised
automatically (up to MAX_SPEED) and a warning is printed.
"""

from __future__ import annotations

import json
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import soundfile as sf

ROOT = Path(__file__).resolve().parent.parent
MODEL_DIR = ROOT / ".cache" / "kokoro"
MODEL_URL = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/"
MODEL_FILES = ["kokoro-v1.0.onnx", "voices-v1.0.bin"]
TAIL_SECONDS = 0.45  # silence kept free at the end of every scene
MAX_SPEED = 1.3


def ensure_model() -> None:
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    for name in MODEL_FILES:
        target = MODEL_DIR / name
        if not target.exists():
            print(f"Downloading {name} ...")
            urllib.request.urlretrieve(MODEL_URL + name, target)


def trim_silence(samples: np.ndarray, sr: int, threshold: float = 0.01) -> np.ndarray:
    loud = np.where(np.abs(samples) > threshold)[0]
    if len(loud) == 0:
        return samples
    pad = int(0.03 * sr)
    return samples[max(0, loud[0] - pad) : min(len(samples), loud[-1] + pad)]


def syllables(word: str) -> int:
    w = re.sub(r"[^a-z0-9]", "", word.lower())
    if not w:
        return 1
    if w.isdigit():
        return max(2, len(w))  # "1956" is spoken as several syllables
    groups = re.findall(r"[aeiouy]+", w)
    n = len(groups)
    if w.endswith("e") and n > 1:
        n -= 1
    return max(1, n)


def word_timings(text: str, start_ms: float, end_ms: float) -> list[dict]:
    """Estimate per-word timing inside a chunk, weighted by syllables."""
    words = text.split()
    weights = [syllables(w) + 0.35 for w in words]
    total = sum(weights)
    out, t = [], start_ms
    for w, weight in zip(words, weights):
        d = (end_ms - start_ms) * weight / total
        out.append({"text": w, "startMs": round(t), "endMs": round(t + d)})
        t += d
    return out


def synth_scene(kokoro, scene: dict, voice: dict, sr_holder: dict) -> tuple[np.ndarray, list[dict], float]:
    lead = voice.get("leadInSeconds", 0.35)
    gap = voice.get("gapSeconds", 0.18)
    budget = scene["durationInSeconds"] - lead - TAIL_SECONDS
    speed = voice.get("speed", 1.0)

    while True:
        clips = []
        for chunk in scene["narration"]:
            samples, sr = kokoro.create(chunk, voice=voice["voice"], speed=speed, lang="en-us")
            sr_holder["sr"] = sr
            clips.append(trim_silence(np.asarray(samples, dtype=np.float32), sr))
        sr = sr_holder["sr"]
        spoken = sum(len(c) for c in clips) / sr + gap * (len(clips) - 1)
        if spoken <= budget or speed >= MAX_SPEED:
            break
        speed = min(MAX_SPEED, round(speed * spoken / budget + 0.01, 3))

    if spoken > budget:
        print(f"  ! WARNING scene '{scene['id']}' narration is {spoken:.2f}s, budget {budget:.2f}s. Shorten the text.")

    parts = [np.zeros(int(lead * sr), dtype=np.float32)]
    captions = []
    t = lead
    for i, (chunk, clip) in enumerate(zip(scene["narration"], clips)):
        start, end = t, t + len(clip) / sr
        captions.append(
            {
                "text": chunk,
                "startMs": round(start * 1000),
                "endMs": round(end * 1000),
                "words": word_timings(chunk, start * 1000, end * 1000),
            }
        )
        parts.append(clip)
        t = end
        if i < len(clips) - 1:
            parts.append(np.zeros(int(gap * sr), dtype=np.float32))
            t += gap
    audio = np.concatenate(parts)
    # gentle loudness normalisation to about -16 dBFS RMS, peak-limited
    rms = float(np.sqrt(np.mean(audio**2))) or 1.0
    audio = audio * (10 ** (-16 / 20) / rms)
    peak = float(np.max(np.abs(audio)))
    if peak > 0.95:
        audio *= 0.95 / peak
    return audio, captions, speed


def main() -> None:
    spec_path = Path(sys.argv[1] if len(sys.argv) > 1 else ROOT / "data" / "american-mall.json")
    spec = json.loads(spec_path.read_text())
    voice = spec.get("voice", {})
    if voice.get("engine", "kokoro") != "kokoro":
        sys.exit(f"Unsupported voice engine: {voice.get('engine')}")

    ensure_model()
    from kokoro_onnx import Kokoro

    kokoro = Kokoro(str(MODEL_DIR / MODEL_FILES[0]), str(MODEL_DIR / MODEL_FILES[1]))
    out_dir = ROOT / "public" / "generated" / spec["id"]
    out_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "engine": "kokoro-onnx v1.0",
        "voice": voice["voice"],
        "generatedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "scenes": {},
    }
    sr_holder: dict = {}
    # long-form specs use "scenes", Shorts specs use "segments"
    for scene in spec.get("scenes") or spec.get("segments", []):
        if not scene.get("narration"):
            continue
        audio, captions, speed = synth_scene(kokoro, scene, voice, sr_holder)
        fname = f"{scene['id']}.wav"
        sf.write(out_dir / fname, audio, sr_holder["sr"], subtype="PCM_16")
        duration = len(audio) / sr_holder["sr"]
        manifest["scenes"][scene["id"]] = {
            "src": f"generated/{spec['id']}/{fname}",
            "durationInSeconds": round(duration, 3),
            "speed": speed,
            "captions": captions,
        }
        print(f"  {scene['id']:<12} {duration:5.2f}s / {scene['durationInSeconds']}s  (speed {speed})")

    (out_dir / "narration.json").write_text(json.dumps(manifest, indent=2))
    print(f"Wrote {out_dir / 'narration.json'}")


if __name__ == "__main__":
    main()

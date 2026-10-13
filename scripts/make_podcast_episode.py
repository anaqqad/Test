#!/usr/bin/env python3
"""Build a "Black History in 10 Minutes" episode from a spec (free Kokoro voice + original theme).

Usage:
    python3 scripts/make_podcast_episode.py data/podcast-ep01-frederick-douglass.json [out.mp3]

Spec segments, in order:
    {"text": ..., "pause": s, "chapter": "title"?, "bed": true | "in" | "out"?}
        bed true: music bed under the line; "in": bed fades in; "out": bed fades out during the line
    {"swell": s}      music alone at full level (after the welcome, and at the end with "end": true)
    {"interlude": s}  short piano break between chapters
Writes the MP3 (-16 LUFS, peaks about -2 dBFS) and prints chapter timestamps for the description.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
import pyloudnorm as pyln
import soundfile as sf
from kokoro_onnx import Kokoro
from scipy.signal import resample_poly

sys.path.insert(0, str(Path(__file__).parent))
from make_podcast_theme import SR, theme  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
FULL = 0.8  # music level when it plays alone


def main() -> None:
    spec = json.loads(Path(sys.argv[1]).read_text())
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "publish/podcast" / f"{spec['id']}.mp3"
    v = spec["voice"]
    k = Kokoro(str(ROOT / ".cache/kokoro/kokoro-v1.0.onnx"), str(ROOT / ".cache/kokoro/voices-v1.0.bin"))
    duck = 10 ** (spec["music"]["bedDb"] / 20)

    # lay out voice and a music gain curve as (time, gain) points
    t = spec["music"]["lead"]
    clips, pts, chapters = [], [(0.0, FULL), (t - 0.3, FULL), (t, duck)], []
    for seg in spec["segments"]:
        if "text" in seg:
            s, vsr = k.create(seg["text"], voice=v["voice"], speed=seg.get("speed", v["speed"]), lang=v["lang"])
            s = resample_poly(np.asarray(s, dtype=np.float64), SR, vsr)
            if "chapter" in seg:
                chapters.append((t, seg["chapter"]))
            d = len(s) / SR
            bed = seg.get("bed")
            if bed is True:
                pts += [(t, duck), (t + d, duck)]
            elif bed == "out":
                pts += [(t, duck), (t + min(2.0, d), duck), (t + d, 0.0)]
            elif bed == "in":
                pts += [(t, 0.0), (t + d, duck)]
            else:
                pts += [(t, 0.0), (t + d, 0.0)]
            clips.append((t, s))
            t += d + seg.get("pause", 0.6)
            print(f"  {t / 60:5.2f} min  {seg['text'][:60]}", flush=True)
        elif "swell" in seg:
            d = seg["swell"]
            start = pts[-1][1]
            pts += [(t + 0.1, start), (t + 0.8, FULL), (t + d - 0.4, FULL)]
            if seg.get("end"):
                t += d
                pts += [(t, 0.0)]
            else:
                pts += [(t + d, duck)]
                t += d
        elif "interlude" in seg:
            d = seg["interlude"]
            pts += [(t, 0.0), (t + 0.4, FULL * 0.85), (t + d - 0.5, FULL * 0.85), (t + d + 0.6, 0.0)]
            t += d

    total = int((t + 0.5) * SR)
    pts.sort(key=lambda p: p[0])
    gain = np.interp(np.arange(total) / SR, [p[0] for p in pts], [p[1] for p in pts])
    music = theme(total / SR + 1)[:total]
    mix = music * (gain * 0.55)[:, None]
    for start, s in clips:
        i = int(start * SR)
        mix[i : i + len(s)] += s[: total - i, None]

    mix = pyln.normalize.loudness(mix, pyln.Meter(SR).integrated_loudness(mix), -16)
    mix = np.tanh(mix / 0.78) * 0.78
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        wav = Path(tmp) / "ep.wav"
        sf.write(wav, mix, SR)
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(wav), "-c:a", "libmp3lame", "-b:a", "128k",
                        "-metadata", f"title={spec['title']}", "-metadata", f"album={spec['show']}",
                        "-metadata", "artist=The Black History Room", "-metadata", f"track={spec['episode']}",
                        str(out)], check=True)
    words = sum(len(s["text"].split()) for s in spec["segments"] if "text" in s)
    print(f"Wrote {out}: {total / SR / 60:.2f} min, {words} words")
    print("Chapters:")
    for ct, name in chapters:
        print(f"{int(ct // 60)}:{int(ct % 60):02d} {name}")


if __name__ == "__main__":
    main()

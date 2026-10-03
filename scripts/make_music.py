#!/usr/bin/env python3
"""Synthesize an original, royalty-free ambient score bed (no samples, no third-party audio).

Usage:
    python3 scripts/make_music.py data/american-mall.json

Writes public/generated/<spec.id>/music.wav, matching the total spec duration.
A slow minor-key pad (Dm9 - Bbmaj7 - Fadd9 - C6sus) with soft sub, a gentle
filter swell and a simple feedback-delay "room". The mood is nostalgic and unresolved.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

ROOT = Path(__file__).resolve().parent.parent
SR = 44100


def midi_hz(n: float) -> float:
    return 440.0 * 2 ** ((n - 69) / 12)


CHORDS = [
    [50, 57, 60, 64, 65],  # Dm9 (D A C E F)
    [46, 53, 57, 62, 65],  # Bbmaj7 (Bb F A D F)
    [41, 53, 57, 60, 67],  # Fadd9 (F F A C G)
    [48, 55, 57, 62, 67],  # C6sus (C G A D G)
]


def pad_voice(freq: float, n: int, rng: np.random.Generator) -> np.ndarray:
    t = np.arange(n) / SR
    out = np.zeros(n)
    for detune in (-0.12, 0.0, 0.11):  # cents-ish chorus
        f = freq * 2 ** (detune / 12)
        phase = rng.uniform(0, 2 * np.pi)
        # soft saw-ish tone from a few decaying harmonics
        for h, amp in ((1, 1.0), (2, 0.28), (3, 0.12), (4, 0.05)):
            out += amp * np.sin(2 * np.pi * f * h * t + phase * h)
    return out / 3


def envelope(n: int, attack: float, release: float) -> np.ndarray:
    env = np.ones(n)
    a, r = int(attack * SR), int(release * SR)
    env[:a] = np.sin(np.linspace(0, np.pi / 2, a)) ** 2
    env[-r:] = np.cos(np.linspace(0, np.pi / 2, r)) ** 2
    return env


def one_pole_lowpass(x: np.ndarray, cutoff: np.ndarray) -> np.ndarray:
    y = np.zeros_like(x)
    alpha = 1 - np.exp(-2 * np.pi * cutoff / SR)
    acc = 0.0
    for i in range(len(x)):
        acc += alpha[i] * (x[i] - acc)
        y[i] = acc
    return y


def room(x: np.ndarray) -> np.ndarray:
    out = x.copy()
    for delay_s, gain in ((0.113, 0.32), (0.197, 0.26), (0.291, 0.2), (0.411, 0.15), (0.587, 0.1)):
        d = int(delay_s * SR)
        out[d:] += gain * x[:-d]
    return out


def main() -> None:
    spec_path = Path(sys.argv[1] if len(sys.argv) > 1 else ROOT / "data" / "american-mall.json")
    spec = json.loads(spec_path.read_text())
    if "beats" in spec:  # MathDoc: length comes from the narration timeline
        timeline = json.loads((ROOT / "public" / "generated" / spec["id"] / "timeline.json").read_text())
        total = timeline["durationInFrames"] / timeline["fps"]
    else:
        total = sum(s["durationInSeconds"] for s in (spec.get("scenes") or spec.get("segments", [])))
    n_total = int(total * SR)
    rng = np.random.default_rng(1956)
    if spec.get("format") == "short":
        write(spec, pulse_bed(total), total)
        return

    mix = np.zeros(n_total)
    chord_len = total / 8  # two passes through the progression
    overlap = 2.5
    for i in range(8):
        start = int(i * chord_len * SR)
        n = min(int((chord_len + overlap) * SR), n_total - start)
        if n <= 0:
            break
        chord = CHORDS[i % len(CHORDS)]
        seg = sum(pad_voice(midi_hz(m), n, rng) * (0.9 if j else 0.6) for j, m in enumerate(chord))
        sub = 0.5 * np.sin(2 * np.pi * midi_hz(chord[0] - 12) * np.arange(n) / SR)
        seg = (seg + sub) * envelope(n, 2.2, 2.8)
        mix[start : start + n] += seg

    t = np.arange(n_total) / SR
    cutoff = 700 + 500 * (0.5 - 0.5 * np.cos(2 * np.pi * t / 20))  # slow breathing filter
    mix = one_pole_lowpass(mix, cutoff)
    mix = room(mix)
    # overall arc: fade in, fade out on the final question
    mix *= envelope(n_total, 2.5, 4.0)
    mix /= np.max(np.abs(mix)) + 1e-9
    mix *= 0.7
    stereo = np.stack([mix, np.roll(mix, int(0.012 * SR))], axis=1)

    write(spec, stereo, total)


def write(spec: dict, stereo: np.ndarray, total: float) -> None:
    out_dir = ROOT / "public" / "generated" / spec["id"]
    out_dir.mkdir(parents=True, exist_ok=True)
    sf.write(out_dir / "music.wav", stereo.astype(np.float32), SR, subtype="PCM_16")
    print(f"Wrote {out_dir / 'music.wav'} ({total}s)")


def pulse_bed(total: float, bpm: float = 118) -> np.ndarray:
    """Upbeat, original news-style bed for Shorts: kick, off-beat hats, plucked bass, soft stabs."""
    n = int(total * SR)
    beat = 60 / bpm
    out = np.zeros(n)
    rng = np.random.default_rng(2026)
    t_kick = np.arange(int(0.25 * SR)) / SR
    kick = np.sin(2 * np.pi * (48 + 90 * np.exp(-t_kick * 30)) * t_kick) * np.exp(-t_kick * 12)
    hat = rng.standard_normal(int(0.05 * SR)) * np.exp(-np.arange(int(0.05 * SR)) / SR * 90)
    hat = np.diff(hat, prepend=0)  # crude high-pass
    roots = [45, 45, 41, 43]  # A A F G
    i = 0
    while i * beat < total:
        s = int(i * beat * SR)
        bar = int(i // 4)
        seg = kick[: max(0, min(len(kick), n - s))]
        out[s : s + len(seg)] += 0.9 * seg
        hs = int((i + 0.5) * beat * SR)
        hseg = hat[: max(0, min(len(hat), n - hs))]
        out[hs : hs + len(hseg)] += 0.25 * hseg
        # bass on 8ths
        for k in range(2):
            bs = int((i + k * 0.5) * beat * SR)
            dur = int(beat * 0.45 * SR)
            if bs + dur >= n:
                continue
            tb = np.arange(dur) / SR
            f = midi_hz(roots[bar % 4])
            out[bs : bs + dur] += 0.35 * np.tanh(2 * np.sin(2 * np.pi * f * tb)) * np.exp(-tb * 6)
        # chord stab every bar
        if i % 4 == 0:
            dur = int(beat * 1.5 * SR)
            if s + dur < n:
                tc = np.arange(dur) / SR
                stab = sum(np.sin(2 * np.pi * midi_hz(roots[bar % 4] + 24 + iv) * tc) for iv in (0, 3, 7, 10))
                out[s : s + dur] += 0.08 * stab * np.exp(-tc * 3)
        i += 1
    out *= envelope(n, 0.4, 1.5)
    out /= np.max(np.abs(out)) + 1e-9
    out *= 0.7
    return np.stack([out, np.roll(out, int(0.008 * SR))], axis=1)


if __name__ == "__main__":
    main()

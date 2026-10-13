#!/usr/bin/env python3
"""Synthesize the original, royalty-free theme for the podcast "Black History in 10 Minutes".

Usage:
    python3 scripts/make_podcast_theme.py out.wav [seconds]

Version 2 (2026-10-13), shaped on measurements of two example history podcasts: voice starts
within ~1 s, music is a soft sustained bed with no drums (tonal, low onset variance), sitting
~15-20 dB under the voice, and swells in the pause after the episode title.

A slow, warm felt-piano progression (Am - F - C - G, 66 bpm) over a quiet string-like pad and
a low cello-style root, in a convolution room. Nothing is sampled; every sound is generated here.
"""

from __future__ import annotations

import sys

import numpy as np
import soundfile as sf
from scipy.signal import fftconvolve

SR = 44100
BPM = 66
BEAT = 60 / BPM
# (root for the low string, piano voicing, pad voicing)
CHORDS = [
    (45, [57, 60, 64, 69], [57, 64, 72]),  # Am
    (41, [57, 60, 65, 69], [53, 65, 72]),  # F
    (48, [55, 60, 64, 67], [55, 64, 72]),  # C
    (43, [55, 59, 62, 67], [55, 62, 71]),  # G
]


def hz(n: float) -> float:
    return 440.0 * 2 ** ((n - 69) / 12)


def piano(f: float, n: int, vel: float) -> np.ndarray:
    """Felt-piano-ish tone: slightly inharmonic partials, upper partials die fast, soft attack."""
    t = np.arange(n) / SR
    out = np.zeros(n)
    for k in range(1, 9):
        fk = k * f * np.sqrt(1 + 0.0004 * k * k)
        if fk > 9000:
            break
        amp = (0.6 ** (k - 1)) * (0.5 + 0.5 * vel)
        dec = 2.8 / (1 + 0.9 * (k - 1)) * (220 / max(f, 110)) ** 0.3
        out += amp * np.sin(2 * np.pi * fk * t + k) * np.exp(-t / dec)
    attack = np.minimum(1, t / 0.012)
    return out * attack * vel


def pad(notes: list[int], n: int, rng: np.random.Generator) -> np.ndarray:
    """Soft string-like pad: detuned saws, low-passed by averaging, slow swell."""
    t = np.arange(n) / SR
    out = np.zeros((n, 2))
    for note in notes:
        for ch, det in ((0, -0.003), (1, 0.003), (0, 0.0007), (1, -0.0009)):
            ph = rng.uniform(0, 1)
            f = hz(note) * (1 + det) * (1 + 0.002 * np.sin(2 * np.pi * 4.8 * t + ph * 6))
            saw = 2 * ((np.cumsum(f) / SR + ph) % 1) - 1
            out[:, ch] += saw
    k = 24  # gentle low-pass
    out = np.apply_along_axis(lambda c: np.convolve(c, np.ones(k) / k, mode="same"), 0, out)
    sw = np.minimum(1, t / 1.5) * np.minimum(1, (n / SR - t) / 1.2)
    return out / (len(notes) * 2) * sw[:, None]


def room(x: np.ndarray, rng: np.random.Generator, seconds: float = 2.4) -> np.ndarray:
    n = int(seconds * SR)
    t = np.arange(n) / SR
    out = np.zeros_like(x)
    for ch in range(2):
        ir = rng.standard_normal(n) * np.exp(-t / (seconds / 6.9))
        ir = np.convolve(ir, np.ones(6) / 6, mode="same")  # darker tail
        ir[: int(0.015 * SR)] = 0
        ir /= np.sqrt((ir**2).sum())
        out[:, ch] = fftconvolve(x[:, ch], ir)[: len(x)]
    return out


def theme(seconds: float) -> np.ndarray:
    rng = np.random.default_rng(11)
    total = int(seconds * SR)
    dry = np.zeros((total + int(10 * SR), 2))
    bar = 4 * BEAT
    nbar = int(bar * SR)
    for b in range(int(np.ceil(seconds / bar))):
        root, keys, padn = CHORDS[b % 4]
        s = int(b * bar * SR)
        # pad + low string, entering in bar 2 so the opening is piano alone
        if b >= 1:
            seg = pad(padn, nbar + int(1.0 * SR), rng) * 0.10
            dry[s : s + len(seg)] += seg
        tt = np.arange(nbar + int(0.8 * SR)) / SR
        low = np.sin(2 * np.pi * hz(root - 12) * tt) + 0.3 * np.sin(2 * np.pi * hz(root) * tt)
        low *= np.minimum(1, tt / 0.4) * np.minimum(1, (tt[-1] - tt) / 0.8) * 0.13
        dry[s : s + len(low)] += low[:, None]
        # piano: rolled chord on beat 1, then a sparse melody note pattern
        for i, note in enumerate(keys):
            ns = s + int(i * 0.035 * SR)
            tone = piano(hz(note), int(4.5 * SR), 0.55 - 0.05 * i) * 0.11
            pan = 0.35 + 0.1 * i
            dry[ns : ns + len(tone), 0] += tone * (1 - pan)
            dry[ns : ns + len(tone), 1] += tone * pan
        top = keys[-1] + 12
        melody = [(1.5, top - 5), (2.0, top - 3 if b % 2 == 0 else top - 1), (3.0, top - 5)]
        for beat, note in melody:
            ns = s + int(beat * BEAT * SR)
            tone = piano(hz(note), int(3.0 * SR), 0.4) * 0.09
            dry[ns : ns + len(tone)] += tone[:, None] * np.array([0.45, 0.55])
    dry = dry[:total]
    wet = room(dry, rng)
    out = 0.75 * dry + 0.55 * wet
    fade = int(3.0 * SR)
    out[-fade:] *= np.linspace(1, 0, fade)[:, None]
    return out / (np.abs(out).max() + 1e-9) * 0.9


if __name__ == "__main__":
    path = sys.argv[1]
    secs = float(sys.argv[2]) if len(sys.argv) > 2 else 40.0
    sf.write(path, theme(secs), SR)
    print(f"Wrote {path} ({secs:.1f}s)")

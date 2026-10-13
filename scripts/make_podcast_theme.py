#!/usr/bin/env python3
"""Synthesize the original, royalty-free theme for the podcast "Black History in 10 Minutes".

Usage:
    python3 scripts/make_podcast_theme.py out.wav [seconds]

A warm, confident theme at 88 bpm: a soft electric-piano arpeggio over a minor-key pad
(Dm9 - Bbmaj7 - Fadd9 - C), a round sub bass, and a light kick and shaker pulse.
Nothing is sampled; every sound is generated here.
"""

from __future__ import annotations

import sys

import numpy as np
import soundfile as sf

SR = 44100
BPM = 88
BEAT = 60 / BPM
CHORDS = [
    [50, 57, 60, 64, 65],  # Dm9
    [46, 53, 57, 62, 65],  # Bbmaj7
    [41, 53, 57, 60, 67],  # Fadd9
    [48, 55, 60, 64, 67],  # C
]


def hz(n: float) -> float:
    return 440.0 * 2 ** ((n - 69) / 12)


def env(n: int, a: float, d: float) -> np.ndarray:
    t = np.arange(n) / SR
    return np.minimum(1, t / a) * np.exp(-t / d)


def epiano(f: float, n: int) -> np.ndarray:
    t = np.arange(n) / SR
    tone = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t / 0.25)
    tone += 0.12 * np.sin(2 * np.pi * 3.01 * f * t) * np.exp(-t / 0.12)
    return tone * env(n, 0.004, 0.9)


def pad(chord: list[int], n: int) -> np.ndarray:
    t = np.arange(n) / SR
    out = np.zeros(n)
    for note in chord:
        for det in (-0.0015, 0.0, 0.0017):
            out += np.sin(2 * np.pi * hz(note) * (1 + det) * t)
    sw = np.minimum(1, t / 0.6) * np.minimum(1, (n / SR - t) / 0.6)
    return out / (len(chord) * 3) * sw


def kick(n: int) -> np.ndarray:
    t = np.arange(n) / SR
    f = 50 + 70 * np.exp(-t / 0.03)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.18)


def shaker(n: int, rng: np.random.Generator) -> np.ndarray:
    noise = rng.standard_normal(n)
    noise = np.diff(noise, prepend=0)  # brighten
    return noise * env(n, 0.002, 0.03)


def theme(seconds: float) -> np.ndarray:
    rng = np.random.default_rng(7)
    total = int(seconds * SR)
    out = np.zeros((total, 2))
    bar = 4 * BEAT
    nbar = int(bar * SR)
    for b in range(int(np.ceil(seconds / bar))):
        chord = CHORDS[b % 4]
        s = int(b * bar * SR)
        seg = pad(chord, nbar) * 0.22
        e = min(total, s + nbar)
        out[s:e, 0] += seg[: e - s]
        out[s:e, 1] += seg[: e - s]
        # sub bass on beats 1 and 3
        for beat in (0, 2):
            bs = s + int(beat * BEAT * SR)
            n = int(1.4 * BEAT * SR)
            tt = np.arange(n) / SR
            bass = np.sin(2 * np.pi * hz(chord[0] - 12) * tt) * env(n, 0.01, 0.6) * 0.35
            be = min(total, bs + n)
            if bs < total:
                out[bs:be] += bass[: be - bs, None]
        # arpeggio in eighth notes, panned gently
        arp = [chord[1], chord[2], chord[3], chord[4], chord[3], chord[2], chord[4] + 12, chord[3]]
        for i, note in enumerate(arp):
            ns = s + int(i * BEAT / 2 * SR)
            n = int(1.2 * SR)
            tone = epiano(hz(note + 12), n) * 0.16
            ne = min(total, ns + n)
            if ns < total:
                pan = 0.5 + 0.25 * np.sin(i)
                out[ns:ne, 0] += tone[: ne - ns] * (1 - pan)
                out[ns:ne, 1] += tone[: ne - ns] * pan
        # light drums from bar 2
        if b >= 1:
            for beat in range(4):
                ks = s + int(beat * BEAT * SR)
                if beat in (0, 2) and ks < total:
                    k = kick(int(0.4 * SR)) * 0.5
                    ke = min(total, ks + len(k))
                    out[ks:ke] += k[: ke - ks, None]
                for half in (0, 1):
                    ss = s + int((beat + half / 2 + 0.25) * BEAT * SR)
                    if ss < total:
                        sh = shaker(int(0.08 * SR), rng) * 0.05
                        se = min(total, ss + len(sh))
                        out[ss:se] += sh[: se - ss, None]
    # simple room: two feedback delays
    for d, g in ((0.11, 0.25), (0.23, 0.15)):
        k = int(d * SR)
        out[k:] += out[:-k] * g
    fade = int(1.5 * SR)
    out[-fade:] *= np.linspace(1, 0, fade)[:, None]
    return out / (np.abs(out).max() + 1e-9) * 0.9


if __name__ == "__main__":
    path = sys.argv[1]
    secs = float(sys.argv[2]) if len(sys.argv) > 2 else 30.0
    sf.write(path, theme(secs), SR)
    print(f"Wrote {path} ({secs:.1f}s)")

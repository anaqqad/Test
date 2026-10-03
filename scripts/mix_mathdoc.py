#!/usr/bin/env python3
"""Final soundtrack for a MathDoc: level the voice, duck the music gently, master to a fixed loudness.

Usage:
    python3 scripts/mix_mathdoc.py data/mathdoc-eratosthenes-full.json

Reads public/generated/<id>/narration.wav, music.wav and timeline.json and writes mix.wav
(48 kHz stereo), which the MathDoc composition plays instead of the separate tracks.

Aim: no bumps and an even level.
  1. Voice leveller: a slow RMS compressor (2.5:1 above -24 dBFS, 15 ms attack, 250 ms release)
     evens out loud and soft words without pumping.
  2. Music bed: sits ~16 dB under the voice. It dips only 3 dB while someone speaks, with 0.6 s
     / 1.2 s ramps, so the bed never audibly "breathes" between sentences.
  3. Master: integrated loudness normalised to -16 LUFS, then a look-ahead true-peak limiter
     (4x oversampled) at -1.5 dBTP.
Specs can override the targets with "mix": {"targetLufs": -14, "ceilingDbtp": -1.0,
"musicUnderVoiceDb": 20, "duckDb": 3}. Reels use -14 LUFS and a quieter bed.
It prints loudness statistics so the result can be checked, not assumed.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pyloudnorm as pyln
import soundfile as sf
from scipy.signal import resample_poly

ROOT = Path(__file__).resolve().parent.parent
SR = 48000
TARGET_LUFS = -16.0
CEILING_DBTP = -1.5
MUSIC_UNDER_VOICE_DB = 16.0
DUCK_DB = 3.0


def to_sr(x: np.ndarray, sr: int) -> np.ndarray:
    if sr == SR:
        return x
    g = np.gcd(sr, SR)
    return resample_poly(x, SR // g, sr // g, axis=0).astype(np.float32)


def smooth(env: np.ndarray, hop_s: float, attack_s: float, release_s: float) -> np.ndarray:
    """One-pole attack/release smoother on a control-rate envelope (in dB or linear)."""
    a_att = np.exp(-hop_s / attack_s)
    a_rel = np.exp(-hop_s / release_s)
    out = np.empty_like(env)
    y = env[0]
    for i, x in enumerate(env):
        a = a_att if x > y else a_rel
        y = a * y + (1 - a) * x
        out[i] = y
    return out


def level_voice(v: np.ndarray) -> np.ndarray:
    hop = int(0.005 * SR)
    win = int(0.05 * SR)
    power = np.convolve(v.astype(np.float64) ** 2, np.ones(win) / win, mode="same")[::hop]
    level_db = 10 * np.log10(power + 1e-12)
    thr, ratio = -24.0, 2.5
    over = np.maximum(0.0, level_db - thr)
    gain_db = -over * (1 - 1 / ratio)
    # only compress where there is speech (gates out breaths and silence)
    gain_db[level_db < -50] = 0.0
    # attack = gain going down quickly; smooth on the negated curve
    g = -smooth(-gain_db, 0.005, 0.015, 0.25)
    gain = 10 ** (np.interp(np.arange(len(v)) / hop, np.arange(len(g)), g) / 20)
    return (v * gain).astype(np.float32)


def speech_envelope(timeline: dict, n: int) -> np.ndarray:
    """1 while a word is being spoken (bridging gaps < 0.35 s), smoothed at control rate."""
    hop_s = 0.01
    m = np.zeros(int(n / SR / hop_s) + 1)
    words = [w for b in timeline["beats"] for w in b["words"]]
    for w0, w1 in zip(words, words[1:] + [None]):
        end = w1["start"] if w1 and w1["start"] - w0["end"] < 0.35 else w0["end"]
        m[int(w0["start"] / hop_s) : int(end / hop_s) + 1] = 1.0
    m = smooth(m, hop_s, 0.6, 1.2)
    return np.interp(np.arange(n) / SR / hop_s, np.arange(len(m)), m).astype(np.float32)


def sample_peaks(x: np.ndarray) -> np.ndarray:
    """Per-sample true peak (max over channels of the 4x-oversampled signal), in 10 s chunks."""
    out = np.empty(len(x), dtype=np.float32)
    step, pad = 10 * SR, 64
    for s in range(0, len(x), step):
        a, b = max(0, s - pad), min(len(x), s + step + pad)
        up = np.abs(resample_poly(x[a:b], 4, 1, axis=0)).max(axis=1).reshape(-1, 4).max(axis=1)
        out[s : min(len(x), s + step)] = up[s - a : s - a + min(step, len(x) - s)]
    return out


def true_peak_limit(x: np.ndarray, ceiling_db: float) -> np.ndarray:
    ceiling = 10 ** (ceiling_db / 20)
    peak = sample_peaks(x)
    need = np.minimum(1.0, ceiling / np.maximum(peak, 1e-9))
    look = int(0.005 * SR)
    # look-ahead: take the minimum gain over the next 5 ms, then release smoothly
    padded = np.concatenate([need, np.ones(look)])
    windows = np.lib.stride_tricks.sliding_window_view(padded, look + 1)[: len(need)]
    g = windows.min(axis=1)
    hop = 48
    gc = g[::hop]
    gc = -smooth(-gc, hop / SR, 0.001, 0.08)
    g = np.minimum(g, np.interp(np.arange(len(g)) / hop, np.arange(len(gc)), gc))
    return (x * g[:, None]).astype(np.float32)


def main() -> None:
    spec = json.loads(Path(sys.argv[1]).read_text())
    opts = spec.get("mix", {})
    target_lufs = opts.get("targetLufs", TARGET_LUFS)
    ceiling = opts.get("ceilingDbtp", CEILING_DBTP)
    under_db = opts.get("musicUnderVoiceDb", MUSIC_UNDER_VOICE_DB)
    duck_db = opts.get("duckDb", DUCK_DB)
    d = ROOT / "public" / "generated" / spec["id"]
    timeline = json.loads((d / "timeline.json").read_text())
    voice, vsr = sf.read(d / "narration.wav", dtype="float32")
    voice = level_voice(to_sr(voice if voice.ndim == 1 else voice.mean(axis=1), vsr))
    n = len(voice)
    meter = pyln.Meter(SR)

    mix = np.stack([voice, voice], axis=1)
    if (d / "music.wav").exists():
        music, msr = sf.read(d / "music.wav", dtype="float32")
        music = to_sr(music if music.ndim == 2 else np.stack([music, music], axis=1), msr)
        music = np.pad(music, ((0, max(0, n - len(music))), (0, 0)))[:n]
        v_lufs = meter.integrated_loudness(voice)
        m_lufs = meter.integrated_loudness(music)
        music *= 10 ** ((v_lufs - under_db - m_lufs) / 20)
        duck = 10 ** (-duck_db * speech_envelope(timeline, n) / 20)
        mix = mix + music * duck[:, None]

    lufs = meter.integrated_loudness(mix)
    mix *= 10 ** ((target_lufs - lufs) / 20)
    mix = true_peak_limit(mix, ceiling)

    sf.write(d / "mix.wav", mix, SR, subtype="PCM_24")

    # report: integrated loudness, true peak, and how even the voice is (short-term 3 s windows)
    final = meter.integrated_loudness(mix)
    tp = 20 * np.log10(float(sample_peaks(mix).max()) + 1e-12)
    st = []
    for s in range(0, n - 3 * SR, SR // 2):
        seg = mix[s : s + 3 * SR]
        if np.sqrt(np.mean(seg**2)) > 1e-3:
            st.append(meter.integrated_loudness(seg) if len(seg) >= 0.4 * SR else -70)
    st = np.array([x for x in st if np.isfinite(x) and x > -40])
    report = {
        "integratedLUFS": round(final, 2),
        "truePeakDBTP": round(float(tp), 2),
        "shortTermLUFS_p10_p50_p90": [round(float(np.percentile(st, q)), 1) for q in (10, 50, 90)],
        "shortTermSpreadLU_p90_minus_p10": round(float(np.percentile(st, 90) - np.percentile(st, 10)), 1),
    }
    (d / "mix.json").write_text(json.dumps(report, indent=1) + "\n")
    print(json.dumps(report))


if __name__ == "__main__":
    main()

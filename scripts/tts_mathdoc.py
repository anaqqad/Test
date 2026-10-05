#!/usr/bin/env python3
"""Narration + exact cut timeline for a MathDoc spec (Kokoro, a CosyVoice3 cloned voice, or ElevenLabs).

Usage:
    python3 scripts/tts_mathdoc.py data/mathdoc-eratosthenes.json

Unlike the fixed-duration documentary template, a MathDoc is timed by its voice-over:
every beat (one picture) is synthesized as its own clip, then the clips are joined with
measured-style pauses. Each picture cuts in CUT_LEAD seconds before the first word of its
beat, which is how the reference style lands cuts on the spoken word.

Word timestamps inside each clip come from faster-whisper (local) so "cues" (diagram steps
keyed to a spoken word) fire when that word is heard. Without faster-whisper installed, a
syllable-weighted estimate is used instead.

With "voice": {"engine": "elevenlabs", "voiceId": ...} the narration is synthesized one
section at a time instead (see tts_elevenlabs.py): continuous delivery, word times from the
API's character alignment, every section at the same loudness.

With "voice": {"engine": "cosyvoice", "sample": ..., "sampleText": ...} each beat is spoken in
a voice cloned from a short sample (see tts_cosyvoice.py), free and local.

Output (public/generated/<spec.id>/):
    narration.wav   the whole voice-over
    timeline.json   {fps, durationInFrames, beats: [{id, startFrame, endFrame, words, cues}]}
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tts_kokoro import MODEL_DIR, MODEL_FILES, ensure_model, trim_silence, word_timings  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CUT_LEAD = 0.1  # measured on the reference: cuts land ~0.09 s before the word
TAIL = 1.2  # hold on the last picture after the final word


def norm(w: str) -> str:
    return re.sub(r"[^a-z0-9]", "", w.lower())


def align_words(model, clip: np.ndarray, sr: int, text: str) -> list[dict]:
    """Return [{text, start, end}] in seconds relative to the clip, one per word of `text`."""
    words = text.split()
    if model is None:
        est = word_timings(text, 0, len(clip) / sr * 1000)
        return [{"text": w["text"], "start": w["startMs"] / 1000, "end": w["endMs"] / 1000} for w in est]
    import librosa

    audio16 = librosa.resample(clip, orig_sr=sr, target_sr=16000)
    segs, _ = model.transcribe(audio16, word_timestamps=True, beam_size=5, language="en")
    heard = [w for s in segs for w in s.words]
    # Map heard words onto script words in order; numbers may be heard differently
    # ("240" vs "two hundred forty"), so fall back to interpolation between anchors.
    out: list[dict | None] = [None] * len(words)
    j = 0
    for i, w in enumerate(words):
        target = norm(w)
        for k in range(j, min(j + 4, len(heard))):
            if norm(heard[k].word) == target:
                out[i] = {"text": w, "start": heard[k].start, "end": heard[k].end}
                j = k + 1
                break
    dur = len(clip) / sr
    anchors = [(-1, 0.0, 0.0)] + [(i, o["start"], o["end"]) for i, o in enumerate(out) if o] + [(len(words), dur, dur)]
    for (a, _, a_end), (b, b_start, _) in zip(anchors, anchors[1:]):
        gap = b - a - 1
        for n in range(1, gap + 1):
            t0 = a_end + (b_start - a_end) * (n - 1) / gap
            t1 = a_end + (b_start - a_end) * n / gap
            out[a + n] = {"text": words[a + n], "start": t0, "end": t1}
    return out  # type: ignore[return-value]


def load_whisper():
    try:
        from faster_whisper import WhisperModel

        return WhisperModel("small.en", device="cpu", compute_type="int8")
    except ImportError:
        print("faster-whisper not installed: using estimated word timings")
        return None


def join_beats(spec: dict, groups: list[tuple[list[int], np.ndarray]], sr: int, lead: float, whisper) -> tuple[np.ndarray, int, list[dict]]:
    """Join clips with clause/sentence/section pauses; word times via Whisper.

    Each clip speaks one or more consecutive beats (`groups` = [(beat indices, clip)]); its
    words are aligned once and handed back to the beats in order, so a beat inside a clip still
    starts on its own first word.
    """
    voice = spec["voice"]
    gap = voice.get("gapSeconds", 0.32)
    sentence_gap = voice.get("sentenceGapSeconds", 0.45)
    section_gap = voice.get("sectionGapSeconds", sentence_gap)
    parts: list[np.ndarray] = [np.zeros(int(lead * sr), dtype=np.float32)]
    t = lead
    beats = []
    for g, (idx, clip) in enumerate(groups):
        texts = [spec["beats"][i]["text"] for i in idx]
        words = align_words(whisper, clip, sr, " ".join(texts))
        k = 0
        for i, text in zip(idx, texts):
            n = len(text.split())
            mine = [{"text": w["text"], "start": round(t + w["start"], 3), "end": round(t + w["end"], 3)} for w in words[k : k + n]]
            k += n
            start = t if i == idx[0] else mine[0]["start"]
            beats.append({"id": spec["beats"][i]["id"], "speechStart": start, "words": mine})
        parts.append(clip)
        t += len(clip) / sr
        if g < len(groups) - 1:
            nxt = spec["beats"][groups[g + 1][0][0]]
            if nxt.get("section"):
                pause = section_gap
            else:
                pause = sentence_gap if texts[-1].rstrip()[-1] in ".?!" else gap
            parts.append(np.zeros(int(pause * sr), dtype=np.float32))
            t += pause
    audio = np.concatenate(parts)
    rms = float(np.sqrt(np.mean(audio**2))) or 1.0
    audio = audio * (10 ** (-18 / 20) / rms)
    peak = float(np.max(np.abs(audio)))
    if peak > 0.9:
        audio *= 0.9 / peak
    return audio, sr, beats


def kokoro_beats(spec: dict, lead: float) -> tuple[np.ndarray, int, list[dict]]:
    """One Kokoro clip per beat."""
    voice = spec["voice"]
    ensure_model()
    from kokoro_onnx import Kokoro

    kokoro = Kokoro(str(MODEL_DIR / MODEL_FILES[0]), str(MODEL_DIR / MODEL_FILES[1]))
    clips = []
    sr = 24000
    for beat in spec["beats"]:
        samples, sr = kokoro.create(beat["text"], voice=voice["voice"], speed=voice.get("speed", 1.0), lang="en-us")
        clips.append(trim_silence(np.asarray(samples, dtype=np.float32), sr))
        print(f"  {beat['id']}: {len(clips[-1]) / sr:.2f}s")
    return join_beats(spec, [([i], c) for i, c in enumerate(clips)], sr, lead, load_whisper())


def cosyvoice_beats(spec: dict, lead: float) -> tuple[np.ndarray, int, list[dict]]:
    """One cloned CosyVoice3 clip per sentence (see tts_cosyvoice.py)."""
    from tts_cosyvoice import synthesize

    whisper = load_whisper()
    groups, sr = synthesize(spec, whisper)
    return join_beats(spec, groups, sr, lead, whisper)


def main() -> None:
    spec_path = Path(sys.argv[1])
    spec = json.loads(spec_path.read_text())
    voice = spec["voice"]
    fps = spec.get("fps", 30)
    lead = voice.get("leadInSeconds", 0.25)
    engine = voice.get("engine", "kokoro")

    if engine == "elevenlabs":
        from tts_elevenlabs import synthesize

        audio, sr, beats = synthesize(spec, lead)
        engine_name = f"elevenlabs {voice.get('model', 'eleven_multilingual_v2')}"
        voice_name = voice.get("voiceName", voice["voiceId"])
    elif engine == "cosyvoice":
        audio, sr, beats = cosyvoice_beats(spec, lead)
        engine_name = "cosyvoice3 Fun-CosyVoice3-0.5B"
        voice_name = voice.get("voiceName", voice["sample"])
    else:
        audio, sr, beats = kokoro_beats(spec, lead)
        engine_name = "kokoro-onnx v1.0"
        voice_name = voice["voice"]

    # hold the last picture, then compute each beat's cue frames
    audio = np.concatenate([audio, np.zeros(int(TAIL * sr), dtype=np.float32)])
    total = len(audio) / sr
    for beat, b in zip(spec["beats"], beats):
        b["cues"] = {}
        for name, cue_word in beat.get("cues", {}).items():
            hit = next((w for w in b["words"] if norm(w["text"]) == norm(cue_word)), None)
            if hit is None:
                print(f"  ! beat '{beat['id']}': cue word '{cue_word}' not in narration")
                continue
            b["cues"][name] = round(hit["start"] * fps)

    # picture boundaries: each beat starts CUT_LEAD before its first word
    starts = [0] + [max(0, round((b["speechStart"] - CUT_LEAD) * fps)) for b in beats[1:]]
    duration_frames = round(total * fps)
    for k, b in enumerate(beats):
        b["startFrame"] = starts[k]
        b["endFrame"] = starts[k + 1] if k + 1 < len(beats) else duration_frames
        del b["speechStart"]

    out_dir = ROOT / "public" / "generated" / spec["id"]
    out_dir.mkdir(parents=True, exist_ok=True)
    sf.write(out_dir / "narration.wav", audio, sr)
    n_words = sum(len(b["words"]) for b in beats)
    timeline = {
        "fps": fps,
        "durationInFrames": duration_frames,
        "voice": voice_name,
        "engine": engine_name,
        "words": n_words,
        "wpm": round(n_words / (total / 60), 1),
        "beats": beats,
    }
    (out_dir / "timeline.json").write_text(json.dumps(timeline, indent=1) + "\n")
    print(f"Narration {total:.1f}s, {n_words} words, {timeline['wpm']} wpm -> {out_dir}")


if __name__ == "__main__":
    main()

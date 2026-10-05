"""ElevenLabs narration for MathDoc specs: one request per section, with character-level timings.

Used by tts_mathdoc.py when the spec says "voice": {"engine": "elevenlabs", ...}.

Why whole sections instead of one request per beat: every request restarts the voice's
intonation and level, which is audible as a bump every few seconds. One request per section
keeps the delivery continuous. The API's character alignment still gives each beat's exact start
time, so cuts stay locked to the spoken word. previous_text / next_text carry the intonation
across section joins.

Every section is loudness-normalised to the same target and gets 15 ms fades, so joins neither
jump in level nor click.

Responses are cached by content hash in .cache/elevenlabs/<spec id>/, so re-running with
unchanged text never bills again. Needs ELEVENLABS_API_KEY in the environment. The key is only
sent in the request header; it is never logged or written to disk.
"""

from __future__ import annotations

import base64
import hashlib
import io
import json
import os
import re
import time
import urllib.error
import urllib.request
from pathlib import Path

import numpy as np
import soundfile as sf

ROOT = Path(__file__).resolve().parent.parent
API = "https://api.elevenlabs.io/v1/text-to-speech/{voice}/with-timestamps?output_format={fmt}"
FORMAT = "mp3_44100_192"  # the best format below the Pro tier (PCM needs Pro)
SECTION_TARGET_LUFS = -20.0
FADE = 0.015
HEAD_PAD = 0.04  # keep this much before the first character
TAIL_PAD = 0.18  # and after the last one (the release of the final syllable)


def _request(voice: dict, text: str, prev_text: str, next_text: str) -> dict:
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        raise SystemExit("ELEVENLABS_API_KEY is not set")
    body = {
        "text": text,
        "model_id": voice.get("model", "eleven_multilingual_v2"),
        "voice_settings": {
            "stability": voice.get("stability", 0.55),
            "similarity_boost": voice.get("similarity", 0.75),
            "style": voice.get("style", 0.0),
            "use_speaker_boost": True,
            "speed": voice.get("speed", 1.0),
        },
        "previous_text": prev_text or None,
        "next_text": next_text or None,
        "seed": voice.get("seed", 1234),
    }
    url = API.format(voice=voice["voiceId"], fmt=FORMAT)
    for attempt in range(5):
        req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={"xi-api-key": key, "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            detail = e.read()[:300].decode(errors="replace")
            if e.code in (429, 500, 502, 503, 504) and attempt < 4:
                time.sleep(5 * (attempt + 1))
                continue
            raise SystemExit(f"ElevenLabs HTTP {e.code}: {detail}")
    raise SystemExit("ElevenLabs: too many retries")


def _cached(spec_id: str, voice: dict, text: str, prev_text: str, next_text: str) -> tuple[np.ndarray, int, dict]:
    settings = {k: voice.get(k) for k in ("voiceId", "model", "stability", "similarity", "style", "speed", "seed")}
    digest = hashlib.sha1(json.dumps([settings, FORMAT, text, prev_text, next_text]).encode()).hexdigest()[:16]
    cache = ROOT / ".cache" / "elevenlabs" / spec_id
    cache.mkdir(parents=True, exist_ok=True)
    mp3, meta = cache / f"{digest}.mp3", cache / f"{digest}.json"
    if not (mp3.exists() and meta.exists()):
        r = _request(voice, text, prev_text, next_text)
        mp3.write_bytes(base64.b64decode(r["audio_base64"]))
        meta.write_text(json.dumps(r["alignment"]))
        print(f"    synthesized {len(text)} chars")
    else:
        print(f"    cached ({len(text)} chars)")
    audio, sr = sf.read(io.BytesIO(mp3.read_bytes()), dtype="float32")
    if audio.ndim > 1:
        audio = audio.mean(axis=1)
    return audio, sr, json.loads(meta.read_text())


def _normalise(audio: np.ndarray, sr: int, target: float) -> np.ndarray:
    import pyloudnorm as pyln

    loud = pyln.Meter(sr).integrated_loudness(audio)
    if not np.isfinite(loud):
        return audio
    return audio * (10 ** ((target - loud) / 20))


def _fade(audio: np.ndarray, sr: int) -> np.ndarray:
    n = min(int(FADE * sr), len(audio) // 2)
    ramp = np.sin(np.linspace(0, np.pi / 2, n)) ** 2
    audio = audio.copy()
    audio[:n] *= ramp
    audio[-n:] *= ramp[::-1]
    return audio


def sections_of(beats: list[dict]) -> list[list[int]]:
    """Beat indices grouped into sections; a beat with "section" starts a new one."""
    groups: list[list[int]] = []
    for i, b in enumerate(beats):
        if i == 0 or b.get("section"):
            groups.append([])
        groups[-1].append(i)
    return groups


def synthesize(spec: dict, lead: float) -> tuple[np.ndarray, int, list[dict]]:
    """Return (mono audio, sample rate, per-beat {id, speechStart, speechEnd, words[]})."""
    voice = spec["voice"]
    beats = spec["beats"]
    groups = sections_of(beats)
    texts = [" ".join(beats[i]["text"].strip() for i in g) for g in groups]
    gap = voice.get("sectionGapSeconds", 1.0)
    parts: list[np.ndarray] = []
    out: list[dict] = [{} for _ in beats]
    sr_out = 44100
    t = lead
    for s, (group, text) in enumerate(zip(groups, texts)):
        prev_text = texts[s - 1][-300:] if s > 0 else ""
        next_text = texts[s + 1][:300] if s + 1 < len(texts) else ""
        name = beats[group[0]].get("section") or "intro"
        print(f"  section {s + 1}/{len(groups)} '{name}': {len(group)} beats")
        audio, sr, al = _cached(spec["id"], voice, text, prev_text, next_text)
        sr_out = sr
        chars, cs, ce = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
        if "".join(chars) != text:
            raise SystemExit(f"Alignment text mismatch in section {s + 1}")
        # trim to the speech, keeping a little air, then level and fade
        first = next(i for i, c in enumerate(chars) if not c.isspace())
        last = max(i for i, c in enumerate(chars) if not c.isspace())
        a0 = max(0.0, cs[first] - HEAD_PAD)
        a1 = min(len(audio) / sr, ce[last] + TAIL_PAD)
        clip = audio[int(a0 * sr) : int(a1 * sr)]
        clip = _fade(_normalise(clip, sr, SECTION_TARGET_LUFS), sr)
        offset = t - a0  # section-local time -> film time
        # beat character ranges inside the joined section text
        pos = 0
        for i in group:
            btext = beats[i]["text"].strip()
            start = text.index(btext, pos)
            words = []
            for m in re.finditer(r"\S+", btext):
                c0, c1 = start + m.start(), start + m.end() - 1
                words.append({"text": m.group(), "start": round(cs[c0] + offset, 3), "end": round(ce[c1] + offset, 3)})
            out[i] = {"id": beats[i]["id"], "speechStart": words[0]["start"], "speechEnd": words[-1]["end"], "words": words}
            pos = start + len(btext)
        parts.append(clip)
        t += len(clip) / sr
        if s + 1 < len(groups):
            parts.append(np.zeros(int(gap * sr), dtype=np.float32))
            t += gap
        print(f"    {len(clip) / sr:.1f}s")
    return np.concatenate([np.zeros(int(lead * sr_out), dtype=np.float32), *parts]), sr_out, out

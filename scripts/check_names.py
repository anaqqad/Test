#!/usr/bin/env python3
"""Check how Kokoro pronounces the names in a spec BEFORE the full narration run.

Usage:
    python scripts/check_names.py data/<spec>.json [extra term ...]

It collects every proper noun in the beats (runs of capitalized words, not counting the first word
of a sentence unless it is also capitalized elsewhere mid-sentence), plus any extra terms given,
speaks each one alone with Kokoro (applying the spec's "pronounce" respellings, same voice and speed),
transcribes it with faster_whisper and prints what was heard. A term that comes back different is
flagged with "!!": respell it in the spec's "pronounce" map (an easy phonetic spelling) and run again.
Whisper often misspells unusual but correctly spoken names, so read the flagged ones with judgment.
"""
from __future__ import annotations

import json
import re
import sys
import tempfile
from pathlib import Path

import numpy as np
import soundfile as sf

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from tts_kokoro import MODEL_DIR, MODEL_FILES, ensure_model, spoken  # noqa: E402

COMMON = {"The", "A", "An", "And", "But", "So", "Then", "In", "On", "At", "By", "Her", "His", "She", "He", "It", "That",
          "This", "They", "There", "When", "After", "Before", "For", "With", "Years", "Now", "One", "Two", "Three", "Subscribe",
          "Follow", "Black", "White", "Army", "Navy", "Hollywood", "Broadway", "America", "American", "Americans", "Congress",
          "President", "World", "War", "II", "I", "We", "You", "Our", "Its", "Days", "Weeks", "Months", "Not", "No", "Yes", "Of"}


def terms_from_spec(spec: dict) -> list[str]:
    found: dict[str, None] = {}
    for b in spec["beats"]:
        for sent in re.split(r"(?<=[.!?:])\s+", b["text"]):
            words = re.findall(r"[A-Z][\w'’.-]*(?:\s+(?:of|the|de|van|von|du|la)?\s*[A-Z][\w'’.-]*)*", sent)
            for i, w in enumerate(words):
                w = w.strip(".,'’")
                if sent.startswith(w) and w.split()[0] in COMMON:
                    rest = " ".join(w.split()[1:])
                    if not rest:
                        continue
                    w = rest
                if w in COMMON or len(w) < 3:
                    continue
                found[w] = None
    return list(found)


def norm(s: str) -> str:
    return re.sub(r"[^a-z ]", "", s.lower()).strip()


def main() -> None:
    spec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    terms = terms_from_spec(spec) + sys.argv[2:]
    voice = spec.get("voice", {})
    if voice.get("engine") not in (None, "kokoro"):
        voice = {"voice": "am_michael", "speed": 1.0}
    ensure_model()
    from kokoro_onnx import Kokoro
    from faster_whisper import WhisperModel

    kokoro = Kokoro(str(MODEL_DIR / MODEL_FILES[0]), str(MODEL_DIR / MODEL_FILES[1]))
    whisper = WhisperModel("small", device="cpu", compute_type="int8")
    tmp = Path(tempfile.gettempdir()) / "check_names.wav"
    flagged = 0
    for t in terms:
        said = spoken(t, spec.get("pronounce"))
        samples, sr = kokoro.create(said, voice=voice.get("voice", "am_michael"), speed=voice.get("speed", 1.0), lang="en-us")
        pad = np.zeros(int(sr * 0.3), dtype=samples.dtype)
        sf.write(tmp, np.concatenate([pad, samples, pad]), sr)
        segs, _ = whisper.transcribe(str(tmp), language="en")
        heard = " ".join(s.text for s in segs).strip()
        bad = norm(heard) != norm(t)
        flagged += bad
        print(f"{'!!' if bad else 'ok'} {t!r:32} spoken as {said!r:32} heard {heard!r}")
    print(f"{len(terms)} terms, {flagged} to listen to / respell")


if __name__ == "__main__":
    main()

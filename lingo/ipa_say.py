# Speak an IPA string with a Piper voice (no espeak text step): python3 ipa_say.py MODEL "ipa" out.wav [length_scale]
# Used only for the "simulated extinct languages" video; every clip is labelled as an AI simulation on screen.
import sys, wave, json, numpy as np
from piper import PiperVoice
from piper.config import SynthesisConfig

# phonemes a model may lack -> closest fallback sequence
FALLBACK = {"͡": "", "ʍ": "hw", "ʰ": "h", "l̩": "əl", "̩": "", "ħ": "h", "ʕ": "ʔ", "χ": "x", "ɬ": "l", "q": "k", "ʃ": "ʃ", "ɣ": "ɡ", "θ": "t", "ð": "d", "ɸ": "f", "β": "v", "ʷ": "w", "ˤ": "", "g": "ɡ"}


def ids_for(voice, ipa):
    idmap = voice.config.phoneme_id_map
    out, missing = [], set()
    for ch in ipa:
        if ch in idmap:
            out.append(ch)
        else:
            fb = FALLBACK.get(ch)
            if fb is None or any(c not in idmap for c in fb):
                missing.add(ch)
                continue
            out.extend(fb)
    return voice.phonemes_to_ids(out), missing


def say(model, ipa, dst, scale=1.0):
    voice = PiperVoice.load(model)
    ids, missing = ids_for(voice, ipa)
    audio = voice.phoneme_ids_to_audio(ids, SynthesisConfig(length_scale=scale))
    pcm = (np.clip(audio, -1, 1) * 32767).astype(np.int16)
    with wave.open(dst, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(voice.config.sample_rate); w.writeframes(pcm.tobytes())
    return missing


if __name__ == "__main__":
    m = say(sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]) if len(sys.argv) > 4 else 1.0)
    if m: print("missing phonemes:", " ".join(sorted(m)))

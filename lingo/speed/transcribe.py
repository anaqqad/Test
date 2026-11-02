"""Whisper transcript with word timings for each speed recording -> speed/out/<key>.json"""
import json, os, sys
from faster_whisper import WhisperModel, decode_audio
HERE = os.path.dirname(os.path.abspath(__file__)); os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
LANG = {"jpn": "ja", "spa": "es", "fra": "fr", "ita": "it", "eng": "en", "deu": "de", "vie": "vi", "cmn": "zh"}
m = WhisperModel(sys.argv[1] if len(sys.argv) > 1 else "small", compute_type="int8")
for k, lg in LANG.items():
    a = decode_audio(os.path.join(HERE, "..", "incoming", "speed", k + ".wav"))[: 16000 * 120]
    segs, info = m.transcribe(a, language=lg, word_timestamps=True, beam_size=5, vad_filter=False, condition_on_previous_text=False)
    out = [{"start": s.start, "end": s.end, "text": s.text, "words": [[w.start, w.end, w.word] for w in s.words]} for s in segs]
    json.dump(out, open(os.path.join(HERE, "out", k + ".json"), "w"), ensure_ascii=False, indent=1)
    print(k, len(out), "segments;", " ".join(s["text"] for s in out)[:220], flush=True)

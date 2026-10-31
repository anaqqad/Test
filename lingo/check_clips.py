"""Transcribe each cut clip with Whisper to catch clips that are really English (intro/outro talk)."""
import sys, glob, os
from faster_whisper import WhisperModel
m = WhisperModel("base", device="cpu", compute_type="int8")
for v in sys.argv[1:]:
    for f in sorted(glob.glob(f"cache/audio/{v}/*.wav")):
        segs, info = m.transcribe(f, beam_size=1)
        text = " ".join(s.text for s in segs)[:160]
        print(f"{v}/{os.path.basename(f):28s} {info.language} {info.language_probability:.2f} | {text}")

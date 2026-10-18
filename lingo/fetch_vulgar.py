# Audio for "Ranking the World's Most Vulgar Languages": python3 fetch_vulgar.py
# One Lingua Libre recording per language (vulgar.json "rec"), trimmed and loudness-matched, with the speaker's pitch
# (to pick a Wojak of the right gender). Writes cache/audio/vulgar/<key>.wav, manifest.json and out/vulgar_credits.txt.
import json, os
import numpy as np, parselmouth
import fetch_audio as fa
import fetch_pairs as fp

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "vulgar.json")))
OUT = os.path.join(HERE, "cache", "audio", "vulgar")
os.makedirs(OUT, exist_ok=True)
man, credits = {}, []
for it in D["items"]:
    dst = os.path.join(OUT, it["key"] + ".wav")
    if not it.get("rec") and it.get("tts"):  # no native recording exists: a Piper AI voice reads the word (labelled on screen)
        import wave
        from piper import PiperVoice, SynthesisConfig
        raw = os.path.join(OUT, it["key"] + "_raw.wav")
        with wave.open(raw, "wb") as w:
            PiperVoice.load(os.path.join(HERE, "cache", "voices", it["tts"] + ".onnx")).synthesize_wav(it.get("tts_text", it["word"]), w, SynthesisConfig(length_scale=1.0))
        fa.to_wav(raw, dst, extra="silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,loudnorm=I=-18:TP=-2")
        m = {"title": "AI voice", "artist": "Piper TTS voice " + it["tts"], "license": "MIT", "page": "https://github.com/rhasspy/piper"}
    elif it.get("rec"):
        m = fp.clip(it["rec"], dst)
    else:
        m = None
    if not m:
        man[it["key"]] = None; print(it["key"], "no recording"); continue
    # punch: compress and lift the word so it lands harder than the rest of the mix
    import subprocess
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", dst, "-af", "acompressor=threshold=-20dB:ratio=4:attack=5:release=80,volume=6dB,alimiter=limit=0.95", dst + ".p.wav"], check=True)
    os.replace(dst + ".p.wav", dst)
    p = parselmouth.Sound(dst).to_pitch(pitch_floor=60, pitch_ceiling=400).selected_array["frequency"]; p = p[p > 0]
    f0 = int(np.median(p)) if len(p) else 0
    man[it["key"]] = {"d": round(fa.duration(dst), 2), "f0": f0, "voice": "female" if f0 > 165 else "male", "ai": not it.get("rec"), "credit": m}
    if it.get("rec"): credits.append(f"{it['name']}: \"{m['title'][5:]}\" by {m['artist']}, {m['license']}, via Wikimedia Commons, {m['page']}")
    print(it["key"], man[it["key"]]["d"], "s, F0", f0, man[it["key"]]["voice"], flush=True)
json.dump(man, open(os.path.join(OUT, "manifest.json"), "w"), indent=1, ensure_ascii=False)
open(os.path.join(HERE, "out", "vulgar_credits.txt"), "w").write("Audio credits (Ranking the World's Most Vulgar Languages)\n\n" + "\n".join(credits) + "\n")

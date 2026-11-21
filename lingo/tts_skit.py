"""Synthesize every skit line with Piper (free, open-source TTS) and build the timeline.
  python3 tts_skit.py skit_a2.mjs -> cache/skit/<key>/*.wav + timeline.json
The timeline stores each line's start, duration and a per-frame "mouth open" track (from loudness),
so the avatar's mouth moves with the voice."""
import json, os, subprocess, sys, wave
import numpy as np
from piper import PiperVoice, SynthesisConfig

HERE = os.path.dirname(os.path.abspath(__file__))
FPS = 30
GAP = 0.35          # pause between lines
SCENE_PAD = (1.0, 1.0)  # silence before the first / after the last line of a scene


def main(path):
    skit = json.loads(subprocess.run(["node", "-e", f"import('./{path}').then(m=>console.log(JSON.stringify(m.SKIT)))"],
                                     cwd=HERE, capture_output=True, text=True, check=True).stdout)
    out = os.path.join(HERE, "cache", "skit", skit["key"])
    os.makedirs(out, exist_ok=True)
    voices = {}
    tl = {"scenes": []}
    for si, sc in enumerate(skit["scenes"]):
        t = SCENE_PAD[0]
        lines = []
        for li, line in enumerate(sc["lines"]):
            who, text = line[0], line[1]
            v = skit["voices"][who]
            if v["model"] not in voices:
                voices[v["model"]] = PiperVoice.load(os.path.join(HERE, "cache", "voices", v["model"] + ".onnx"))
            wav = os.path.join(out, f"{si:02d}_{li:02d}.wav")
            sig = f"{text}|{v}"
            if not (os.path.exists(wav) and os.path.exists(wav + ".sig") and open(wav + ".sig").read() == sig):
                with wave.open(wav, "wb") as w:
                    voices[v["model"]].synthesize_wav(text, w, syn_config=SynthesisConfig(length_scale=v["speed"]))
                open(wav + ".sig", "w").write(sig)
            with wave.open(wav) as w:
                sr, n = w.getframerate(), w.getnframes()
                a = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float32) / 32768
            dur = n / sr
            hop = sr // FPS
            rms = np.array([np.sqrt((a[i:i + hop] ** 2).mean() + 1e-12) for i in range(0, len(a) - hop + 1, hop)])
            mouth = "".join("1" if r > 0.035 else "0" for r in rms)
            lines.append({"who": who, "text": text, "start": round(t, 3), "dur": round(dur, 3), "wav": wav, "mouth": mouth,
                          "fx": line[2] if len(line) > 2 else None, "opts": line[3] if len(line) > 3 else {}})
            t += dur + GAP
        tl["scenes"].append({"dur": round(t - GAP + SCENE_PAD[1], 3), "lines": lines})
        print(f"scene {si} {sc['label']}: {t:.1f}s, {len(lines)} lines", flush=True)
    json.dump(tl, open(os.path.join(out, "timeline.json"), "w"), indent=1, ensure_ascii=False)
    print("total", round(sum(s["dur"] for s in tl["scenes"]), 1), "s")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "skit_a2.mjs")

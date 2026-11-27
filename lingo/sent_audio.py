# Audio for the sentence video: python3 sent_audio.py [pair ...]
# The sentence of language A, then of language B, read by Piper AI voices (sent_pairs.json "voices"), trimmed and
# loudness-matched. Writes cache/audio/sent/<pair>.wav and manifest.json (captions with side/start/duration, scores).
import json, os, subprocess, sys, wave
from piper import PiperVoice, SynthesisConfig
import fetch_audio as fa
import sent_score as ss

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "sent_pairs.json")))
OUT = os.path.join(HERE, "cache", "audio", "sent")
RAW = os.path.join(HERE, "cache", "sent")
os.makedirs(OUT, exist_ok=True); os.makedirs(RAW, exist_ok=True)
LEAD, GAP, TAIL = 0.8, 1.0, 0.6
SPEED = {"ces": 0.9, "nld": 0.9, "ukr": 0.9}  # a touch faster for the slowest voices


def say(code):
    model = D["voices"][code]
    raw, dst = os.path.join(RAW, f"{code}_raw.wav"), os.path.join(RAW, f"{code}.wav")
    if not os.path.exists(dst):
        v = PiperVoice.load(os.path.join(HERE, "cache", "voices", model + ".onnx"))
        with wave.open(raw, "wb") as w:
            v.synthesize_wav(D["sentences"][code], w, SynthesisConfig(length_scale=SPEED.get(code, 1.0)))
        fa.to_wav(raw, dst, extra="silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,loudnorm=I=-18:TP=-2")
    return dst


def build(pk, p):
    t, parts, caps = LEAD, [], []
    for side in ("a", "b"):
        f = say(p[side]); d = fa.duration(f)
        caps.append({"side": side, "t": round(t, 2), "d": round(d, 2)})
        parts.append((t, f)); t += d + GAP
    total = t - GAP + TAIL
    ins, filt = [], []
    for i, (st, f) in enumerate(parts):
        ins += ["-i", f]; filt.append(f"[{i}]adelay={int(st * 1000)}|{int(st * 1000)}[a{i}]")
    filt.append(f"[a0][a1]amix=inputs=2:normalize=0,apad,atrim=0:{total:.2f}[out]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(filt), "-map", "[out]", "-ar", str(fa.SR), os.path.join(OUT, pk + ".wav")], check=True)
    return {"captions": caps, "len": round(total, 2), "score": ss.score(pk)}


if __name__ == "__main__":
    mpath = os.path.join(OUT, "manifest.json")
    manifest = json.load(open(mpath)) if os.path.exists(mpath) else {}
    for pk in sys.argv[1:] or D["pairs"]:
        manifest[pk] = build(pk, D["pairs"][pk])
        print(pk, manifest[pk]["len"], "s", [c["d"] for c in manifest[pk]["captions"]])
    json.dump(manifest, open(mpath, "w"), indent=1, ensure_ascii=False)

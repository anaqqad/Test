# Simulated audio for videos whose items use audio.sim: python3 sim_audio.py ancient
# Each phrase (IPA from a scholarly reconstruction) is read by a Piper voice; it is repeated until it lasts ~8 s,
# and word captions are timed by each word's share of the phonemes.
import json, math, os, subprocess, sys, wave
from ipa_say import say

HERE = os.path.dirname(os.path.abspath(__file__))
VOICES = os.path.join(HERE, "cache", "voices")
SR, GAP, MIN_LEN, MAX_REPS = 48000, 0.9, 8.0, 3


def wav_len(p):
    with wave.open(p) as w:
        return w.getnframes() / w.getframerate()


def lead_trail(p):
    """Leading and trailing silence (s) of a mono wav, so captions line up with the voice."""
    import numpy as np
    with wave.open(p) as w:
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float) / 32768
        sr = w.getframerate()
    loud = np.where(np.abs(a) > 0.02)[0]
    return (loud[0] / sr, (len(a) - loud[-1]) / sr) if len(loud) else (0, 0)


def process(vkey, video):
    outdir = os.path.join(HERE, "cache", "audio", vkey)
    os.makedirs(outdir, exist_ok=True)
    mpath = os.path.join(outdir, "manifest.json")
    manifest = {}
    for item in video["items"]:
        sim = (item.get("audio") or {}).get("sim")
        if not sim:
            continue
        name = item["name"]
        slug = "".join(c if c.isalnum() else "_" for c in name.lower())
        one = os.path.join(outdir, slug + "_once.wav")
        ipa = " ".join(w[1] for w in sim["words"])
        missing = say(os.path.join(VOICES, sim["model"] + ".onnx"), ipa, one, sim.get("scale", 1.0))
        if missing:
            print(f"  {name}: phonemes the voice lacks (dropped): {' '.join(sorted(missing))}")
        d = wav_len(one)
        lead, trail = lead_trail(one)
        reps = min(MAX_REPS, max(1, math.ceil((MIN_LEN + GAP) / (d + GAP))))
        caps, t = [], 0.6
        weights = [max(1, sum(ch.isalpha() or ch == "ː" for ch in w[1])) for w in sim["words"]]
        speech = d - lead - trail
        for r in range(reps):
            u = t + lead
            for (shown, _), wgt in zip(sim["words"], weights):
                dur = speech * wgt / sum(weights)
                caps.append({"t": round(u, 2), "d": round(dur, 2), "text": shown})
                u += dur
            t += d + GAP
        dst = os.path.join(outdir, slug + ".wav")
        ins = []
        for r in range(reps):
            ins += ["-i", one]
        filt = "".join(f"[{r}]aresample={SR},apad=pad_dur={GAP}[a{r}];" for r in range(reps))
        filt += "".join(f"[a{r}]" for r in range(reps)) + f"concat=n={reps}:v=0:a=1,adelay=600,pan=stereo|c0=c0|c1=c0,loudnorm=I=-18:TP=-2[o]"
        subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", filt, "-map", "[o]", "-ar", str(SR), dst], check=True)
        os.remove(one)
        manifest[name] = {"sig": json.dumps(sim, ensure_ascii=False), "credits": [], "captions": caps, "sim": True, "model": sim["model"], "reps": reps}
        print(f"  {name}: {d:.1f}s x{reps} ({sim['model']})")
    json.dump(manifest, open(mpath, "w"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    videos = json.loads(subprocess.run(["node", "-e", "import('./videos.mjs').then(m=>console.log(JSON.stringify(m.VIDEOS)))"], cwd=HERE, capture_output=True, text=True, check=True).stdout)
    for k in sys.argv[1:]:
        process(k, videos[k])

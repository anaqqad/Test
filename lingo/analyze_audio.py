"""Per clip: where the voice really ends, and whether the voice is male or female (median pitch).
  python3 analyze_audio.py [video ...] -> cache/audio/<video>/analysis.json, printed table.
Pitch: autocorrelation F0 on voiced 40 ms frames; median under 165 Hz = male. An override in videos.mjs
(audio.voice: "m" | "f") wins, for singing, whistling, children or mixed recordings."""
import json, os, re, subprocess, sys
import numpy as np

SR = 16000


def load(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"], capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768


def voice_end(a, thr_db=-38):
    hop = SR // 50
    rms = np.array([np.sqrt((a[i:i + hop] ** 2).mean() + 1e-12) for i in range(0, len(a) - hop, hop)])
    loud = np.where(20 * np.log10(rms + 1e-9) > thr_db)[0]
    return (loud[-1] + 1) * hop / SR if len(loud) else 0.0


def f0_median(a):
    win, hop = int(0.04 * SR), int(0.01 * SR)
    lo, hi = SR // 350, SR // 70
    f0s = []
    for i in range(0, len(a) - win, hop):
        x = a[i:i + win]
        if np.sqrt((x ** 2).mean()) < 0.02:
            continue
        x = x - x.mean()
        ac = np.correlate(x, x, "full")[win - 1:]
        if ac[0] <= 0:
            continue
        ac = ac / ac[0]
        lag = lo + int(np.argmax(ac[lo:hi]))
        if ac[lag] > 0.45:
            f0s.append(SR / lag)
    return (float(np.median(f0s)), len(f0s)) if f0s else (0.0, 0)


def slug(name):
    return re.sub(r"[^\w]+", "_", name).strip("_").lower()


def main(videos):
    vids = json.loads(subprocess.run(["node", "-e", "import('./videos.mjs').then(m=>console.log(JSON.stringify(m.VIDEOS)))"],
                                     capture_output=True, text=True, check=True).stdout)
    for v in videos:
        out = {}
        for it in vids[v]["items"]:
            wav = f"cache/audio/{v}/{slug(it['name'])}.wav"
            if not os.path.exists(wav):
                continue
            a = load(wav)
            end = voice_end(a)
            f0, n = f0_median(a)
            g = (it.get("audio") or {}).get("voice") or ("?" if n < 50 else "m" if f0 < 165 else "f")
            char_g = "f" if it["char"].get("fem") else "m"
            out[it["name"]] = {"end": round(end, 2), "f0": round(f0), "frames": n, "voice": g}
            flag = "  -> avatar becomes " + g if g in ("m", "f") and g != char_g else ""
            print(f"{v:9s} {it['name']:22s} end {end:5.1f}s  f0 {f0:4.0f}Hz ({n:4d})  voice {g}  avatar {char_g}{flag}")
        json.dump(out, open(f"cache/audio/{v}/analysis.json", "w"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main(sys.argv[1:])

# Audio for "Words That Don't Exist in English be like": python3 fetch_untrans.py
# Per word: the native recording (Wiktionary pronunciation file on Commons, untrans.json "rec", downloaded as the mp3
# transcode), peak-normalised; and the English translation read by a Piper AI voice (labelled on screen).
# Writes cache/audio/untrans/<key>_w.wav, <key>_en.wav, manifest.json and out/untrans_credits.txt.
import hashlib, json, os, re, subprocess, time, urllib.parse, wave
import numpy as np, parselmouth
from piper import PiperVoice, SynthesisConfig
import fetch_audio as fa

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "untrans.json")))
OUT = os.path.join(HERE, "cache", "audio", "untrans")
RAW = os.path.join(HERE, "cache", "raw")
os.makedirs(OUT, exist_ok=True); os.makedirs(RAW, exist_ok=True)
UA = "LingoDudeVideoBot/0.1 (contact: lingodude channel)"


def download(title):
    """Commons transcoded mp3 of a File: title (the originals are throttled much harder)"""
    name = title[5:].replace(" ", "_")
    dst = os.path.join(RAW, re.sub(r"[^\w.-]", "_", name)[:80] + ".mp3")
    if os.path.exists(dst) and os.path.getsize(dst) > 500:
        return dst
    h = hashlib.md5(name.encode()).hexdigest(); q = urllib.parse.quote(name)
    url = f"https://upload.wikimedia.org/wikipedia/commons/transcoded/{h[0]}/{h[:2]}/{q}/{q}.mp3"
    hdr = os.path.join(RAW, "_hdr.txt")
    for i in range(12):
        r = subprocess.run(["curl", "-s", "-D", hdr, "-w", "%{http_code}", "-A", UA, "-o", dst, url], capture_output=True, text=True)
        if r.stdout == "200" and fa.duration(dst) > 0.05:
            return dst
        if os.path.exists(dst): os.remove(dst)
        if r.stdout == "404" and i >= 4: return None  # a transcode is generated on the first request; give it a few tries
        ra = re.search(r"(?im)^retry-after:\s*(\d+)", open(hdr).read())
        time.sleep(min(60, int(ra.group(1)) + 1) if ra else 12)
    return None


def punch(dst):
    r = subprocess.run(["ffmpeg", "-i", dst, "-af", "volumedetect", "-f", "null", "-"], capture_output=True, text=True)
    peak = float(re.search(r"max_volume: (-?[\d.]+) dB", r.stderr).group(1))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", dst, "-af", f"volume={-1 - peak:.1f}dB,acompressor=threshold=-14dB:ratio=3:attack=5:release=80:makeup=2,alimiter=limit=0.95", dst + ".p.wav"], check=True)
    os.replace(dst + ".p.wav", dst)


man, credits = {}, []
en = PiperVoice.load(os.path.join(HERE, "cache", "voices", D["english_voice"] + ".onnx"))
for it in D["items"]:
    k = it["key"]
    src = download(it["rec"])
    if not src:
        print(k, "recording not found:", it["rec"]); man[k] = None; continue
    w = os.path.join(OUT, k + "_w.wav")
    fa.to_wav(src, w, extra="silenceremove=start_periods=1:start_threshold=-42dB,areverse,silenceremove=start_periods=1:start_threshold=-42dB,areverse")
    punch(w)
    p = parselmouth.Sound(w).to_pitch(pitch_floor=60, pitch_ceiling=400).selected_array["frequency"]; p = p[p > 0]
    f0 = int(np.median(p)) if len(p) else 0
    raw = os.path.join(OUT, k + "_en_raw.wav"); e = os.path.join(OUT, k + "_en.wav")
    with wave.open(raw, "wb") as wv:
        en.synthesize_wav(it["translation"], wv, SynthesisConfig(length_scale=1.05))
    fa.to_wav(raw, e, extra="silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,loudnorm=I=-17:TP=-2")
    nwords = len(re.findall(r"[A-Za-z'’-]+", it["translation"]))
    man[k] = {"dw": round(fa.duration(w), 2), "de": round(fa.duration(e), 2), "f0": f0, "voice": "female" if f0 > 165 else "male", "words": nwords}
    c = it["credit"]
    credits.append(f"{it['name']} ({it['word']}): \"{it['rec'][5:]}\" by {c['artist']}, {c['license']}, via Wikimedia Commons, https://commons.wikimedia.org/wiki/{urllib.parse.quote(it['rec'].replace(' ', '_'))}")
    print(k, man[k], flush=True)
json.dump(man, open(os.path.join(OUT, "manifest.json"), "w"), indent=1, ensure_ascii=False)
open(os.path.join(HERE, "out", "untrans_credits.txt"), "w").write("Audio credits (Words That Don't Exist in English)\n\n" + "\n".join(credits) + "\n")

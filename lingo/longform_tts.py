# Narration for long-form episodes with Kokoro (local, free; voice chosen by the owner).
#   python3.13 longform_tts.py <key> --voice <name or path/to/voice.pt> [--speed 1.0] [--only id1,id2] [--force]
# Reads longform/<key>/episode.mjs (via node), writes cache/longform/<key>/vo/<id>.wav (48 kHz mono, trimmed).
# Pronunciation fixes for names/foreign words live in SAY below (respellings, applied only to what Kokoro reads).
import argparse, json, os, re, subprocess, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SAY = {  # what Kokoro reads instead (the on-screen text is unchanged)
    "Caxaro": "Ka-sharo", "Kantilena": "Kanti-layna", "Giliberto Abbate": "Jili-bairto Ab-bahtay", "al-Himyari": "al-Him-yaari",
    "Agius de Soldanis": "Ah-joos deh Sol-dah-nis", "Mifsud": "Mif-sood", "Micallef": "Mika-lef", "Zammit": "Zam-mit",
    "Lucera": "Loo-chair-a", "Siculo-Arabic": "Sickulo-Arabic", "Ktieb": "K-teeb", "Kittieb": "Kit-teeb",
    "kitaab": "kitahb", "kaatib": "kah-tib", "jazeera": "ja-zeera", "Alla jbierek": "Alla yibb-ee-rek", "Alla": "Alla",
}

ap = argparse.ArgumentParser()
ap.add_argument("key"); ap.add_argument("--voice", required=True); ap.add_argument("--speed", type=float, default=1.0)
ap.add_argument("--only", default=""); ap.add_argument("--force", action="store_true")
a = ap.parse_args()
ep = json.loads(subprocess.run(["node", "-e", f"import('./longform/{a.key}/episode.mjs').then(m=>console.log(JSON.stringify(m.default.lines.map(l=>({{id:l.id,say:l.say}})))))"],
                               cwd=HERE, capture_output=True, text=True, check=True).stdout)
vname = os.path.splitext(os.path.basename(a.voice))[0]
out = os.path.join(HERE, "cache", "longform", a.key, "vo_" + vname); os.makedirs(out, exist_ok=True)  # one folder per voice
only = set(filter(None, a.only.split(",")))

from kokoro import KPipeline
voice = a.voice
lang = "b" if os.path.basename(voice).startswith("b") else "a"   # bf_/bm_ voices are British English
pipe = KPipeline(lang_code=lang, repo_id="hexgrad/Kokoro-82M")
if voice.endswith(".pt"):
    import torch; voice = torch.load(voice, weights_only=True)

def fix(text):
    for k in sorted(SAY, key=len, reverse=True):
        text = re.sub(r"(?<![\w-])" + re.escape(k) + r"(?![\w-])", SAY[k], text)
    return text

for line in ep:
    f = os.path.join(out, line["id"] + ".wav")
    if (only and line["id"] not in only) or (os.path.exists(f) and not a.force and not only):
        continue
    chunks = [aud.numpy() if hasattr(aud, "numpy") else np.asarray(aud) for _, _, aud in pipe(fix(line["say"]), voice=voice, speed=a.speed)]
    wav = np.concatenate(chunks).astype(np.float32)
    tmp = f + ".f32"; wav.tofile(tmp)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", "24000", "-ac", "1", "-i", tmp, "-af",
                    "silenceremove=start_periods=1:start_threshold=-50dB,areverse,silenceremove=start_periods=1:start_threshold=-50dB,areverse",
                    "-ar", "48000", f], check=True)
    os.remove(tmp)
    print(line["id"], round(len(wav) / 24000, 2), "s", flush=True)

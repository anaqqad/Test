# QA for a long-form render: python3 longform_qa.py <key> <tag>   (e.g. malta3 malta3_v3)
# 1. Headphones: loudness, true peak, and level of every stem (cache/longform/<key>/stems_<tag>/).
# 2. Phone speaker: the mix band-limited to 350-4500 Hz, mono, with soft clipping. Whisper must still recover the narration,
#    and every native word must stand at least 6 dB above the score+ambience beneath it.
# 3. Muted watch: a contact sheet every 10 s (out/qa_<tag>_muted.jpg) to check that captions and labels carry the story.
# 4. Audio only: lines whose meaning rests on a picture alone (no narration and no heard word) are listed.
# Writes out/qa_<tag>.txt.
import json, os, subprocess, sys
import numpy as np

key, tag = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
C = os.path.join(HERE, "cache", "longform", key)
mp4 = os.path.join(HERE, "out", tag + ".mp4")
proj = json.load(open(os.path.join(C, f"project_{tag}.json")))
SR = 16000
rep = [f"QA {tag}"]

def wav(f, af=None):
    cmd = ["ffmpeg", "-v", "error", "-i", f] + (["-af", af] if af else []) + ["-ac", "1", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32)
def db(a): return 20 * np.log10(np.sqrt(np.mean(a.astype(np.float64) ** 2)) + 1e-9)

# 1. loudness
m = subprocess.run(["ffmpeg", "-v", "info", "-i", mp4, "-af", "loudnorm=print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
m = json.loads(m[m.rindex("{"): m.rindex("}") + 1])
rep.append(f"1. Headphones: {m['input_i']} LUFS integrated, true peak {m['input_tp']} dBTP, LRA {m['input_lra']} LU (target -16 / -1.5)")
st = {k: wav(os.path.join(C, "stems_" + tag, k + ".wav")) for k in ["vo", "words", "amb", "sfx", "score"]}
for k, a in st.items(): rep.append(f"   stem {k:5s} RMS over active parts {db(a[np.abs(a) > 1e-4]) if np.any(np.abs(a) > 1e-4) else -99:6.1f} dBFS")

# 2. phone speaker
phone = os.path.join(C, f"phone_{tag}.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp4, "-af", "highpass=f=350,highpass=f=350,lowpass=f=4500,lowpass=f=4500,asoftclip=type=tanh,volume=-3dB", "-ac", "1", "-ar", "16000", phone], check=True)
from faster_whisper import WhisperModel
wm = WhisperModel("small", compute_type="int8")
segs, _ = wm.transcribe(phone, language="en")
heard = " ".join(s.text for s in segs).lower()
import re
words = lambda t: re.findall(r"[a-z]+", t.lower())
ref = [w for r in proj["timeline"] if r.get("say") and r["t1"] <= proj["mix"]["end"] + 0.5 for w in words(r["say"])]
hw = set(words(heard)); hit = sum(1 for w in ref if w in hw)
rep.append(f"2. Phone speaker: Whisper recovers {hit}/{len(ref)} narration words ({100 * hit / len(ref):.0f} %)")
bed = st["score"] + st["amb"]
low = []
for it in proj["mix"]["items"]:
    if it["track"] != "words": continue
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", it["f"]], capture_output=True, text=True).stdout)
    i0, i1 = int(it["t"] * SR), int((it["t"] + d) * SR)
    margin = db(st["words"][i0:i1]) - db(bed[i0:i1])
    if margin < 6: low.append(f"{os.path.basename(it['f'])} at {it['t']:.1f}s ({margin:.1f} dB)")
rep.append("   native words at least 6 dB over the bed: " + ("all" if not low else "NO: " + "; ".join(low)))

# 3. muted
sheet = os.path.join(HERE, "out", f"qa_{tag}_muted.jpg")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp4, "-vf", "fps=1/10,scale=384:-1,tile=8x7", "-frames:v", "1", "-an", sheet], check=True)
rep.append(f"3. Muted watch: contact sheet {os.path.relpath(sheet, HERE)} (one frame every 10 s)")

# 4. audio only
silent = [r["id"] for r in proj["timeline"] if not r.get("say") and r["t0"] < proj["mix"]["end"]]
rep.append("4. Audio only: lines with no narration (meaning carried by the recording or the picture): " + ", ".join(silent))
# 5. shot lengths, measured on the actual render: scene-cut detection (cuts) + the renderer's shot list (planned cuts)
sh = os.path.join(C, f"shots_{tag}.json")
if os.path.exists(sh):
    import re as _re
    plan = json.load(open(sh))
    det = subprocess.run(["ffmpeg", "-v", "info", "-i", mp4, "-an", "-vf", "scale=320:-2,select='gt(scene,0.12)',showinfo", "-f", "null", "-"], capture_output=True, text=True).stderr
    cuts = sorted(float(x) for x in _re.findall(r"pts_time:([0-9.]+)", det))
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mp4], capture_output=True, text=True).stdout)
    edges = [0.0] + cuts + [dur]; gaps = [(edges[i], edges[i + 1] - edges[i]) for i in range(len(edges) - 1)]
    # a planned cut the detector missed (two similar compositions) still counts as a cut: merge both lists
    allc = sorted(set([round(c, 1) for c in cuts] + [round(x["t0"], 1) for x in plan if x["t0"] > 0.2]))
    e2 = [0.0] + allc + [dur]; g2 = [(e2[i], e2[i + 1] - e2[i]) for i in range(len(e2) - 1)]
    longd = max(g2, key=lambda x: x[1])
    over = [f"{int(a // 60)}:{a % 60:04.1f} ({d:.1f} s)" for a, d in g2 if d > 5.05]
    rep.append(f"5. Five-second rule: {len(plan)} planned shots (longest {max(x['d'] for x in plan):.2f} s); {len(cuts)} cuts detected in the MP4; "
               f"longest stretch between cuts {longd[1]:.2f} s at {int(longd[0] // 60)}:{longd[0] % 60:04.1f}; over 5 s: {', '.join(over) if over else 'none'}")
    missed = [x for x in plan if x["t0"] > 0.2 and not any(abs(c - x["t0"]) < 0.25 for c in cuts)]
    rep.append(f"   planned cuts not seen by the detector (similar compositions, check by eye): {len(missed)}" + ("".join(f"\n     {int(x['t0'] // 60)}:{x['t0'] % 60:04.1f} {x['line']} {x['kind']} {x['what']}" for x in missed[:40])))
    # 6. flashes: a picture on screen for under 0.5 s between two detected cuts (the v4 flash at 6:27 was 0.3 s of a stale map)
    fl = [f"{int(a // 60)}:{a % 60:04.1f} ({d:.2f} s)" for a, d in gaps if d < 0.5 and a > 0.2]
    rep.append("6. Flashes (under 0.5 s between detected cuts): " + (", ".join(fl) if fl else "none"))
open(os.path.join(HERE, "out", f"qa_{tag}.txt"), "w").write("\n".join(rep) + "\n")
print("\n".join(rep))

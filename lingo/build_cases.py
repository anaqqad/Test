# Audio for "Ranking Languages by How Many Grammar Cases They Have": python3 build_cases.py
# 1) joins the Lingua Libre case forms of one noun (same speaker) into incoming/cases/seq_<key>.wav,
# 2) runs fetch_vulgar.py cases (clips, loudness, voice pitch), 3) rewrites out/cases_credits.txt with every file used.
import json, os, subprocess, urllib.parse
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "incoming", "cases")
D = json.load(open(os.path.join(HERE, "cases.json")))
GAP = 0.45
for it in D["items"]:
    seq = it.get("seq")
    if not seq: continue
    parts = []
    for i, f in enumerate(seq):
        out = os.path.join(SRC, f"_part_{it['key']}_{i}.wav")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(SRC, f), "-ac", "1", "-ar", "44100", "-af",
                        "silenceremove=start_periods=1:start_threshold=-40dB,areverse,silenceremove=start_periods=1:start_threshold=-40dB,areverse,"
                        f"loudnorm=I=-18:TP=-2,apad=pad_dur={GAP}", out], check=True)
        parts.append(out)
    lst = os.path.join(SRC, f"_list_{it['key']}.txt")
    open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
    dst = os.path.join(SRC, f"seq_{it['key']}.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, dst], check=True)
    for p in parts + [lst]: os.remove(p)
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", dst], capture_output=True, text=True).stdout)
    it["local"] = {"file": "incoming/cases/" + os.path.basename(dst), "start": 0, "end": round(d - GAP + 0.1, 2)}
json.dump(D, open(os.path.join(HERE, "cases.json"), "w"), ensure_ascii=False, indent=1)
subprocess.run(["python3", os.path.join(HERE, "fetch_vulgar.py"), "cases"], check=True, cwd=HERE)
page = lambda t: "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(("File:" + t).replace(" ", "_"))
lines = [f"Audio credits ({D['title']})", ""]
for it in D["items"]:
    c = it["credit"]
    files = it.get("seq") or [c["title"][5:]]
    lines.append(f"{it['name']}: " + ", ".join(f'"{f}"' for f in files) + f" by {c['artist']}, {c['license']}, via Wikimedia Commons, " + " ".join(page(f) for f in files))
open(os.path.join(HERE, "out", "cases_credits.txt"), "w").write("\n".join(lines) + "\n")
print("\n".join(lines))

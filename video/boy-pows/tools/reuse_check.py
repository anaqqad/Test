"""Owner's rule (24 Nov 2026): no second of a 3D reconstruction or a film on screen more than twice; no shot may run past the
end of its clip. Counts only what is visible (full-frame cards hide the footage under them).
python tools/reuse_check.py   -> prints problems and 'bad N'"""
import json, subprocess
from collections import defaultdict
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sb = json.load(open(ROOT / "build/storyboard.json", encoding="utf-8"))
FULL = {o["type"] for o in sb["overlays"]} - {"ContextTag", "SubscribeButton"}
covers = sorted((o["start"], o["end"]) for o in sb["overlays"] if o["type"] in FULL)
N3D = {"r3d_s_zero": 14.0, "r3d_s_camp_day": 16.0, "r3d_s_camp_night": 14.0, "r3d_s_bugle": 13.0, "r3d_s_charge": 15.0,
       "r3d_s_vickers": 14.0, "r3d_s_broadway": 13.0, "r3d_s_dawn": 15.0, "r3d_s_farm": 14.0}
def length(f):
    if f in N3D: return N3D[f]
    p = ROOT / f"assets/footage/{f}.mp4"
    if not p.exists(): return None
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout)
def visible(a, b):  # pieces of [a,b) not under a full-frame card
    out, t = [], a
    for c0, c1 in covers:
        if c1 <= t or c0 >= b: continue
        if c0 > t: out.append((t, c0))
        t = max(t, c1)
    if t < b: out.append((t, b))
    return out
bad = 0; use = defaultdict(lambda: defaultdict(int)); lens = {}
for s in sb["shots"]:
    f = s["file"]; L = lens.setdefault(f, length(f))
    if L is not None and s["in"] + (s["end"] - s["start"]) > L + 0.05:
        bad += 1; print(f"PAST END  {f} in {s['in']:.1f} + {s['end'] - s['start']:.1f} s > {L:.1f} s  at {s['start']:.1f} ({s['anchor']})")
    for a, b in visible(s["start"], s["end"]):
        x = s["in"] + (a - s["start"])
        while x < s["in"] + (b - s["start"]) - 0.25:
            use[f][round(x * 2) / 2] += 1; x += 0.5
for f, bins in use.items():
    over = sorted(k for k, v in bins.items() if v > 2)
    if over:
        bad += 1; print(f"{'3D' if f.startswith('r3d_') else 'FILM'} OVERUSE {f}: {len(over) / 2:.1f} s seen 3+ times, e.g. {over[:6]}")
    print(f"  {f}: {sum(1 for v in bins.values() if v) / 2:.1f} s of clip shown, max reuse {max(bins.values())}x")
print("bad", bad)

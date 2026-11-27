"""Assert no shot shows a risky range of a film (slates, title cards, surgery, blown-out stretches). python tools/risk.py"""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
RISK = {"prisoners_cherbourg_1944": [(0, 8, "slate"), (13, 41, "cap eagles close-up"), (70, 83, "chalk slate"), (92, 107, "cap eagle close-up"), (128, 140, "end")],
        "prisoners_italy_1945": [(0, 46, "haze"), (113, 127, "officer with breast eagle"), (128, 205, "haze")],
        "prisoners_shipped_adc140": [(0, 300, "British desert"), (476, 600, "other story")],
        "troop_train_1943": [(0, 45, "titles"), (598, 617, "text card"), (640, 660, "end")],
        "logging_1950": [(155, 200, "fire poster/tower"), (430, 560, "elk")]}
sb = json.load(open(ROOT / "build/storyboard.json", encoding="utf-8"))
bad = 0
for s in sb["shots"]:
    a, b = s["in"], s["in"] + s["end"] - s["start"]
    for r0, r1, why in RISK.get(s["file"], []):
        if a < r1 and b > r0:
            bad += 1; print(f"{s['file']} {a:.1f}-{b:.1f} overlaps {why} {r0}-{r1} at {s['start']:.1f} ({s['anchor']})")
print("bad", bad)

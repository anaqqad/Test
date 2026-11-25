"""Assert no shot shows a risky range of a film (slates, title cards, surgery, blown-out stretches). python tools/risk.py"""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
RISK = {"jpow_noumea_a": [(44, 54, "slate"), (285, 336, "dark/blurred"), (0, 3, "head")],
        "jpow_noumea_b": [(157, 169, "slate"), (172, 248, "surgery"), (0, 3, "head")],
        "jp_navy_review": [(0, 14, "titles"), (135, 148, "title"), (250, 264, "title/map"), (372, 384, "title")],
        "jp_newsreel42": [(0, 46, "titles"), (80, 108, "title card"), (255, 372, "maps/titles"), (595, 700, "end titles")]}
sb = json.load(open(ROOT / "build/storyboard.json", encoding="utf-8"))
bad = 0
for s in sb["shots"]:
    a, b = s["in"], s["in"] + s["end"] - s["start"]
    for r0, r1, why in RISK.get(s["file"], []):
        if a < r1 and b > r0:
            bad += 1; print(f"{s['file']} {a:.1f}-{b:.1f} overlaps {why} {r0}-{r1} at {s['start']:.1f} ({s['anchor']})")
print("bad", bad)

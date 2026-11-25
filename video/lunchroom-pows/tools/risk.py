"""Assert no shot shows a risky range of a film (slates, title cards, surgery, blown-out stretches). python tools/risk.py"""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
RISK = {"negro_soldier_1944": [(0, 70, "titles"), (228, 290, "enemy flag"), (1050, 1090, "enemy officers/map"), (2396, 2430, "end")],
        "teamwork_1946": [(0, 300, "titles, enemy flags, staging"), (590, 600, "end")],
        "restaurant_1946": [(0, 45, "titles"), (78, 175, "pages/titles"), (420, 440, "newspaper"), (480, 530, "text page"), (628, 645, "end titles")],
        "troop_train_1943": [(0, 45, "titles"), (598, 617, "text card"), (640, 660, "end")],
        "controlling_german_pows_1944": [(0, 80, "titles/manual"), (495, 545, "handwriting"), (880, 930, "enemy flag/end")],
        "prisoners_shipped_adc140": [(0, 300, "British desert, not POWs"), (476, 600, "other story")],
        "negro_personnel_1945": [(0, 30, "slate"), (470, 560, "end of recording")]}
sb = json.load(open(ROOT / "build/storyboard.json", encoding="utf-8"))
bad = 0
for s in sb["shots"]:
    a, b = s["in"], s["in"] + s["end"] - s["start"]
    for r0, r1, why in RISK.get(s["file"], []):
        if a < r1 and b > r0:
            bad += 1; print(f"{s['file']} {a:.1f}-{b:.1f} overlaps {why} {r0}-{r1} at {s['start']:.1f} ({s['anchor']})")
print("bad", bad)

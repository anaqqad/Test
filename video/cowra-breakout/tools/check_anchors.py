"""List every plan anchor / synced phrase that is not spoken in its paragraph (all at once). python tools/check_anchors.py"""
import json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
src = open(ROOT / "tools/plan.py", encoding="utf-8").read().split("def photo_items")[0]
g = {"__name__": "x", "__file__": str(ROOT / "tools/plan.py")}; exec(src, g)
exec("def photo_items" + open(ROOT / "tools/plan.py", encoding="utf-8").read().split("def photo_items")[1].split("def tag")[0], g)
g["photo_items"]()
P = g["P"]; words = json.load(open(ROOT / "audio/words.json", encoding="utf-8"))
norm = lambda w: re.sub(r"[^a-z0-9]", "", w.lower())
def found(pi, ph):
    t = [norm(x) for x in ph.split()]; toks = [norm(w["text"]) for w in words[pi]]
    return any(toks[i:i + len(t)] == t for i in range(len(toks) - len(t) + 1))
TK = {"t", "t0", "t1", "at", "labelAt", "labelTo", "beamAt", "byAt", "out", "show", "cardsOut"}
def phrases(o, key=None):
    if isinstance(o, dict):
        for k, v in o.items(): yield from phrases(v, k)
    elif isinstance(o, list):
        for v in o: yield from phrases(v, key)
    elif key in TK and isinstance(o, str): yield o
bad = 0
for pi, items in enumerate(P):
    for it in items:
        phs = [it[1]] if it[0] in "@#" else [it[0]]
        if it[0] == "#":
            if it[2]: phs.append(it[2])
            phs += list(phrases(it[3]))
            if it[3].get("type") == "LedgerDocument": phs += [s["say"] for s in it[3]["spans"]]
        for ph in phs:
            if not found(pi, ph):
                bad += 1; print(pi, repr(ph), "|", " ".join(norm(w["text"]) for w in words[pi])[:220])
print("bad", bad)

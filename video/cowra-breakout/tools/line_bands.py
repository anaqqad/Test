"""Manual highlight rects for typewritten scans the OCR cannot read (microfilm, heavy type).
Step 1: python tools/line_bands.py <scan> <x0> <x1> <y0> <y1>
        -> prints text-line bands (index, y0, y1) with their words' x ranges, writes build/bands_<scan>.jpg (numbered)
Step 2: python tools/line_bands.py <scan> <x0> <x1> <y0> <y1> --save <key> "<phrase>" b:w0-w1 b:w0-w1 ...
        -> one rect per band from word w0 to word w1 (inclusive, 0-based; w1 may be -1 = last word) into tools/doc_spans.json
"""
import json, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
scan = Path(sys.argv[1]); x0, x1, y0, y1 = map(int, sys.argv[2:6])
im = Image.open(scan).convert("L"); W, H = im.size
a = np.asarray(im.crop((x0, y0, x1, y1)), np.float32)
ink = a < (np.median(a) - 60)  # dark type on light paper
rows = ink.sum(1) > max(3, ink.shape[1] * 0.025)
bands, start = [], None
for y, r in enumerate(list(rows) + [False]):
    if r and start is None: start = y
    if not r and start is not None:
        if y - start > 12: bands.append([start, y])
        start = None
merged = []  # join bands split by thin gaps (descenders / dots)
for b in bands:
    if merged and b[0] - merged[-1][1] < 8: merged[-1][1] = b[1]
    else: merged.append(b)
hs = sorted(b1 - b0 for b0, b1 in merged); hmed = hs[len(hs) // 2]
starts = [b[0] for b in merged if b[1] - b[0] < 1.4 * hmed]
pitch = sorted(q - p for p, q in zip(starts, starts[1:]) if q - p < 2.5 * hmed)
pitch = pitch[len(pitch) // 2] if pitch else hmed * 1.15
split = []  # lines whose bands touch (tight typing) come out as one tall band: cut it at the line pitch
for b0, b1 in merged:
    n = max(1, round((b1 - b0) / pitch)) if b1 - b0 > 1.4 * hmed else 1
    for k in range(n):
        split.append([b0 + round(k * (b1 - b0) / n), b0 + round((k + 1) * (b1 - b0) / n)])
merged = split
out = []
for i, (b0, b1) in enumerate(merged):
    cols = ink[b0:b1].sum(0) > 0
    words, s, gap = [], None, 0
    for x, c in enumerate(list(cols) + [False] * 40):
        if c:
            if s is None: s = x
            gap = 0; e = x
        elif s is not None:
            gap += 1
            if gap > max(18, (b1 - b0) * 0.45): words.append([s, e]); s = None
    out.append({"i": i, "y0": y0 + b0, "y1": y0 + b1, "words": [[x0 + p, x0 + q] for p, q in words]})

if "--save" not in sys.argv:
    vis = Image.open(scan).convert("RGB").crop((x0, y0, x1, y1)); d = ImageDraw.Draw(vis)
    f = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 34)
    for b in out:
        for k, (p, q) in enumerate(b["words"]):
            d.rectangle([p - x0, b["y0"] - y0, q - x0, b["y1"] - y0], outline=(224, 68, 46), width=3)
            d.text((p - x0 + 2, b["y0"] - y0 - 30), str(k), fill=(0, 90, 200), font=f)
        d.text((4, b["y0"] - y0), str(b["i"]), fill=(0, 150, 0), font=f)
    vis.thumbnail((1800, 4000)); vis.save(ROOT / f"build/bands_{scan.stem}.jpg", quality=88)
    for b in out: print(b["i"], b["y0"], b["y1"], len(b["words"]), "words")
else:
    k = sys.argv.index("--save"); key, phrase, specs = sys.argv[k + 1], sys.argv[k + 2], sys.argv[k + 3:]
    rects = []
    for sp in specs:
        bi, ws = sp.split(":"); w0, w1 = map(int, ws.split("-")) if not ws.endswith("--1") else (int(ws.split("-")[0]), -1)
        b = out[int(bi)]; ww = b["words"]; p, q = ww[w0][0], ww[w1][1]
        pad = 10; rects.append([p - pad, b["y0"] - pad, q - p + 2 * pad, b["y1"] - b["y0"] + 2 * pad])
    store = ROOT / "tools/doc_spans.json"
    d = json.loads(store.read_text(encoding="utf-8")) if store.exists() else {}
    d[key] = {"image": scan.name, "pw": W, "ph": H, "phrase": phrase, "rects": rects}
    store.write_text(json.dumps(d, indent=1, ensure_ascii=False), encoding="utf-8")
    vis = Image.open(scan).convert("RGB"); dr = ImageDraw.Draw(vis)
    for r in rects: dr.rectangle([r[0], r[1], r[0] + r[2], r[1] + r[3]], outline=(224, 68, 46), width=8)
    vis.crop((x0, y0, x1, y1)).resize(((x1 - x0) // 3, (y1 - y0) // 3)).save(ROOT / f"build/doc_check_{key}.jpg", quality=85)
    print(key, rects)

"""Prepares the photos and document strips for the two Bush / Chichi Jima Shorts (23 Nov 2026).

Copies the episode's public-domain stills into the reel engine's public/pd/<id>/ folders, writes credits.json, and
builds phone-readable document strips: the highlighted lines of a real scan, re-flowed into short rows at word gaps,
each row underlined in grease-pencil red.

    PYTHONUTF8=1 python shorts/prep_bush_shorts.py
"""
import json
import shutil
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

EP = Path(__file__).resolve().parents[1] / "video" / "bush-chichijima"
ENGINE = Path(r"C:\Users\anass\Desktop\The Black History Room\Test")
STILLS = EP / "assets" / "stills"
META = json.loads((EP / "research" / "stills_meta.json").read_text(encoding="utf-8"))
SPANS = json.loads((EP / "tools" / "doc_spans.json").read_text(encoding="utf-8"))
RED = (224, 68, 46)

DOCS = {
    "doc_fire": ("aar_fire", "VT-51 Aircraft Action Report, Strike Baker, 2 Sept 1944, sheet 4 (NARA)", 1000),
    "doc_chute": ("aar_chute", "VT-51 Aircraft Action Report, 2 Sept 1944, sheet 4 (NARA)", 1000),
    "doc_shelter": ("trial_shelter", "U.S. v. Tachibana et al., Navy Military Commission, Guam, 1946 (NARA RG 125)", 560),
    "doc_revolting": ("trial_revolting", "U.S. v. Tachibana et al., prosecution's opening, Guam, 1946 (NARA RG 125)", 640),
}

SHORTS = {
    "reel-wwf-bush-fire": {
        "photos": {"portrait": "bush_flight_gear.jpg", "takeoff": "vt51_takeoff_jun44.jpg", "crew": "bl_H080-01.jpg",
                   "cockpit": "bush_cockpit_wide.jpg", "rescue": "bush_rescue_still.jpg"},
        "docs": ["doc_fire", "doc_chute"],
    },
    "reel-wwf-chichi-airmen": {
        "photos": {"tachibana": "tachibana_surrender.jpg", "guam": "guam_trial_building.jpg", "rescue": "bush_rescue_still.jpg", "portrait": "bush_flight_gear.jpg"},
        "docs": ["doc_shelter", "doc_revolting"],
    },
}
BL = {"bl_H080-01.jpg": {"title": "George Bush's flight crew: John Delaney, Leo Nadeau and George Bush (NARA 485327702)",
                         "artist": "U.S. Navy / George Bush Presidential Library", "license": "Public domain"}}


def split_points(strip: np.ndarray, max_w: int) -> list[int]:
    """Cut a text line at inter-word gaps so no piece is wider than max_w."""
    ink = (strip < 120).sum(axis=0)
    blank = ink == 0
    cuts, start, w = [], 0, strip.shape[1]
    while w - start > max_w:
        target = start + max_w
        # the widest blank run that ends before the target
        best, x = None, target
        while x > start + max_w // 2:
            if blank[x]:
                run = x
                while run > start and blank[run]:
                    run -= 1
                if x - run >= 8:
                    best = (run + x) // 2
                    break
                x = run
            x -= 1
        best = best or target
        cuts.append(best)
        start = best
    return cuts


def doc_strip(key: str, out: Path, max_w: int = 1500) -> tuple[int, int]:
    s = SPANS[key]
    page = Image.open(STILLS / s["image"]).convert("L")
    sx, sy = page.width / s["pw"], page.height / s["ph"]
    arr = np.asarray(page).astype(np.float32)
    paper = float(np.percentile(arr, 90))
    arr = np.clip((arr - 40) / max(paper - 40, 1) * 245, 0, 255)  # paper -> 245, ink stays dark
    bands = []
    for x, y, w, h in s["rects"]:
        x0, y0, x1, y1 = int(x * sx), int((y - 4) * sy), int((x + w) * sx), int((y + h + 4) * sy)
        strip = arr[y0:y1, x0:x1]
        ink = strip < 120
        strip = strip[:, ink.mean(axis=0) < 0.85]  # drop punch holes / page-edge blobs
        ink = strip < 120
        rows_ink = ink.sum(axis=1) > max(3, 0.01 * strip.shape[1])
        # the main text band = the longest run of inked rows (cuts off neighbouring lines)
        best, run, start = (0, 0), 0, 0
        for i, v in enumerate(rows_ink):
            if v:
                if run == 0:
                    start = i
                run += 1
                if run > best[1] - best[0]:
                    best = (start, i + 1)
            else:
                run = 0
        band = strip if best[1] - best[0] > 0.6 * strip.shape[0] else strip[max(best[0] - 4, 0):best[1] + 4]
        cols = np.where((band < 120).sum(axis=0) > 0)[0]
        bands.append(band[:, cols[0]:cols[-1] + 1])
    hh = int(np.median([b.shape[0] for b in bands]))
    bands = [np.asarray(Image.fromarray(b.astype(np.uint8)).resize((max(1, round(b.shape[1] * hh / b.shape[0])), hh))) for b in bands]
    space = np.full((hh, int(hh * 0.45)), 245, np.uint8)
    line = np.concatenate(sum(([b, space] for b in bands), [])[:-1], axis=1)
    rows, prev = [], 0
    for c in split_points(line, max_w) + [line.shape[1]]:
        piece = line[:, prev:c]
        cols = np.where((piece < 120).sum(axis=0) > 0)[0]
        if len(cols):
            rows.append(piece[:, cols[0]:cols[-1] + 1])
        prev = c
    pad, gap = 60, 36
    W = max(r.shape[1] for r in rows) + 2 * pad
    H = sum(r.shape[0] for r in rows) + gap * (len(rows) - 1) + 2 * pad
    img = Image.new("RGB", (W, H), (245, 245, 232))
    d = ImageDraw.Draw(img)
    y = pad
    for r in rows:
        r = r.astype(np.float32)
        img.paste(Image.fromarray(np.dstack([r, r, r * 232 / 245]).astype(np.uint8)), (pad, y))
        d.line([(pad - 4, y + r.shape[0] + 4), (pad + r.shape[1] + 4, y + r.shape[0] + 6)], fill=RED, width=9)
        y += r.shape[0] + gap
    img.save(out, quality=94)
    return img.size


for rid, cfg in SHORTS.items():
    dst = ENGINE / "public" / "pd" / rid
    dst.mkdir(parents=True, exist_ok=True)
    credits = {}
    for k, f in cfg["photos"].items():
        shutil.copy(STILLS / f, dst / f"{k}.jpg")
        m = META.get(f) or BL[f]
        im = Image.open(dst / f"{k}.jpg")
        credits[k] = {"title": "File:" + m["title"] if not m["title"].startswith("File:") and f in META else m["title"],
                      "artist": m.get("artist", "U.S. Navy"), "date": "", "license": m.get("license", "Public domain"),
                      "source": m.get("page", ""), "width": im.width, "height": im.height}
    for k in cfg["docs"]:
        w, h = doc_strip(DOCS[k][0], dst / f"{k}.jpg", DOCS[k][2])
        credits[k] = {"title": DOCS[k][1], "artist": "U.S. Navy", "date": "", "license": "Public domain", "source": "",
                      "width": w, "height": h}
    (dst / "credits.json").write_text(json.dumps(credits, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(rid, {k: (v["width"], v["height"]) for k, v in credits.items()})

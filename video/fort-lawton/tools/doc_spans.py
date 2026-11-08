"""Finds a sentence on a scanned document, for the LedgerDocument highlight card.
OCRs the scan once (RapidOCR, local, cached in build/ocr/), follows the sentence from line to line down its
column, and stores one rect per printed line in tools/doc_spans.json. Always look at the check image it writes:
OCR can merge or drop lines. The phrase must be verbatim from the document.
Usage: python tools/doc_spans.py assets/stills/<scan> <key> "<verbatim phrase>"     -> build/doc_check_<key>.jpg"""
import difflib, json, re, sys
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
STORE = ROOT / "tools/doc_spans.json"
norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())


def join(a, b):
    """One line read twice from overlapping tiles."""
    if a["x0"] > b["x0"]:
        a, b = b, a
    box = {"x0": a["x0"], "x1": max(a["x1"], b["x1"]), "y0": min(a["y0"], b["y0"]), "y1": max(a["y1"], b["y1"]), "conf": min(a["conf"], b["conf"])}
    if b["x1"] <= a["x1"]:
        return {**box, "text": a["text"]}
    if a["x0"] == b["x0"] or b["x0"] - a["x0"] < 4:
        return {**box, "text": b["text"]}
    m = difflib.SequenceMatcher(None, a["text"], b["text"], autojunk=False).find_longest_match(0, len(a["text"]), 0, len(b["text"]))
    return {**box, "text": a["text"][:m.a + m.size] + b["text"][m.b + m.size:]}


def ocr(path):
    cache = ROOT / f"build/ocr/{path.name}.json"
    if cache.exists():
        return json.load(open(cache, encoding="utf-8"))
    from rapidocr_onnxruntime import RapidOCR
    import numpy as np
    # small overlapping tiles at 2x: on a whole newspaper page the detector drops lines and joins columns
    eng, im, boxes = RapidOCR(), Image.open(path).convert("RGB"), []
    T, step, Z = 640, 480, 2
    for ty in range(0, max(1, im.height - T + step), step):
        for tx in range(0, max(1, im.width - T + step), step):
            tile = im.crop((tx, ty, tx + T, ty + T)).resize((T * Z, T * Z), Image.LANCZOS)
            result, _ = eng(np.asarray(tile))
            for box, text, conf in result or []:
                xs, ys = [p[0] / Z + tx for p in box], [p[1] / Z + ty for p in box]
                new = {"x0": min(xs), "x1": max(xs), "y0": min(ys), "y1": max(ys), "text": text, "conf": float(conf)}
                same = [o for o in boxes if abs((o["y0"] + o["y1"]) - (new["y0"] + new["y1"])) < 12 and min(o["x1"], new["x1"]) - max(o["x0"], new["x0"]) > 0.4 * min(o["x1"] - o["x0"], new["x1"] - new["x0"])]
                for o in same:  # a line cut by a tile edge: rejoin its two readings
                    boxes.remove(o)
                    new = join(o, new)
                boxes.append(new)
    cache.parent.mkdir(parents=True, exist_ok=True)
    json.dump(boxes, open(cache, "w", encoding="utf-8"), indent=0)
    return boxes


def next_line(boxes, b):
    """The box printed directly under b, in the same column."""
    below = []
    for o in boxes:
        overlap = min(o["x1"], b["x1"]) - max(o["x0"], b["x0"])
        if overlap > 0.5 * min(o["x1"] - o["x0"], b["x1"] - b["x0"]) and o["y0"] > (b["y0"] + b["y1"]) / 2:
            below.append(o)
    return min(below, key=lambda o: o["y0"], default=None)


def char_x(box, n_chars_before):
    """x of the n-th letter or digit of a box, by its position in the printed string."""
    text, seen = box["text"], 0
    for i, ch in enumerate(text):
        if seen == n_chars_before:
            return box["x0"] + (box["x1"] - box["x0"]) * i / max(1, len(text))
        seen += bool(norm(ch))
    return box["x1"]


def find(boxes, phrase):
    q = norm(phrase)
    probe = q[:24]
    best = (0.0, None, 0)
    for b in boxes:
        t = norm(b["text"])
        for s in range(max(1, len(t))):
            r = difflib.SequenceMatcher(None, t[s:s + len(probe)], probe[:len(t) - s]).ratio() * min(1, (len(t) - s) / 8)
            if r > best[0]:
                best = (r, b, s)
    score, b, s = best
    if score < 0.7:
        raise SystemExit(f"not found on this scan (best {score:.2f}): {phrase!r}")
    rects, left, spelled = [], q, []
    while b is not None and left:
        t = norm(b["text"])
        n = min(len(left), len(t) - s)
        if rects and difflib.SequenceMatcher(None, t[:n], left[:n]).ratio() < 0.6:
            print("WARNING: the next line does not match, stopped at:", b["text"], "| wanted:", left[:40])
            break
        x0, x1 = char_x(b, s), char_x(b, s + n)
        rects.append([round(x0) - 4, round(b["y0"]) - 2, round(x1 - x0) + 8, round(b["y1"] - b["y0"]) + 5])
        spelled.append(b["text"])
        left, s = left[n:], 0
        b = next_line(boxes, b) if left else None
    if len(rects) > 1:  # justified columns: full lines end at the same x, so a stray long box cannot cross the gutter
        right = rects[0][0] + rects[0][2]
        for r in rects[1:-1]:
            r[2] = min(r[2], right - r[0])
    if len(left) > 3:
        print("WARNING: not placed on the scan:", left[:60])
    print("read on the scan:", " / ".join(spelled))
    return rects


def find_pdf(pdf, page_no, phrase, image, dpi=200):
    """A PDF with a text layer (govinfo bills, the Congressional Record, OCR'd archive scans): exact word boxes,
    no OCR. Renders the page to `image` and returns one rect per printed line, in its pixels."""
    import pymupdf
    page = pymupdf.open(pdf)[page_no - 1]
    page.get_pixmap(dpi=dpi, colorspace=pymupdf.csGRAY).save(str(image))
    k = dpi / 72
    words = [w for w in page.get_text("words") if norm(w[4])]
    # drop margin line numbers (bills number every line at the left edge)
    words = [w for w in words if not (w[4].isdigit() and w[0] < page.rect.width * 0.25 and len(w[4]) <= 2)]
    words.sort(key=lambda w: (w[5], w[6], w[7]))  # block, line, word: reading order
    stream = "".join(norm(w[4]) for w in words)
    q = norm(phrase)
    i = stream.find(q)
    if i < 0:
        raise SystemExit(f"not in the PDF text: {phrase!r}")
    pos, picked = 0, []
    for w in words:
        n = len(norm(w[4]))
        if pos + n > i and pos < i + len(q):
            picked.append(w)
        pos += n
    lines = {}
    for w in picked:
        lines.setdefault((w[5], w[6]), []).append(w)
    rects = []
    for ws in lines.values():
        x0, y0 = min(w[0] for w in ws), min(w[1] for w in ws)
        x1, y1 = max(w[2] for w in ws), max(w[3] for w in ws)
        rects.append([round(x0 * k) - 4, round(y0 * k) - 2, round((x1 - x0) * k) + 8, round((y1 - y0) * k) + 4])
    rects.sort(key=lambda r: (r[1], r[0]))
    print("read in the PDF:", " ".join(w[4] for w in picked))
    return rects


if __name__ == "__main__":
    if sys.argv[1] == "--pdf":  # --pdf <file.pdf> <page, from 1> <key> "<phrase>"  -> assets/stills/<key>.png
        pdf, page_no, key, phrase = Path(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5]
        image = ROOT / f"assets/stills/{key}.png"
        rects = find_pdf(pdf, page_no, phrase, image)
        im = Image.open(image).convert("RGB")
    else:
        image, key, phrase = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
        im = Image.open(image).convert("RGB")
        rects = find(ocr(image), phrase)
    store = json.load(open(STORE, encoding="utf-8")) if STORE.exists() else {}
    store[key] = {"image": image.name, "pw": im.width, "ph": im.height, "phrase": phrase, "rects": rects}
    json.dump(store, open(STORE, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    d = ImageDraw.Draw(im, "RGBA")
    for x, y, w, h in rects:
        d.rectangle([x, y, x + w, y + h], fill=(224, 68, 46, 90), outline=(224, 68, 46, 255))
    (ROOT / "build").mkdir(exist_ok=True)
    im.save(ROOT / f"build/doc_check_{key}.jpg", quality=88)
    print(key, rects)

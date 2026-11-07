"""Pass 3 (academic source): Soepomo Poedjosoedarmo, "Wordlist of Javanese Non-Ngoko Vocabularies", Indonesia 7 (1969),
Cornell University (eCommons). A complete list of non-Ngoko word stems in columns: Ngoko | Krama (standard, substandard) |
Krama Inggil / Krama Andap | Madya | gloss. The scan is OCR'd, so columns are recovered from word coordinates
(pdftotext -bbox). Kept: the standard Krama column (polite register) and the K.I/K.A column (honorific / humble).
Not kept: substandard Krama, Madya, the separate kasar (rude) list, cells with several words on one line.
Old spelling is converted to the modern one (dj>j, tj>c, nj>ny, j>y) for merging. Confidence 'medium' (OCR).
usage: python3 extract_javanese.py  -> data_dicts/Javanese.poedjosoedarmo.jsonl (+ .excl.jsonl)"""
import re, json, html, subprocess, os, collections
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
PDF = "dicts/javanese/poedjo_wordlist.pdf"
URL = "https://ecommons.cornell.edu/server/api/core/bitstreams/1055992b-f295-4083-bc22-08923e6f3684/content"
bb = subprocess.run(["pdftotext", "-bbox", PDF, "-"], capture_output=True, text=True).stdout
COLS = ["ngoko", "krama", "krama_sub", "ki_ka", "madya", "gloss"]
CUTS = [30, 85, 135, 185, 235]
def col_of(rel):
    for i, c in enumerate(CUTS):
        if rel < c: return COLS[i]
    return "gloss"
def modern(w):
    w = w.replace("£", "é").replace("dj", "J").replace("tj", "C").replace("nj", "Ñ").replace("j", "y")
    return w.replace("J", "j").replace("C", "c").replace("Ñ", "ny")
TOK = re.compile(r"^[a-z£é][a-z£é'\-]*[a-z£é]$")
out, excl = open("data_dicts/Javanese.poedjosoedarmo.jsonl", "w"), open("data_dicts/Javanese.poedjosoedarmo.excl.jsonl", "w")
seen = set(); stats = collections.Counter(); started = False
for pno, page in enumerate(bb.split("<page ")[1:], 1):
    words = [(float(a), float(b), html.unescape(t)) for a, b, t in re.findall(r'xMin="([\d.]+)" yMin="([\d.]+)" xMax="[\d.]+" yMax="[\d.]+">([^<]*)<', page)]
    text = " ".join(t for _, _, t in words)
    if "NGOKO" in text and "MADYA" in text: started = True
    if not started: continue
    if "kasar)" in text and "rude" in text: break  # the separate list of rude words starts here
    for half in (0, 1):
        hw = [w for w in words if (w[0] < 370) == (half == 0)]
        if not hw: continue
        firsts = sorted(x for x, _, t in hw if (x < 150 if half == 0 else 370 <= x < 480) and TOK.match(t.lower()))
        if not firsts: continue
        base = firsts[max(0, len(firsts) // 20)]  # robust left edge of the Ngoko column
        rows = collections.defaultdict(list)
        for x, y, t in hw:
            c = col_of(x - base + 6)
            rows[(c, round(y / 3))].append((x, y, t))
        # join cells per column/line
        cells = collections.defaultdict(list)
        for (c, yk), ws in rows.items():
            ws.sort(); cells[c].append((min(y for _, y, _ in ws), [t for _, _, t in ws]))
        gloss_lines = sorted(cells.get("gloss", []))
        for c in ("krama", "ki_ka"):
            items = sorted(cells.get(c, []))
            i = 0
            while i < len(items):
                y, toks = items[i]
                toks = [t for t in toks if t.strip("-_~'\".,*=") and not t.startswith("(")]
                # word split over two lines with a hyphen
                if len(toks) == 1 and toks[0].endswith("-") and i + 1 < len(items) and items[i + 1][0] - y < 12:
                    toks = [toks[0][:-1] + items[i + 1][1][0]]; i += 1
                i += 1
                if not toks: continue
                g = next((" ".join(t) for gy, t in gloss_lines if abs(gy - y) < 4), "")
                raw = " ".join(toks)
                clean = [re.sub(r"[*=.,;:!]+$", "", t).strip("*=").lower() for t in toks]
                rec = {"lang": "Javanese", "word": modern(clean[0]) if clean else raw, "old_spelling": raw, "column": c, "gloss": g, "page": pno,
                       "source": "Poedjosoedarmo 1969 (Cornell)", "url": URL}
                if len(clean) > 1: reason = "several words in one cell (multiword or OCR split)"
                elif not TOK.match(clean[0]) or not 3 <= len(clean[0]) <= 18: reason = "OCR noise / not a clean word"
                elif clean[0].startswith("-") or clean[0].endswith("-"): reason = "affix"
                else: reason = None
                if not reason:
                    k = (c, rec["word"])
                    if k in seen: continue
                    seen.add(k)
                rec["evidence"] = ["label:" + ("krama inggil / krama andap column" if c == "ki_ka" else "krama (polite) column")]
                (excl if reason else out).write(json.dumps({**rec, **({"exclusion": reason} if reason else {})}, ensure_ascii=False) + "\n")
                stats[(c, bool(reason))] += 1
out.close(); excl.close(); print(stats)

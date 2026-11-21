"""Display data for render_speed.mjs -> speed/words.json (words with times relative to the first word, pauses, look)"""
import json, os, glob
HERE = os.path.dirname(os.path.abspath(__file__))
U = "/root/.claude/uploads/dc85da4d-be44-5a84-a7c9-a173fd7fa0b7/"
R = json.load(open(os.path.join(HERE, "out", "result.json")))
LOOK = {"eng": ("English", "gb", "p_eng_f", "moorland", "5e939b78"), "deu": ("German", "de", "a_slk", "forest", "01c6e092"),
        "jpn": ("Japanese", "jp", "p_jpn_f", "hongkong", "86bd6962"), "spa": ("Spanish", "es", "sl2_ell", "canary", "0c5d3452"),
        "fra": ("French", "fr", "sl2_est", "village", "3fadf45f"), "ita": ("Italian", "it", "e_ita", "tuscany", "066755c1"),
        "vie": ("Vietnamese", "vn", "t_vie", "andaman", "cc9d2ec8"), "cmn": ("Mandarin", "cn", "t_cmn", "hongkong", "2b694501")}
out = {}
for k, r in R.items():
    segs = json.load(open(os.path.join(HERE, "out", ("jpn_medium" if k == "jpn" else k) + ".json")))
    ws = [(s0, s1, w) for s in segs for s0, s1, w in s["words"] if s0 >= r["start"] - 0.05 and s1 <= r["end"] + 0.05]
    t0 = ws[0][0]
    pauses = [[round(ws[i][1] - t0, 3), round(ws[i + 1][0] - t0, 3)] for i in range(len(ws) - 1) if ws[i + 1][0] - ws[i][1] > 0.25]
    cjk = k in ("jpn", "cmn")
    if k == "deu":  # display the corrected fable text, timed along the original words
        new = r["text"].split()
        words = [[round(ws[min(len(ws) - 1, int(i * len(ws) / len(new)))][0] - t0, 3), x] for i, x in enumerate(new)]
    else:
        words = [[round(s0 - t0, 3), w.strip()] for s0, s1, w in ws]
    name, fl, wj, sc, up = LOOK[k]
    out[k] = {"name": name, "flag": fl, "wojak": wj, "scene": sc, "src": glob.glob(U + up + "*")[0], "words": words, "pauses": pauses, "sep": "" if cjk else " "}
json.dump(out, open(os.path.join(HERE, "words.json"), "w"), ensure_ascii=False, indent=1)
print({k: len(v["words"]) for k, v in out.items()})

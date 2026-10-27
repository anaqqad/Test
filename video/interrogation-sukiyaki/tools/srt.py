"""English captions (SRT) from the narration word timings: out/<slug>.srt.

audio/words.json holds the *spoken* form ("nineteen forty-four"); captions show the *written* script ("1944"). Each
paragraph's written words are matched to the spoken words with difflib, so a written word that became several spoken
words ("1944," -> "nineteen forty-four,") gets their combined time span. Lines are at most ~42 characters, broken
after punctuation where possible, and never overlap.
Usage: python tools/srt.py"""
import difflib, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAX = 42
norm = lambda w: re.sub(r"[^a-z0-9]", "", w.lower())

paras = json.load(open(ROOT / "audio/paragraphs.json", encoding="utf-8"))
words = json.load(open(ROOT / "audio/words.json", encoding="utf-8"))
timed = []  # (written word, start, end)
for p, ws in zip(paras, words):
    W = p["text"].split()
    sm = difflib.SequenceMatcher(a=[norm(w) for w in W], b=[norm(w["text"]) for w in ws], autojunk=False)
    for tag, i0, i1, j0, j1 in sm.get_opcodes():
        if i1 == i0: continue
        if j1 == j0:  # written words with no spoken counterpart: borrow the neighbour's time
            j = min(j0, len(ws) - 1); span = (ws[j]["start"], ws[j]["start"])
        else:
            span = (ws[j0]["start"], ws[j1 - 1]["end"])
        n = i1 - i0
        for k in range(n):  # spread a multi-word span evenly
            a = span[0] + (span[1] - span[0]) * k / n; b = span[0] + (span[1] - span[0]) * (k + 1) / n
            timed.append((W[i0 + k], a, b))
    timed.append(None)  # paragraph break

cues, cur = [], []
def flush():
    if cur: cues.append([" ".join(w for w, _, _ in cur), cur[0][1], cur[-1][2]]); cur.clear()
for t in timed:
    if t is None: flush(); continue
    line = " ".join(w for w, _, _ in cur + [t])
    if cur and len(line) > MAX: flush()
    cur.append(t)
    if re.search(r"[.!?:;]$", t[0]) or (re.search(r",$", t[0]) and len(" ".join(w for w, _, _ in cur)) > MAX * 0.6): flush()
flush()
for a, b in zip(cues, cues[1:]):
    a[2] = min(max(a[2], a[1] + 0.8), b[1] - 0.02)  # at least 0.8 s on screen, never overlapping the next cue

ts = lambda s: f"{int(s // 3600):02d}:{int(s % 3600 // 60):02d}:{int(s % 60):02d},{int(round(s % 1 * 1000)) % 1000:03d}"
out = ROOT / f"out/{ROOT.name}.srt"
out.parent.mkdir(exist_ok=True)
out.write_text("".join(f"{i}\n{ts(a)} --> {ts(b)}\n{t}\n\n" for i, (t, a, b) in enumerate(cues, 1)), encoding="utf-8")
print(len(cues), "cues ->", out)

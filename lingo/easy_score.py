# "Ranking the World's Easiest Languages (for English speakers)": FSI class hours decide the rank; ties are broken by
# how much the 207 Swadesh core words look like English (Wiktionary Swadesh appendices, saved in easy_data/).
# Look-alike score = mean over concepts of the best spelling similarity (1 - Levenshtein / longer length, diacritics
# folded) between any listed English word and any listed word of the language. python3 easy_score.py -> easy_data/scores.json
import re, html, json, os, unicodedata
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(HERE, "easy_data")
# FSI (U.S. Department of State, Foreign Service Institute), weeks of full-time class to professional working proficiency
FSI = {"Danish": 24, "Dutch": 24, "Italian": 24, "Norwegian": 24, "Portuguese": 24, "Romanian": 24, "Spanish": 24, "Swedish": 24,
       "French": 30, "German": 36, "Haitian Creole": 36, "Indonesian": 36, "Malay": 36, "Swahili": 36}
PAGES = {"Appendix:Swadesh_lists_for_Romance_languages": {"Portuguese": "Portuguese", "Spanish": "Spanish", "French": "French", "Italian": "Italian", "Romanian": "Romanian"},
         "Appendix:Swadesh_lists_for_Germanic_languages": {"Dutch": "Dutch", "German": "German", "Swedish": "Swedish", "Danish": "Danish", "Norwegian Bokmål": "Norwegian"},
         "Appendix:Swahili_Swadesh_list": {"Swahili": "Swahili"}, "Appendix:Haitian_Creole_Swadesh_list": {"Haitian Creole": "Haitian Creole"},
         "Appendix:Malay_Swadesh_list": {"Rumi": "Malay"}, "Appendix:Indonesian_Swadesh_list": {"Indonesian": "Indonesian"}}
clean = lambda c: re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", c))).strip()
fold = lambda s: "".join(ch for ch in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(ch) != "Mn")
def forms(cell):
    cell = re.sub(r"\([^)]*\)|\[[^\]]*\]|\*", " ", cell)
    return [fold(w) for w in re.split(r"[,/;~]|\s+", cell) if re.fullmatch(r"[^\W\d_]+(?:[-'][^\W\d_]+)*", w or "")]
def lev(a, b):
    p = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        c = [i]
        for j, y in enumerate(b, 1): c.append(min(p[j] + 1, c[j - 1] + 1, p[j - 1] + (x != y)))
        p = c
    return p[-1]
sim = lambda a, b: 1 - lev(a, b) / max(len(a), len(b))
words = {}  # language -> {concept number: [forms]}
eng = {}
for page, cols in PAGES.items():
    t = open(os.path.join(D, page + ".html")).read()
    rows = re.findall(r"<tr.*?</tr>", re.search(r"<table.*?</table>", t, re.S).group(0), re.S)
    hdr = [clean(c) for c in re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", rows[0], re.S)]
    idx = {}
    for h, lang in cols.items():
        idx[lang] = next(i for i, x in enumerate(hdr) if x.startswith(h) and not (h == "Swedish" and False))
    for r in rows[1:]:
        cells = [clean(c) for c in re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", r, re.S)]
        if len(cells) < 3 or not cells[0].rstrip(".").isdigit(): continue
        n = int(cells[0].rstrip(".")); eng.setdefault(n, forms(cells[1]))
        for lang, i in idx.items():
            if i < len(cells): words.setdefault(lang, {})[n] = forms(cells[i])
out = {}
for lang, w in words.items():
    s = [max((sim(a, b) for a in eng[n] for b in f), default=0) for n, f in w.items() if f and eng.get(n)]
    out[lang] = {"fsi_weeks": FSI[lang], "concepts": len(s), "lookalike": round(100 * sum(s) / len(s), 1),
                 "same_spelling": sum(1 for n, f in w.items() if f and set(f) & set(eng.get(n, [])))}
rank = sorted(out, key=lambda l: (out[l]["fsi_weeks"], -out[l]["lookalike"]))
for i, l in enumerate(rank, 1): out[l]["rank"] = i; print(i, l, out[l])
json.dump({"_note": "rank = FSI weeks, then look-alike % on the 207 Swadesh words (Wiktionary appendices)", **out}, open(os.path.join(D, "scores.json"), "w"), indent=1)

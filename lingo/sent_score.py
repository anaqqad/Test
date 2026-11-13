# Scores for the sentence video (sent_pairs.json): the same sentence in both languages, three ways.
#   words:   share of the words (both sentences together) that have a cognate in the other sentence
#   sound:   for every word, the Levenshtein similarity to its closest word in the other sentence (lower-cased,
#            diacritics folded), averaged over both sentences; word order does not matter
#   grammar: the same 6-point checklist as similar_score.py (cases, genders, article, verb endings, word order, script)
# python3 sent_score.py -> prints the table, writes cache/sent_scores.json
import json, os, re, unicodedata
import similar_score as sc

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "sent_pairs.json")))
GRAMMAR = dict(sc.GRAMMAR, **{
    "ces": (7, 3, "none", True, "SVO", "Latin"), "slk": (6, 3, "none", True, "SVO", "Latin"),
    "dan": (0, 2, "suffix", False, "V2", "Latin"), "nor": (0, 3, "suffix", False, "V2", "Latin"), "swe": (0, 2, "suffix", False, "V2", "Latin"),
    "rus": (6, 3, "none", True, "SVO", "Cyrillic"), "ukr": (7, 3, "none", True, "SVO", "Cyrillic"),
    "nld": (0, 2, "before", True, "V2", "Latin"), "deu": (4, 3, "before", True, "V2", "Latin"),
})


def words(s):
    return [w for w in re.findall(r"[^\W\d_]+(?:['’-][^\W\d_]+)*", s)]


def score(pk):
    p = D["pairs"][pk]
    sa, sb = D["sentences"][p["a"]], D["sentences"][p["b"]]
    wa, wb = words(sa), words(sb)
    na, nb = set(p["noncog"]), set(p["noncog_b"])
    for w in na | nb:
        assert w in wa or w in wb, f"{pk}: '{w}' is not in the sentence"
    cog = [w not in na for w in wa] + [w not in nb for w in wb]
    v = sum(cog) / len(cog)
    s = (sum(max(sc.sound_sim(w, x) for x in wb) for w in wa) + sum(max(sc.sound_sim(w, x) for x in wa) for w in wb)) / (len(wa) + len(wb))
    gm = [x == y for x, y in zip(GRAMMAR[p["a"]], GRAMMAR[p["b"]])]
    g = sum(gm) / 6
    return {"vocab": round(100 * v), "sound": round(100 * s), "grammar": round(100 * g), "total": round(100 * (v + s + g) / 3), "exact": 100 * (v + s + g) / 3,
            "cognates": sum(cog), "n": len(cog), "grammar_ok": sum(gm), "words_a": [{"w": w, "same": w not in na} for w in wa], "words_b": [{"w": w, "same": w not in nb} for w in wb]}


if __name__ == "__main__":
    res = {pk: score(pk) for pk in D["pairs"]}
    for pk, r in sorted(res.items(), key=lambda x: x[1]["exact"]):
        print(f"{pk}: words {r['vocab']}% ({r['cognates']}/{r['n']})  sound {r['sound']}%  grammar {r['grammar']}% ({r['grammar_ok']}/6)  => {r['total']}%")
    json.dump(res, open(os.path.join(HERE, "cache", "sent_scores.json"), "w"), indent=1, ensure_ascii=False)

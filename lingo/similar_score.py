# Fair comparison for the "most similar languages" video. Every pair is scored on the SAME 41 Swadesh core concepts
# (swadesh.json), three ways:
#   vocabulary: share of concepts where both languages use the same (cognate) word
#   sound:      average Levenshtein similarity of the two words' spellings (Hindi/Urdu romanised, diacritics folded)
#   grammar:    6-point checklist (noun cases, genders, definite article, person endings on verbs, word order, script)
# similarity % = mean of the three. Recordings only illustrate the words; the scores never depend on what was recorded.
# python3 similar_score.py -> prints the table and writes cache/similar_scores.json
import json, os, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
SW = json.load(open(os.path.join(HERE, "swadesh.json")))
CONCEPTS = [c for c in SW if c != "_note"]

# word pairs that are NOT the same root ("a|b", first alternative of each language)
NONCOG = {
    "spa_por": {"perro|cão", "negro|preto"},
    "cat_oci": {"gos|can", "dona|femna", "casa|ostal", "petit|pichon"},
    "bul_mkd": {"луна|месечина", "баща|татко", "крак|нога"},
    "nld_afr": {"hoofd|hoof", "steen|klip"},  # Afrikaans 'hoof' is cognate; corrected below
    "tur_aze": {"ateş|od", "köpek|it", "baba|ata", "iyi|yaxşı", "kalp|ürək", "adam|kişi", "beyaz|ağ", "siyah|qara", "ekmek|çörək"},
    "zsm_ind": {"bapa|ayah", "pokok|pohon", "kamu|kamu"},  # kamu|kamu is cognate; corrected below
    "hin_urd": {"पिता|باپ", "पेड़|درخت", "जीभ|زبان"},
}
NONCOG["nld_afr"].discard("hoofd|hoof"); NONCOG["zsm_ind"].discard("kamu|kamu")

# grammar checklist per language
GRAMMAR = {
    #        cases, genders, definite article, verb endings by person, basic word order, script
    "spa": (0, 2, "before", True, "SVO", "Latin"), "por": (0, 2, "before", True, "SVO", "Latin"),
    "cat": (0, 2, "before", True, "SVO", "Latin"), "oci": (0, 2, "before", True, "SVO", "Latin"),
    "bul": (0, 3, "suffix", True, "SVO", "Cyrillic"), "mkd": (0, 3, "suffix", True, "SVO", "Cyrillic"),
    "nld": (0, 2, "before", True, "V2", "Latin"), "afr": (0, 0, "before", False, "V2", "Latin"),
    "tur": (6, 0, "none", True, "SOV", "Latin"), "aze": (6, 0, "none", True, "SOV", "Latin"),
    "zsm": (0, 0, "none", False, "SVO", "Latin"), "ind": (0, 0, "none", False, "SVO", "Latin"),
    "hin": (3, 2, "none", True, "SOV", "Devanagari"), "urd": (3, 2, "none", True, "SOV", "Perso-Arabic"),
}
GRAMMAR_LABELS = ["noun cases", "genders", "definite article", "verb endings", "word order", "script"]

# romanisation of the Hindi / Urdu words (for the spelling distance)
ROM = {
 "पानी": "pani", "پانی": "pani", "आग": "ag", "آگ": "ag", "सूरज": "suraj", "سورج": "suraj", "चाँद": "chand", "چاند": "chand",
 "आँख": "ankh", "آنکھ": "ankh", "हाथ": "hath", "ہاتھ": "hath", "कुत्ता": "kutta", "کتا": "kutta", "मछली": "machhli", "مچھلی": "machhli",
 "माँ": "man", "ماں": "man", "पिता": "pita", "باپ": "bap", "एक": "ek", "ایک": "ek", "दो": "do", "دو": "do", "तीन": "tin", "تین": "tin",
 "रात": "rat", "رات": "rat", "बड़ा": "bada", "بڑا": "bada", "छोटा": "chhota", "چھوٹا": "chhota", "नया": "naya", "نیا": "naya",
 "अच्छा": "achha", "اچھا": "achha", "सिर": "sir", "سر": "sir", "दिल": "dil", "دل": "dil", "खून": "khun", "خون": "khun",
 "पेड़": "ped", "درخت": "darakht", "पत्थर": "patthar", "پتھر": "patthar", "नाम": "nam", "نام": "nam", "आदमी": "admi", "آدمی": "admi",
 "औरत": "aurat", "عورت": "aurat", "खाना": "khana", "کھانا": "khana", "पीना": "pina", "پینا": "pina", "सफ़ेद": "safed", "सफेद": "safed", "سفید": "safed",
 "काला": "kala", "کالا": "kala", "जीभ": "jibh", "زبان": "zaban", "कान": "kan", "کان": "kan", "नाक": "nak", "ناک": "nak",
 "पैर": "pair", "پاؤں": "paon", "इंसान": "insan", "انسان": "insan", "मैं": "main", "میں": "main", "तुम": "tum", "تم": "tum",
 "घर": "ghar", "گھر": "ghar", "रोटी": "roti", "روٹی": "roti", "दूध": "dudh", "دودھ": "dudh", "किताब": "kitab", "کتاب": "kitab",
}
FOLD = {"ə": "e", "ı": "i", "ł": "l", "ø": "o", "æ": "ae", "œ": "oe", "ß": "ss", "ð": "d", "þ": "th"}


def first(code, concept):
    return SW[concept][code].split("/")[0].strip()


def norm(w):
    w = ROM.get(w, w).lower()
    w = "".join(FOLD.get(ch, ch) for ch in w)
    return "".join(ch for ch in unicodedata.normalize("NFKD", w) if not unicodedata.combining(ch))


def lev(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def sound_sim(wa, wb):
    a, b = norm(wa), norm(wb)
    return 1 - lev(a, b) / max(len(a), len(b), 1)


def cognate(pk, wa, wb):
    return f"{wa}|{wb}" not in NONCOG[pk]


def grammar_matches(a, b):
    return [x == y for x, y in zip(GRAMMAR[a], GRAMMAR[b])]


def score(pk):
    a, b = pk.split("_")
    words = [(c, first(a, c), first(b, c)) for c in CONCEPTS]
    cog = [cognate(pk, wa, wb) for _, wa, wb in words]
    snd = [sound_sim(wa, wb) for _, wa, wb in words]
    gm = grammar_matches(a, b)
    v, s, g = sum(cog) / len(cog), sum(snd) / len(snd), sum(gm) / len(gm)
    return {"vocab": round(100 * v), "sound": round(100 * s), "grammar": round(100 * g), "total": round(100 * (v + s + g) / 3), "exact": 100 * (v + s + g) / 3,
            "cognates": sum(cog), "n": len(cog), "grammar_ok": sum(gm), "grammar_rows": [{"k": GRAMMAR_LABELS[i], "a": str(GRAMMAR[a][i]), "b": str(GRAMMAR[b][i]), "ok": gm[i]} for i in range(6)],
            "words": [{"c": c, "a": wa, "b": wb, "same": cg, "snd": round(100 * sd)} for (c, wa, wb), cg, sd in zip(words, cog, snd)]}


if __name__ == "__main__":
    res = {pk: score(pk) for pk in NONCOG}
    for pk, r in sorted(res.items(), key=lambda x: x[1]["total"]):
        print(f"{pk}: vocab {r['vocab']}% ({r['cognates']}/{r['n']})  sound {r['sound']}%  grammar {r['grammar']}% ({r['grammar_ok']}/6)  => {r['total']}%")
    os.makedirs(os.path.join(HERE, "cache"), exist_ok=True)
    json.dump(res, open(os.path.join(HERE, "cache", "similar_scores.json"), "w"), indent=1, ensure_ascii=False)

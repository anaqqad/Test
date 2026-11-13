"""Measure speaking speed: syllables per second of speaking time, on one read paragraph per language.
Syllables are counted from the words actually said (Whisper transcript, checked; English and German use the fable's
standard text where Whisper misheard), numbers counted as spoken. Speaking time = the paragraph minus pauses over
0.25 s. Each syllable gets a time (spread across its word) for the on-screen counter.
python3 speed/measure.py  -> speed/out/result.json"""
import json, os, re, unicodedata
import cmudict, pykakasi

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
PAUSE = 0.25
# paragraph windows (seconds in the original recording), chosen at sentence boundaries
WIN = {"eng": (0.0, 25.3), "deu": (0.0, 21.6), "jpn": (26.2, None), "spa": (0.0, 20.7), "fra": (0.0, 19.1),
       "ita": (0.0, 24.3), "vie": (0.0, 21.0), "cmn": (15.4, 35.5)}
JPN_END_WORD = "決め"  # Japanese paragraph ends at "…いわゆる三冠を決めた"
# numbers, as spoken (syllables)
NUM = {"fra": {"19": 2}, "ita": {"1998": 10}, "vie": {"11": 2, "5": 1}, "cmn": {"3866": 7}}
# Whisper mishearings fixed with the fable's standard text (same position, so the timing stays right)
FIX = {"deu": [("wer von ihnen meinen, wo der Stärkere wäre", "wer von ihnen beiden wohl der Stärkere wäre"),
               ("denn ein warmen Mantel", "der in einen warmen Mantel"), ("Deswegen ist er hergekommen.", "des Weges daherkam."),
               ("bließ", "blies"), ("gehüllt war. des Weges", "gehüllt war, des Weges")]}

CMU = cmudict.dict()
KKS = pykakasi.kakasi()
V = set("aeiouyàáâãäåèéêëìíîïòóôõöùúûüýÿæœ")


def syl_eng(w):
    w = w.lower().strip("'")
    if w in CMU: return sum(ch[-1].isdigit() for ch in CMU[w][0])
    return max(1, len(re.findall(r"[aeiouy]+", w)) - (1 if w.endswith("e") and len(w) > 3 else 0))


def syl_deu(w):
    w = w.lower()
    for d in ["äu", "eu", "ei", "ai", "au", "ie", "aa", "ee", "oo", "ey", "ay"]: w = w.replace(d, "#")
    return max(1, sum(1 for c in w if c in "aeiouyäöü#"))


def syl_romance(w, lang):
    w = w.lower()
    w = re.sub(r"qu(?=[eiéí])", "q", w); w = re.sub(r"gu(?=[eiéí])", "g", w); w = w.replace("qu", "q")
    if lang == "ita": w = re.sub(r"(c|g|sc|gl)i(?=[aou])", r"\1", w)  # silent i in cia, gio, scia, glio
    if w == "y": return 1
    w = w.replace("y", "")
    strong = set("aeoáéíóúàèòìù")
    n = 0
    for run in re.findall(r"[aeiouáéíóúàèìòùü]+", w):
        s = sum(1 for c in run if c in strong)
        n += s if s else 1
    return max(1, n) if re.search(r"[aeiouáéíóúàèìòù]", w) else 0


def syl_fra(w):
    w = w.lower()
    for part in [w]:
        p = re.sub(r"(?<=[^aeiouyéèêëàâîïôûù])(e|es)$", "", part) if len(re.findall(r"[aeiouyàâéèêëîïôûùœ]+", part)) > 1 else part
        p = re.sub(r"(?<=[aeiouéè])e$", "", p) if len(re.findall(r"[aeiouyàâéèêëîïôûùœ]+", p)) > 1 else p
        return max(1, len(re.findall(r"[aeiouyàâéèêëîïôûùœ]+", p)))


def syl_vie(w):
    if re.fullmatch(r"[A-Za-z]+", w) and len(re.findall(r"[aeiouy]+", w.lower())) > 1:  # foreign names: Malaysia, Ibrahim
        return len(re.findall(r"[aeiouy]+", w.lower()))
    return 1


def kanji_num(n):
    d = "〇一二三四五六七八九"; s = ""
    for val, ch in [(1000, "千"), (100, "百"), (10, "十")]:
        q, n = divmod(n, val)
        if q: s += ("" if q == 1 else d[q]) + ch
    return s + (d[n] if n else "")


def syl_jpn(text):
    text = re.sub(r"\d+", lambda m: kanji_num(int(m.group())), text)
    n = 0
    for tok in KKS.convert(text):
        r = tok["hepburn"].lower()
        prev = ""
        for c in r:
            if c in "aeiou":
                if not (prev and (prev == c or (prev == "o" and c == "u") or (prev == "e" and c == "i"))): n += 1
                prev = c
            else:
                prev = ""
    return n


def count_word(w, lang):
    w = w.strip()
    core = re.sub(r"[^\w'’\-]", "", w)
    if not core: return 0
    if lang in NUM and core in NUM[lang]: return NUM[lang][core]
    if lang == "cmn":
        return sum(1 for c in core if unicodedata.name(c, "").startswith("CJK")) + sum(NUM["cmn"].get(x, len(x)) for x in re.findall(r"\d+", core))
    if lang == "jpn": return syl_jpn(core)
    parts = re.split(r"['’\-]", core)
    f = {"eng": syl_eng, "deu": syl_deu, "fra": syl_fra, "vie": syl_vie}.get(lang)
    return sum((f(p) if f else syl_romance(p, lang)) for p in parts if p and not p.isdigit()) + sum(len(p) for p in parts if p.isdigit() and lang not in NUM)


res = {}
for lang, (a, b) in WIN.items():
    segs = json.load(open(os.path.join(OUT, ("jpn_medium" if lang == "jpn" else lang) + ".json")))
    words = [(s0, s1, w) for s in segs for s0, s1, w in s["words"] if s0 >= a - 0.05]
    if lang == "jpn":
        acc = ""
        for i, x in enumerate(words):
            acc += x[2]
            if JPN_END_WORD in acc: words = words[: i + 2]; break
    else:
        words = [x for x in words if x[1] <= b + 0.05]
    text = "".join(w for _, _, w in words)
    for old, new in FIX.get(lang, []):
        assert old in text, (lang, old)
        text = text.replace(old, new)
    ticks, total = [], 0
    if lang in FIX:  # corrected text: spread its syllables over the words' time span proportionally
        n_all = sum(count_word(w, lang) for w in text.split())
        spans = [(s0, s1) for s0, s1, _ in words]; dur = sum(s1 - s0 for s0, s1 in spans)
        k = 0
        for s0, s1 in spans:
            share = round(n_all * (s1 - s0) / dur) if dur else 0
            for j in range(share): ticks.append(s0 + (s1 - s0) * (j + 0.5) / share)
        total = n_all
        ticks = sorted(ticks)[:n_all] + [spans[-1][1]] * max(0, n_all - len(ticks))
    else:
        for s0, s1, w in words:
            n = count_word(w, lang); total += n
            for j in range(n): ticks.append(s0 + (s1 - s0) * (j + 0.5) / n)
    t0, t1 = words[0][0], words[-1][1]
    gaps = sum(max(0, words[i + 1][0] - words[i][1]) for i in range(len(words) - 1) if words[i + 1][0] - words[i][1] > PAUSE)
    speak = t1 - t0 - gaps
    res[lang] = {"start": round(t0, 2), "end": round(t1, 2), "speaking_time": round(speak, 2), "syllables": total,
                 "rate": round(total / speak, 2), "text": text.strip(), "ticks": [round(x - t0, 3) for x in ticks]}
    print(f"{lang}: {total} syllables / {speak:.1f} s speaking ({t1 - t0:.1f} s with pauses) = {total / speak:.2f} syl/s")
json.dump(res, open(os.path.join(OUT, "result.json"), "w"), ensure_ascii=False, indent=1)
for lang, r in sorted(res.items(), key=lambda kv: -kv[1]["rate"]): print(lang, r["rate"])

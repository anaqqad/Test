"""Pass 5-7: apply one set of inclusion/exclusion rules to every candidate sense from every source, merge spelling
variants into lemmas, and write the deliverables.
Inputs: data_en/<Lang>.cand.jsonl + .excl.jsonl (English Wiktionary), data_ed/<edition>.jsonl (native Wiktionaries),
data_dicts/*.jsonl (JMdict, CC-CEDICT). Outputs in out/: master.csv (A), language_summary.csv (B), exclusions.csv (D),
plus lemmas.json used by report.py.  usage: python3 classify.py"""
import json, glob, os, re, csv, collections, unicodedata
import opencc, pykakasi, hanja

HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
os.makedirs("out", exist_ok=True)
ACCESSED = "2026-10-24"
t2s = opencc.OpenCC("t2s"); kks = pykakasi.kakasi()
CODE2LANG = {"ja": "Japanese", "ko": "Korean", "zh": "Chinese", "cmn": "Chinese", "th": "Thai", "vi": "Vietnamese", "id": "Indonesian",
             "ms": "Malay", "jv": "Javanese", "su": "Sundanese", "ban": "Balinese", "km": "Khmer", "bo": "Tibetan", "my": "Burmese", "lo": "Lao",
             "dz": "Dzongkha", "en": "English", "fr": "French", "es": "Spanish", "de": "German", "it": "Italian", "pt": "Portuguese", "ar": "Arabic",
             "ru": "Russian", "tr": "Turkish", "hi": "Hindi", "fa": "Persian", "ur": "Urdu", "bn": "Bengali", "nl": "Dutch", "sv": "Swedish",
             "pl": "Polish", "ta": "Tamil", "tl": "Tagalog", "ne": "Nepali", "si": "Sinhalese", "mn": "Mongolian", "ml": "Malayalam",
             "te": "Telugu", "kn": "Kannada", "mr": "Marathi"}
UNSPACED = {"Japanese", "Chinese", "Thai", "Lao", "Khmer", "Burmese", "Tibetan", "Dzongkha"}
EXCL_POS = {"phrase", "proverb", "idiom", "prefix", "suffix", "infix", "affix", "interfix", "circumfix", "character", "symbol", "romanization",
            "punct", "combining_form", "name", "syllable", "contraction", "abbrev", "abbreviation", "prep_phrase", "adv_phrase", "counter", "num"}
BAD_TAGS = {"slang": "slang", "Internet": "Internet/nonstandard", "nonstandard": "Internet/nonstandard", "misspelling": "misspelling",
            "humorous": "humorous/jocular", "jocular": "humorous/jocular", "nonce-word": "nonce word", "pronunciation-spelling": "eye dialect",
            "eye-dialect": "eye dialect", "vulgar": "not polite (vulgar/derogatory/familiar)", "derogatory": "not polite (vulgar/derogatory/familiar)",
            "impolite": "not polite (vulgar/derogatory/familiar)", "familiar": "not polite (vulgar/derogatory/familiar)",
            "archaic": "archaic/obsolete/historical", "obsolete": "archaic/obsolete/historical", "historical": "archaic/obsolete/historical",
            "dialectal": "dialect/regional variety only", "proscribed": "proscribed usage", "childish": "baby-talk variant", "sarcastic": "sarcastic/ironic use", "ironic": "sarcastic/ironic use"}
# varieties outside the language's standard form(s): the count is for the standard language, the same rule for every language
REGIONAL = {"Philippines", "India", "Indian-English", "Singapore", "Singlish", "Malaysia", "Nigeria", "Pakistan", "South-Africa", "Ghana", "Louisiana",
            "Jamaica", "Caribbean", "Hawaii", "Kenya", "Sri-Lanka", "Bangladesh", "Cantonese", "Hokkien", "Min-Nan", "Hakka", "Wu", "Teochew",
            "Taiwanese-Hokkien", "Xiamen", "Quanzhou", "Zhangzhou", "Classical-Chinese", "Literary-Chinese", "Shanghainese", "Min-Dong", "Gan",
            "Xiang", "Jin", "Hong-Kong-Cantonese", "Guangzhou", "Jeju", "Gyeongsang", "Jeolla", "Hamgyong", "Pyongan", "Kansai", "Osaka", "Kyoto",
            "Tohoku", "Kyushu", "Hokkaido", "Okinawa", "Quebec", "Acadian", "Cajun", "Belgium", "Switzerland", "Swiss", "Austria", "Bavaria",
            "dialectal", "Northern-Thai", "Isan", "Southern-Thai"}
MANDARIN = {"Mandarin", "Mainland-China", "Taiwan", "Taiwanese-Mandarin", "Beijing", "Standard-Chinese"}
TITLE_WL = re.compile(r"^((?i:sir|madam|ma'am|mister|madame|monsieur|mademoiselle)\b|(Mr|Mrs|Miss|Ms)\b)")  # 'miss' lower-case is usually the verb
THEOLOGY = re.compile(r"apologia|\(defen[cs]e\)|written defen[cs]e|apologetic(s|ism)|apologist|apologian|theolog|Christian|presupposition|escapolog|defen[cs]e of (a|the|one's) (faith|doctrine|belief)", re.I)
DESCRIBES = re.compile(r"^\(?(very |extremely |overly )?(polite|politely|politeness|courteous|courteously|courtesy|humble|humbly|humility|respectful|respectfully|"
                       r"respect|reverent|deferential|deference|well-mannered|civil|gracious|grateful|gratitude|thankful|apologetic|ungrateful|rude|modest)\b", re.I)
FUNC_INTJ = re.compile(r"^\(?((expresses|expressing|used to express) (\w+, )?(remorse|gratitude|thanks|appreciation|apology)|please|thank you|thanks|thank-you|sorry|excuse me|pardon|i beg your pardon|my apologies|forgive me|i'm sorry|"
                       r"used to (express|show) (thanks|gratitude|appreciation|apology|regret)|used (to make|in making|when making) a (polite )?request|"
                       r"(an? )?(expression|acknowledg(e)?ment) of (thanks|gratitude|apology|remorse))", re.I)
FUNC_VERB = re.compile(r"^\(?(to )?(thank|apologi[sz]e|make an apology|acknowledge (a|some|one's) fault|express (one's )?(\w+ (or|and) )?(thanks|gratitude|appreciation|remorse|an apology|apologies)|ask (for )?(forgiveness|pardon)|"
                       r"beg (for )?(someone's )?pardon|say (thank you|thanks|sorry)|request politely|politely request|please\b)", re.I)
FUNC_NOUN = re.compile(r"^\(?(an? |the )?(thank-you|thanks\b|thank you|apology|apologies|expression of (\w+ (or|and) )?(thanks|gratitude|appreciation|apology|regret|remorse)|"
                       r"act of saying (sorry|thank you|thanks)|courtesy title|title of respect|respectful (title|term|form of address))", re.I)
FUNC_ADV = re.compile(r"^\(?(please|thank you|sorry)\b|^\(?(used (to make|in making|when making) a (polite )?request|used to soften (a |the )?(request|command|imperative)|\(?used to soften requests\)?)", re.I)
ADDR = re.compile(r"(respectful|honorific|polite|courtesy|deferential) (title|term of address|form of address|address|way of addressing)|title of (respect|honou?r|courtesy)|"
                  r"(term|form) of (respectful )?address|used (as a (respectful|polite) )?(title|form of address|term of address) (for|to)|respectful term", re.I)
NONPOLITE_GLOSS = re.compile(r"non-?polite|\bplain\b.{0,20}(pronoun|form)|impolite|\brude\b|vulgar|condescending|contemptuous|disparaging|pejorative", re.I)
# native-edition labels (categories/tags) that put the word itself in a politeness register
NAT_LABEL = re.compile(r"^(honorific|humble|polite|respectful|deferential)$|^(Respectueux|Humble|Honorifique|Registre (honorifique|humble)|Humble poli|Poli et humble|Respectueux et poli|Honorifique ou respectueux|Légèrement (humble|respectueux))$|敬語|尊敬語|謙譲語|丁寧語|尊辞|謙辞|높임말|겸양어|ราชาศัพท์|ที่สุภาพ|คำสุภาพ|"
                       r"Kính ngữ|Từ lịch sự|Thể lịch sự|Humble terms|Honorific terms|Perkataan sopan|bahasa halus|^krama|krama inggil|Istilah hormat|diraja", re.I)
NAT_GLOSS = re.compile(r"높여 이르는|높임말|높이어 이르는|겸양어|낮추어 이르는|낮춰 이르는|の尊敬語|の謙譲語|の丁寧語|尊敬語|謙譲語|丁寧語|敬称|謙称|尊称|"
                       r"敬辭|敬辞|謙辭|谦辞|敬稱|谦称|尊稱|尊称|ราชาศัพท์|คำสุภาพ|kính ngữ|tôn xưng|khiêm xưng|"
                       r"(bahasa|ragam) (halus|hormat|krama)|^\(?(kata )?(halus|hormat|krama)\b|bentuk (halus|hormat)|krama inggil|(sapaan|panggilan|sebutan) (hormat|sopan)|untuk menghormati|"
                       r"formule de politesse|forme de politesse|titre de courtoisie|Höflichkeitsform|fórmula de cortesía|tratamiento de respeto|"
                       r"forma di cortesia|forma de cortesia|вежливое обращение|форма вежливости|zwrot grzecznościowy|beleefdheidsvorm", re.I)
ROYAL = re.compile(r"royal|ราชาศัพท์|diraja|bahasa istana|king|queen|monarch|emperor|sovereign", re.I)

def kana(s):
    return "".join(x["hira"] for x in kks.convert(s))
def key_of(lang, w):
    w = unicodedata.normalize("NFC", w).strip()
    if lang == "Chinese": return t2s.convert(w)
    if lang in ("Javanese", "Indonesian", "Malay", "Sundanese", "Balinese"):
        return "".join(c for c in unicodedata.normalize("NFD", w.casefold()) if unicodedata.category(c) != "Mn")
    if lang == "Korean" and re.search(r"[\u4e00-\u9fff]", w): return hanja.translate(w, "substitution")  # Hanja spelling -> Hangul
    if lang in UNSPACED: return w
    return w.casefold()

def category(lang, fn, tags, labels, gloss, pos):
    """Map one accepted sense to the 12 mission categories."""
    t = " ".join(tags + labels).lower(); g = gloss.lower()
    if fn == "request": return "1 request"
    if fn == "apology": return "2 apology"
    if fn == "gratitude": return "3 gratitude"
    if ROYAL.search(" ".join(labels)) or ("royal" in t) or (("honorific" in t or "尊" in t) and re.search(r"\b(king|royal|monarch|emperor|majesty|highness|prince|princess)\b", g)): return "10 royal register"
    if fn == "pronoun" or pos == "pron": return "6 respectful pronoun"
    if fn == "address": return "5 honorific title/address"
    if re.search(r"humble|謙譲|謙|겸양|낮추|khiêm|merendah|ถ่อม", t + " " + g): return "8 humble vocabulary"
    if re.search(r"deferential|respectful", t): return "9 deferential vocabulary"
    if re.search(r"honorific|尊敬|尊辞|敬称|높임|kính ngữ|krama inggil|hormat|ยกย่อง", t + " " + g): return "7 honorific vocabulary"
    if pos in ("intj", "particle"): return "11 polite particle/interjection/greeting"
    if re.search(r"polite|丁寧|공손|สุภาพ|lịch sự|sopan|halus|krama", t + " " + g): return "4 courtesy/polite vocabulary"
    return "12 other documented"

def judge_en(d):
    """English-Wiktionary candidate sense -> (function, None) if accepted, or (None, reason)."""
    if d.get("exclusion"): return None, d["exclusion"]
    if d["lang"] == "Vietnamese" and re.search(r"[\u4e00-\u9fff\U00020000-\U0002ffff]", d["word"]):
        return None, "Han-Nom (chữ Hán/Nôm) spelling of a Vietnamese word, not a separate lemma"
    w, pos, gl, tags = d["word"], d["pos"], d["gloss"], d["tags"]
    ev = ",".join(d["evidence"]); cats = " | ".join(c for c in d.get("cats", []) if c.startswith(d["lang"] + " "))  # own-language categories only
    strong = ev.startswith("tag:") or "cat:" in ev
    for t in tags:
        if t in BAD_TAGS: return None, BAD_TAGS[t]
        if t in REGIONAL: return None, f"regional variety only ({t})"
    if re.search(r"unadapted borrowings", cats): return None, "unadapted foreign borrowing"
    if d["lang"] == "Chinese":
        var = [t for t in tags if t[:1].isupper() and t not in ("Internet",)]
        if var and not set(var) & MANDARIN: return None, f"not Standard Mandarin ({','.join(var)})"
    # a foreign courtesy word used as-is (merci, gracias, arigato in English): borrowed interjection marked colloquial/humorous or cultural
    if not strong and pos in ("intj", "particle") and re.search(r"^(Unadapted borrowing|Borrowed|Learned borrowing|Semi-learned borrowing|Pseudo-borrowed) from|romanization of", d.get("etym", "")):
        return None, "courtesy interjection borrowed whole from another language"
    if re.search(r"\b(slang|Internet slang|nonstandard|misspellings|humorous|nonce)\b", cats) and not strong: return None, "slang/Internet/nonstandard/humorous"
    if THEOLOGY.search(gl) or THEOLOGY.search(w): return None, "theological/unrelated sense of an apolog- word"
    if NONPOLITE_GLOSS.search(gl) and not strong: return None, "plain/non-polite counterpart"
    if pos in ("adj", "adv") and DESCRIBES.search(gl) and not FUNC_ADV.search(gl): return None, "describes politeness rather than being a politeness word"
    if pos in ("noun",) and DESCRIBES.search(gl) and not strong: return None, "describes politeness rather than being a politeness word"
    funcs = re.findall(r"gloss:([\w/,-]+)", ev); funcs = funcs[0].split(",") if funcs else []
    rawroyal = re.search(r"tag:royal/clerical register \(([^)]*)\)", ev)
    if rawroyal and not re.search(r"royal|monk", rawroyal.group(1), re.I) and not re.search(r"tag:(honorific|humble|polite|respectful|deferential)|cat:", ev):
        strong = False
        if not funcs: return None, f"usage note ({rawroyal.group(1)}) is not a register label"
    if strong:
        if "pronoun" in funcs: return "pronoun", None
        if "address/title" in funcs: return "address", None
        return "register", None
    # gloss-only evidence: the definition must say what the word itself does
    for fn in ("request", "gratitude", "apology"):
        if fn in funcs:
            if pos == "verb" and ("modal" in tags or "auxiliary" in tags): return None, "general modal/auxiliary verb (polite request is one use)"
            ok = (pos in ("intj", "particle") and FUNC_INTJ.search(gl)) or (pos == "verb" and FUNC_VERB.search(gl)) or \
                 (pos == "noun" and FUNC_NOUN.search(gl)) or (pos == "adv" and FUNC_ADV.search(gl))
            if ok: return fn, None
    if re.search(r"brothel|procur(ess|er)|bordello", gl, re.I): return None, "not a title of respect (brothel 'madam')"
    if "address/title" in funcs and pos in ("noun", "pron", "particle", "intj"):
        if ADDR.search(gl) or (TITLE_WL.search(gl) and d["lang"] != "English"): return "address", None
    if "title-word" in funcs and pos in ("noun", "pron", "particle") and TITLE_WL.search(gl): return "address", None
    if "pronoun" in funcs and pos == "pron" and re.search(r"\b(polite|respectful|honorific|humble|deferential|formal)\b", gl): return "pronoun", None
    if "honorific-gloss" in funcs and re.search(r"^\(?(an? )?(honorific|humble|polite|respectful|deferential) (form|term|word|equivalent|version|particle|pronoun|verb|title|way of (saying|referring)|counter|expression for)|"
                                                r"^\((honorific|humble|polite|respectful|deferential)\)|^.{0,30}\b(honorific|humble|polite|respectful|deferential) (equivalent|form|term|word|version) (of|for)\b", gl, re.I):
        return "register", None
    return None, "definition does not state a politeness function of the word itself"

def judge_ed(d):
    lang = CODE2LANG.get(d["lang_code"])
    if not lang: return None, None, "language outside scope"
    if d.get("form_of"): return lang, None, "inflected/alternative form"
    if d.get("pos") in EXCL_POS: return lang, None, f"part of speech '{d['pos']}' (not a standalone word)"
    w = d["word"] or ""
    if lang == "Vietnamese" and re.search(r"[\u4e00-\u9fff\U00020000-\U0002ffff]", w): return lang, None, "Han-Nom (chữ Hán/Nôm) spelling of a Vietnamese word, not a separate lemma"
    if lang not in UNSPACED and " " in w.strip(): return lang, None, "multiword expression"
    if ":" in w or "/" in w: return lang, None, "not a word page"
    for t in d.get("tags", []):
        if t in BAD_TAGS: return lang, None, BAD_TAGS[t]
        if t in REGIONAL: return lang, None, f"regional variety only ({t})"
    labs = [x for x in d["labels"] if NAT_LABEL.search(x) and not x.startswith("Turunan kata") and "Royal residences" not in x and "bất lịch sự" not in x]
    ed = d["edition"].replace("wiktionary", "")
    if ed == "zh" and d["lang_code"] not in ("zh", "cmn", "ja", "ko", "vi"):
        labs = [x for x in labs if x not in ("honorific", "polite", "humble", "respectful")]  # zh edition maps 'elevated style' of European words to this tag
    # the keyword must describe the headword itself: near the start of the definition, or closing it
    gh = [g for g in d["gloss_hits"] if (m := NAT_GLOSS.search(g)) and (m.start() <= 25 or len(g.rstrip("。.、) ）")) - m.end() <= 3)]
    if not labs and not gh: return lang, None, "native edition: keyword only in a derived-word list or incidental mention"
    if any(re.search(r"非敬語|비높임|bất lịch sự", x) for x in labs + gh): return lang, None, "plain/non-polite counterpart"
    if set(labs) <= {"polite"} and re.search(r"powitani|pożegnani|toast|kichnię|salutation|salu[ée]|quitte|éternu|bienvenue|accueill|greeting|farewell|Begrüßung|Abschied|saludo|despedida|приветстви|прощани", " ".join(d["glosses"]), re.I):
        return lang, None, "everyday greeting/farewell/toast (labelled only as a courtesy formula)"
    if not gh and ED_LANG.get(ed) != lang: return lang, "register-foreign-label", None
    return lang, "register", None

ED_LANG = {"ja": "Japanese", "ko": "Korean", "zh": "Chinese", "th": "Thai", "vi": "Vietnamese", "id": "Indonesian", "ms": "Malay", "it": "Italian",
           "pt": "Portuguese", "tr": "Turkish", "pl": "Polish", "es": "Spanish", "nl": "Dutch", "ru": "Russian", "de": "German", "fr": "French"}

def judge_dict(d):
    if d.get("exclusion"): return None, d["exclusion"]
    g = d["gloss"]; misc = d.get("misc", [])
    if any(m in ("sl", "joc", "derog", "vulg", "net-sl", "male-sl", "rare") for m in misc) and not any(m in ("hon", "hum", "pol") for m in misc):
        return None, "slang/jocular/derogatory/rare (no politeness tag)"
    if any(m in ("sl", "joc", "derog", "vulg", "net-sl") for m in misc): return None, "slang/jocular/derogatory"
    if d["source"] == "CC-CEDICT" and re.search(r"\((humorous|slang|Internet slang|dialect|Cantonese|Hokkien|Shanghainese|old|archaic|classical|loanword)\b|\bphonetic rendering\b|\btranscription of\b", g, re.I):
        return None, "humorous/slang/dialect/archaic/loan transcription (CC-CEDICT note)"
    ev = ",".join(d["evidence"])
    if ev.startswith(("tag:", "label:")) or "label:" in ev:
        return "register", None
    funcs = re.findall(r"gloss:([\w/,-]+)", ev); funcs = funcs[0].split(",") if funcs else []
    parts = [p.strip() for p in re.split(r"[/;]", g)]
    for fn in ("request", "gratitude", "apology"):
        if fn in funcs and any(FUNC_INTJ.search(p) or FUNC_VERB.search(p) or FUNC_NOUN.search(p) for p in parts): return fn, None
    if "address/title" in funcs and any(ADDR.search(p) for p in parts): return "address", None
    if "pronoun" in funcs and any(re.search(r"\b(polite|respectful|honorific|humble|deferential)\b.*\b(you|I|me|pronoun)\b|\byou \((polite|honorific|respectful)", p) for p in parts):
        return "pronoun", None
    return None, "definition does not state a politeness function of the word itself"

senses, excluded = [], []
def wikt_url(w, lang, ed="en"):
    return f"https://{ed}.wiktionary.org/wiki/" + w.replace(" ", "_")
# data_en2 holds the final extraction of every language (with etymology and royal/clerical usage notes)
en_files = sorted(glob.glob("data_en2/*.jsonl"))
for f in en_files:
    for line in open(f):
        d = json.loads(line); fn, why = judge_en(d)
        base = {"language": d["lang"], "word": d["word"], "pos": d["pos"], "gloss": d["gloss"][:200], "translit": d.get("translit") or "",
                "source": "English Wiktionary (kaikki.org wiktextract)", "url": wikt_url(d["word"], d["lang"]) + "#" + d["lang"].replace(" ", "_"),
                "evidence": "; ".join(d["evidence"]) + (" | tags: " + ",".join(d["tags"]) if d["tags"] else ""), "tags": d["tags"], "labels": [x for x in d.get("cats", []) if re.search(r"honorific|polite|humble|royal|respect", x, re.I)]}
        if fn: senses.append({**base, "fn": fn})
        else: excluded.append({**base, "reason": why})
for f in sorted(glob.glob("data_ed/*.jsonl")):
    for line in open(f):
        d = json.loads(line); lang, fn, why = judge_ed(d)
        if not lang: continue
        ed = d["edition"].replace("wiktionary", "")
        base = {"language": lang, "word": d["word"], "pos": d.get("pos", ""), "gloss": " / ".join(d["glosses"])[:200], "translit": "",
                "source": f"{ed} Wiktionary (kaikki.org wiktextract)", "url": wikt_url(d["word"], lang, ed),
                "evidence": "; ".join(d["labels"] + d["gloss_hits"])[:200], "tags": d.get("tags", []), "labels": d["labels"]}
        if fn: senses.append({**base, "fn": fn})
        else: excluded.append({**base, "reason": why})
for f in sorted(glob.glob("data_dicts/*.jsonl")):
    for line in open(f):
        d = json.loads(line); fn, why = judge_dict(d)
        base = {"language": d["lang"], "word": d["word"], "pos": d.get("pos", ""), "gloss": d["gloss"][:200], "translit": d.get("reading") or d.get("pinyin", ""),
                "source": d["source"], "url": d["url"], "evidence": "; ".join(d["evidence"]) + (" | misc: " + ",".join(d.get("misc", [])) if d.get("misc") else ""),
                "tags": [{"hon": "honorific", "hum": "humble", "pol": "polite"}.get(m, m) for m in d.get("misc", [])], "labels": d["evidence"] if d["source"].startswith("Poedjo") else [], "alts": d.get("alts", []) + ([d["trad"]] if d.get("trad") else [])}
        if fn: senses.append({**base, "fn": fn})
        else: excluded.append({**base, "reason": why})

# a label put on a foreign-language word by another language's edition (e.g. "English honorifics" in the Korean edition) only
# corroborates; on its own it does not create a lemma
own = {(s["language"], key_of(s["language"], s["word"])) for s in senses if s["fn"] != "register-foreign-label"}
for s in [s for s in senses if s["fn"] == "register-foreign-label"]:
    if (s["language"], key_of(s["language"], s["word"])) not in own:
        senses.remove(s); excluded.append({**s, "reason": "label only from another language's Wiktionary, not corroborated by any other source"})
    else: s["fn"] = "register"
# --- merge spelling variants into lemmas (union-find per language) ---
parent = {}
def find(x):
    while parent.setdefault(x, x) != x: parent[x] = parent[parent[x]]; x = parent[x]
    return x
def union(a, b): parent[find(a)] = find(b)
def is_kana(s): return bool(s) and all("぀" <= c <= "ヿ" or c in "ー・" for c in s)
for s in senses:
    k = (s["language"], key_of(s["language"], s["word"])); find(k)
    for a in s.get("alts", []):
        if a: union((s["language"], key_of(s["language"], a)), k)
# Japanese: kana-only spelling joins the kanji spelling with the same reading (JMdict already links most)
jp = {}
for s in senses:
    if s["language"] == "Japanese" and not is_kana(s["word"]): jp.setdefault(kana(s["word"]), set()).add(key_of("Japanese", s["word"]))
for s in senses:
    if s["language"] == "Japanese" and is_kana(s["word"]):
        r = kana(s["word"])
        if r in jp and len(jp[r]) == 1: union(("Japanese", key_of("Japanese", s["word"])), ("Japanese", next(iter(jp[r]))))
lemmas = collections.OrderedDict()
for s in senses:
    k = find((s["language"], key_of(s["language"], s["word"])))
    L = lemmas.setdefault(k, {"language": s["language"], "forms": collections.Counter(), "senses": []})
    L["forms"][s["word"]] += 1; L["senses"].append(s)
excluded_keys = collections.defaultdict(list)
for e in excluded: excluded_keys[(e["language"], key_of(e["language"], e["word"]))].append(e)

rows = []
for k, L in lemmas.items():
    lang = L["language"]; forms = [f for f, _ in L["forms"].most_common()]
    head = next((f for f in forms if not is_kana(f)), forms[0]) if lang == "Japanese" else forms[0]
    cats = sorted({category(lang, s["fn"], s["tags"], s["labels"], s["gloss"], s["pos"]) for s in L["senses"]}, key=lambda c: int(c.split()[0]))
    srcs = sorted({s["source"] for s in L["senses"]})
    s0 = next((s for s in L["senses"] if s["source"].startswith("English")), L["senses"][0])
    translit = next((s["translit"] for s in L["senses"] if s["translit"] and s["source"] in ("JMdict", "CC-CEDICT")), "") or (kana(head) if lang == "Japanese" else "")
    rows.append({"language": lang, "lemma": head, "variants_merged": " | ".join(f for f in forms if f != head), "transliteration": translit,
                 "part_of_speech": ",".join(sorted({s["pos"] for s in L["senses"] if s["pos"]})), "categories": "; ".join(cats),
                 "primary_category": cats[0], "english_gloss": s0["gloss"], "evidence": " || ".join(sorted({s["evidence"] for s in L["senses"]}))[:400],
                 "sources": " | ".join(srcs), "n_sources": len(srcs), "source_urls": " ".join(sorted({s["url"] for s in L["senses"]}))[:600],
                 "confidence": "medium" if srcs == ["Poedjosoedarmo 1969 (Cornell)"] else "high" if len(srcs) >= 2 or any(s["evidence"].startswith(("tag:", "cat:", "label:")) or "misc:" in s["evidence"] or (s["labels"] and not s["source"].startswith("English")) for s in L["senses"]) else "medium",
                 "date_accessed": ACCESSED, "audio_status": "not checked"})
rows.sort(key=lambda r: (r["language"], r["primary_category"], r["lemma"]))
F = list(rows[0].keys())
with open("out/master.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, F); w.writeheader(); w.writerows(rows)
accepted_keys = {(r["language"], key_of(r["language"], r["lemma"])) for r in rows} | {(r["language"], key_of(r["language"], v)) for r in rows for v in r["variants_merged"].split(" | ") if v}
with open("out/exclusions.csv", "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["language", "word", "part_of_speech", "reason", "gloss", "source", "url", "note"])
    seen = set()
    for e in excluded:
        k = (e["language"], key_of(e["language"], e["word"]), e["reason"])
        if k in seen: continue
        seen.add(k)
        note = "word is counted through another sense/source" if k[:2] in accepted_keys else ""
        w.writerow([e["language"], e["word"], e["pos"], e["reason"], e["gloss"][:150], e["source"], e["url"], note])
json.dump(rows, open("out/lemmas.json", "w"), ensure_ascii=False)
c = collections.Counter(r["language"] for r in rows)
print("lemmas:", len(rows)); print(c.most_common(40))

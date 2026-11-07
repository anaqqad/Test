"""Pass 1: English-Wiktionary data (kaikki.org extraction), one language at a time, streamed.
For every sense: qualifying evidence = politeness tag, politeness category, or a definition that states a politeness
function (request/please, thanks, apology, title of respect, respectful/polite/formal pronoun, honorific/humble).
Writes <lang>.jsonl of candidate senses with evidence and an exclusion record for near-misses.
usage: curl ... | python3 extract_en.py <Language> <outdir>"""
import sys, json, re, unicodedata
LANG, OUT = sys.argv[1], sys.argv[2]
TAGS = {"honorific", "humble", "polite", "respectful", "deferential"}
CATPAT = re.compile(r"\b(honorific|polite|humble|royal|respectful|deferential) terms\b|honorifics\b|honorific (titles|pronouns|prefixes|suffixes|particles)", re.I)
ROYAL_RAW = re.compile(r"\b(royal|royals|royalty|king|monks?|clergy|god|gods)\b", re.I)
EXCL_POS = {"phrase", "proverb", "idiom", "prefix", "suffix", "infix", "affix", "interfix", "circumfix", "character", "symbol",
            "romanization", "punct", "combining_form", "name", "syllable", "contraction"}
G = [  # (function, regex on a single gloss)
 ("request", re.compile(r"^(please|kindly)\b[\s;,.!(]*|used (to make|in making|when making) a (polite )?request|polite request|request politely|softens? (a|the) (request|command|imperative)", re.I)),
 ("gratitude", re.compile(r"^(thank you|thanks|thank-you)\b|express(es|ing)? (one's )?(thanks|gratitude|appreciation)|(an )?(expression|acknowledg(e)?ment) of (thanks|gratitude|appreciation)|used to (express|show) (thanks|gratitude|appreciation)|express(es|ing)? .{0,25}(gratitude|thanks)", re.I)),
 ("apology", re.compile(r"^(sorry|excuse me|pardon( me)?|i beg your pardon|my apologies|forgive me|i'm sorry)\b|apolog(y|ise|ize|etic)|(expression|admission|acknowledg(e)?ment) of (regret|remorse|fault)|express(es|ing)? (regret|remorse)|ask(s|ing)? (for )?(forgiveness|pardon)", re.I)),
 ("address/title", re.compile(r"\b(title of (respect|honou?r)|honorific title|courtesy title|respectful (term|title|form|way|address|appellation|epithet)|term of (respect|respectful address)|polite (form|term|way) of address|form of address for (a )?(man|woman|superior|elder)|used (as a (respectful|polite) (form of address|title)))", re.I)),
 ("title-word", re.compile(r"^(sir|madam|ma'am|mister|mr\.?|mrs\.?|miss|ms\.?|madame|monsieur|lord|lady|master|mistress)( [(;,].*)?$", re.I)),
 ("pronoun", re.compile(r"\byou\b.*\((polite|formal|respectful|honorific|deferential)|\b(polite|formal|respectful|honorific|deferential)\b.{0,25}\byou\b|\b(polite|respectful|honorific|humble)\b.{0,20}\b(I|me|he|she|they|we|pronoun)\b", re.I)),
 ("honorific-gloss", re.compile(r"\b(honorific|humble|deferential|respectful|polite|courteous)\b", re.I)),
]
norm = lambda w: unicodedata.normalize("NFKC", w).strip()
spaced = LANG not in {"Japanese", "Chinese", "Thai", "Lao", "Khmer", "Burmese", "Tibetan", "Dzongkha", "Cantonese", "Mandarin"}
cand = open(f"{OUT}/{LANG}.cand.jsonl", "w"); excl = open(f"{OUT}/{LANG}.excl.jsonl", "w")
n = 0
for line in sys.stdin:
    e = json.loads(line); n += 1
    w, pos = norm(e.get("word", "")), e.get("pos", "")
    ecats = " | ".join(c if isinstance(c, str) else c.get("name", "") for c in e.get("categories", []))
    for s in e.get("senses", []):
        tags = set(s.get("tags", []))
        scats = " | ".join(c if isinstance(c, str) else c.get("name", "") for c in s.get("categories", []))
        glosses = s.get("glosses", []) or s.get("raw_glosses", [])
        gl = glosses[-1] if glosses else ""
        ev = []
        t = sorted(tags & TAGS)
        if t: ev.append("tag:" + ",".join(t))
        rt = [x for x in s.get("raw_tags", []) if ROYAL_RAW.search(x)]  # e.g. Thai/Khmer "of a royal person", "of monks"
        if rt: ev.append("tag:royal/clerical register (" + "; ".join(rt) + ")")
        cm = set(m.group(0).lower() for m in CATPAT.finditer(scats + " | " + ecats) if LANG.lower() in (scats + ecats).lower())
        if cm: ev.append("cat:" + ",".join(sorted(cm)))
        funcs = [f for f, rx in G if any(rx.search(g) for g in glosses)]
        # a bare politeness word in a non-English gloss only counts for interjections/particles/pronouns/nouns of address
        if funcs: ev.append("gloss:" + ",".join(funcs))
        formal_only = ("formal" in tags) and not ev
        if not ev and not formal_only: continue
        rec = {"lang": LANG, "word": w, "pos": pos, "gloss": gl, "glosses": glosses, "tags": sorted(tags), "evidence": ev,
               "form_of": [f.get("word") for f in (s.get("form_of", []) + s.get("alt_of", []))],
               "senseid": s.get("senseid") or s.get("id"), "cats": [c for c in (scats + " | " + ecats).split(" | ") if re.search(r"borrow|slang|Internet|nonstandard|misspell|dialect|humorous|nonce|phrases|idioms|honorific|polite|humble|royal|respect|courtesy|interjection|titles", c, re.I)][:25], "etym": (e.get("etymology_text") or "")[:240], "translit": next((f.get("roman") for f in e.get("forms", []) if f.get("roman")), None) or e.get("head_templates", [{}])[0].get("expansion", "")[:80]}
        reason = None
        allcats = (scats + " | " + ecats)
        if formal_only: reason = "formal only (not specifically polite)"
        elif pos in EXCL_POS: reason = f"part of speech '{pos}' (not a standalone word)"
        elif spaced and " " in w: reason = "multiword expression"
        elif re.search(re.escape(LANG) + r" (phrases|set phrases|idioms|proverbs|sentences|multiword terms|chengyu)\b", allcats, re.I) or re.search(r"\b(Chinese|Japanese|Korean) (idioms|chengyu|four-character idioms)", allcats): reason = "multiword expression (filed as phrase/idiom)"
        elif tags & {"archaic", "obsolete", "historical"}: reason = "archaic/obsolete/historical sense"
        elif "form-of" in tags or "alt-of" in tags or rec["form_of"]: reason = "inflected/alternative form of " + ",".join(x for x in rec["form_of"] if x)
        elif ev == ["gloss:honorific-gloss"] and not (tags & TAGS):
            # definition merely mentions a politeness word: keep only if the gloss describes the word itself as such
            if not re.search(r"^\(?(honorific|humble|polite|respectful|deferential)\b|\b(honorific|humble|polite|respectful|deferential) (form|term|word|equivalent|version|particle|pronoun|verb|title|suffix|prefix|way)\b|\bused (as|in) (a )?(polite|respectful|honorific|humble)", gl, re.I):
                reason = "definition only mentions politeness (not the word's own function)"
        if lang_en := (LANG == "English"):
            if ev and all(x.startswith("gloss:title-word") for x in ev): reason = reason or "English definition is a bare title word (needs a stated respect function)"
        (excl if reason else cand).write(json.dumps({**rec, **({"exclusion": reason} if reason else {})}, ensure_ascii=False) + "\n")
cand.close(); excl.close()
print(LANG, "entries read:", n, file=sys.stderr)

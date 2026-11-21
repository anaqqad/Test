"""Pass 2: specialist dictionaries.
JMdict (EDRDG, CC BY-SA 4.0): senses with misc &hon; &hum; &pol;, or glosses stating a politeness function.
CC-CEDICT (MDBG, CC BY-SA 4.0): definitions labelled polite/honorific/humble/respectful/courteous, or stating a function.
Excluded: expressions (exp), idioms/sayings, affixes, auxiliaries, archaic/obsolete senses."""
import gzip, re, json, xml.etree.ElementTree as ET
import importlib.util
spec = importlib.util.spec_from_file_location("x", "extract_en.py")
G_SRC = open("extract_en.py").read()
G = eval(G_SRC[G_SRC.index("G = [") + 4: G_SRC.index("]\nnorm") + 1].replace("re.compile", "re.compile"), {"re": re})
out = open("data_dicts/Japanese.jmdict.jsonl", "w"); ex = open("data_dicts/Japanese.jmdict.excl.jsonl", "w")
raw = gzip.open("dicts/JMdict_e.gz").read().decode()
raw = re.sub(r"&(\w[\w-]*);", r"\1", raw)  # keep entity names as plain text
root = ET.fromstring(raw[raw.index("<JMdict>"):])
nj = 0
for e in root.iter("entry"):
    kebs = [k.findtext("keb") for k in e.findall("k_ele")]; rebs = [r.findtext("reb") for r in e.findall("r_ele")]
    pos_carry = []
    for s in e.findall("sense"):
        pos = [p.text for p in s.findall("pos")] or pos_carry; pos_carry = pos
        misc = [m.text for m in s.findall("misc")]; gl = [g.text for g in s.findall("gloss")]
        ev = []
        t = [m for m in misc if m in ("hon", "hum", "pol")]
        if t: ev.append("tag:" + ",".join({"hon": "honorific", "hum": "humble", "pol": "polite"}[m] for m in t))
        f = [n for n, rx in G if n != "honorific-gloss" and any(rx.search(x or "") for x in gl)]
        if f: ev.append("gloss:" + ",".join(f))
        if not ev: continue
        word = kebs[0] if kebs else rebs[0]
        rec = {"lang": "Japanese", "word": word, "reading": rebs[0] if rebs else "", "alts": kebs[1:] + rebs, "pos": ",".join(pos), "gloss": "; ".join(gl), "evidence": ev,
               "source": "JMdict", "url": f"https://www.edrdg.org/jmwsgi/entr.py?svc=jmdict&q={e.findtext('ent_seq')}", "ent_seq": e.findtext("ent_seq"), "misc": misc}
        reason = None
        if any(p in ("exp",) for p in pos): reason = "expression (multiword) in JMdict"
        elif any(p.startswith(("suf", "pref", "aux", "ctr")) for p in pos): reason = "affix/auxiliary/counter (not a standalone word)"
        elif any(m in ("arch", "obs", "rare") for m in misc) and not t: reason = "archaic/obsolete/rare sense"
        elif any(m in ("arch", "obs") for m in misc): reason = "archaic/obsolete sense"
        elif any(m in ("id", "yoji", "proverb") for m in misc): reason = "idiom/four-character compound/proverb"
        elif not t and "gloss:pronoun" == ev[0]: pass
        (ex if reason else out).write(json.dumps({**rec, **({"exclusion": reason} if reason else {})}, ensure_ascii=False) + "\n"); nj += 1
out.close(); ex.close()
# CC-CEDICT
out = open("data_dicts/Chinese.cedict.jsonl", "w"); ex = open("data_dicts/Chinese.cedict.excl.jsonl", "w")
LAB = re.compile(r"\((polite|honorific|humble|courteous|respectful|deferential|honorific title|polite form|self-deprecatory|modest)\b[^)]*\)|\b(honorific|humble (term|form|word)|polite (form|term|way|expression)|term of (respect|address)|respectful (term|form|way|address)|courteous (term|form)|deferential|(your|his|her) (esteemed|honou?rable)|(my|our) (humble|unworthy))\b", re.I)
for line in gzip.open("dicts/cedict.txt.gz", "rt"):
    if line.startswith("#"): continue
    m = re.match(r"(\S+) (\S+) \[([^\]]+)\] /(.*)/", line.strip())
    if not m: continue
    trad, simp, pin, defs = m.groups(); ds = defs.split("/")
    ev = []
    lab = [d for d in ds if LAB.search(d)]
    if lab: ev.append("label:" + "; ".join(lab)[:120])
    f = [n for n, rx in G if n not in ("honorific-gloss", "title-word") and any(rx.search(d) for d in ds)]
    if f: ev.append("gloss:" + ",".join(f))
    if not ev: continue
    rec = {"lang": "Chinese", "word": simp, "trad": trad, "pinyin": pin, "gloss": defs[:200], "evidence": ev, "source": "CC-CEDICT",
           "url": "https://www.mdbg.net/chinese/dictionary?page=worddict&wdqb=" + simp}
    reason = None
    if re.search(r"\((idiom|saying|proverb|set phrase|lit\.|abbr\. for|old|archaic|classical|literary)\b", defs, re.I) and not lab: reason = "idiom/saying/archaic or literary (no politeness label)"
    elif re.search(r"\b(idiom|proverb|saying)\b", defs[:60], re.I): reason = "idiom/saying (multiword)"
    elif len(simp) >= 5: reason = "five or more characters: phrase rather than word"
    elif re.match(r"^[A-Za-z]", simp) or "surname" in defs[:30]: reason = "surname/latin entry"
    (ex if reason else out).write(json.dumps({**rec, **({"exclusion": reason} if reason else {})}, ensure_ascii=False) + "\n")
out.close(); ex.close()
print("ok")

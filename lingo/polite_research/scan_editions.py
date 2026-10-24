"""Pass 4: native Wiktionary editions (kaikki.org extractions). Streams one edition, keeps senses of target languages
whose tags/raw tags/categories/glosses carry a politeness label in English or in the edition's own language.
usage: curl .../kaikki.org-dictionary-all.jsonl | python3 scan_editions.py <edition> <outdir>"""
import sys, json, re
ED, OUT = sys.argv[1], sys.argv[2]
CODES = set("ja ko zh cmn yue nan hak th vi id ms jv su ban km bo my lo dz en fr es de it pt ar ru tr hi fa ur bn nl sv pl ta tl ne si mn ml te kn mr".split())
KW = re.compile(r"honorific|humble|\bpolite|respectful|deferential|royal|"
 r"敬語|尊敬|謙譲|丁寧|丁重|美化語|敬称|謙称|尊称|"
 r"높임|겸양|존댓|존칭|겸칭|공손|존대|"
 r"敬辭|敬辞|謙辭|谦辞|敬稱|謙稱|谦称|尊稱|客套|禮貌|礼貌|謙詞|谦词|敬詞|敬词|"
 r"ราชาศัพท์|สุภาพ|ยกย่อง|ถ่อมตน|"
 r"kính ngữ|lịch sự|tôn kính|khiêm|kính trọng|"
 r"\bhormat|\bsopan|\bhalus\b|krama|bahasa istana|diraja|merendah|"
 r"politesse|honorifique|respectueu|déférence|"
 r"höflich|ehrerbiet|Höflichkeit|Ehrentitel|respektvoll|"
 r"cortés|cortesía|honorífic|respetuos|deferencia|"
 r"cortese|cortesia|onorific|rispettos|deferent|"
 r"cortês|polidez|respeitos|deferência|"
 r"вежлив|почтит|уважит|учтив|уничижит|"
 r"grzeczn|uprzejm|honoryfik|z szacunkiem|"
 r"beleefd|eerbiedig|respectvol|"
 r"\bkibar|saygı|nezaket|alçakgönüllü", re.I)
out = open(f"{OUT}/{ED}.jsonl", "w"); n = k = 0
for line in sys.stdin:
    n += 1
    if '"lang_code"' not in line: continue
    e = json.loads(line)
    if e.get("lang_code") not in CODES: continue
    ecats = [c if isinstance(c, str) else c.get("name", "") for c in e.get("categories", [])]
    for s in e.get("senses", []):
        bits = s.get("tags", []) + s.get("raw_tags", []) + [c if isinstance(c, str) else c.get("name", "") for c in s.get("categories", [])] + ecats
        gl = s.get("glosses", []) or s.get("raw_glosses", [])
        lab = [b for b in bits if KW.search(b)]
        glm = [g for g in gl if KW.search(g)]
        if not lab and not glm: continue
        out.write(json.dumps({"edition": ED, "lang_code": e.get("lang_code"), "lang": e.get("lang"), "word": e.get("word"), "pos": e.get("pos"),
                              "labels": lab, "gloss_hits": glm, "glosses": gl, "tags": s.get("tags", []), "form_of": [f.get("word") for f in s.get("form_of", []) + s.get("alt_of", [])]}, ensure_ascii=False) + "\n"); k += 1
out.close(); print(ED, "lines", n, "kept", k, file=sys.stderr)

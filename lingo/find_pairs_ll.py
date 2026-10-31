# Look up the Swadesh core words (swadesh.json) of every language in similar_pairs.json in Lingua Libre's database
# (SPARQL) and write cache/swadesh_found.json: {"<code>|<word>": ["File:LL-... .wav", ...]}. Fast: one query per
# language. python3 find_pairs_ll.py [code ...]
import json, os, sys, time, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
P = json.load(open(os.path.join(HERE, "similar_pairs.json")))
SW = json.load(open(os.path.join(HERE, "swadesh.json")))
OUT = os.path.join(HERE, "cache", "swadesh_found.json")


def sparql(q):
    for i in range(4):
        try:
            r = urllib.request.Request("https://lingualibre.org/bigdata/namespace/wdq/sparql?" + urllib.parse.urlencode({"query": q}),
                                       headers={"Accept": "application/sparql-results+json", "User-Agent": "LingoDudeVideoBot/0.1 (educational videos)"})
            return json.load(urllib.request.urlopen(r, timeout=180))["results"]["bindings"]
        except Exception as e:
            print("  retry", e, flush=True)
            time.sleep(5 * (i + 1))
    return []


langs = {code: qid for p in P.values() for code, qid in p["ll"].items()}
found = json.load(open(OUT)) if os.path.exists(OUT) else {}
for code in sys.argv[1:] or langs:
    qid = langs[code]
    words = sorted({w.strip() for c in SW if c != "_note" for w in SW[c].get(code, "").split("/") if w.strip()})
    for k in [k for k in found if k.startswith(code + "|")]:
        del found[k]
    vals = " ".join('"' + w.replace('"', '\\"') + '"' for w in words)
    for b in sparql(f'SELECT ?w ?f WHERE {{ VALUES ?w {{ {vals} }} ?r prop:P2 entity:Q2 ; prop:P4 entity:{qid} ; prop:P7 ?w ; prop:P3 ?f . }}'):
        found.setdefault(f"{code}|{b['w']['value']}", []).append("File:" + urllib.parse.unquote(b["f"]["value"].split("/")[-1]))
    have = [c for c in SW if c != "_note" and any(found.get(f"{code}|{w.strip()}") for w in SW[c].get(code, "").split("/"))]
    print(code, f"{len(have)} of 41 concepts recorded", flush=True)
    time.sleep(0.3)
json.dump(found, open(OUT, "w"), ensure_ascii=False, indent=0)
print("wrote", OUT, len(found))

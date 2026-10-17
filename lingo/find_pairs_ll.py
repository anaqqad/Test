# Look up the test words of similar_pairs.json in Lingua Libre's database (SPARQL) and write
# cache/similar_found.json: {"<code>|<word>": ["File:LL-... .wav", ...]}. Fast: one query per language per pair.
import json, os, time, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
P = json.load(open(os.path.join(HERE, "similar_pairs.json")))
OUT = os.path.join(HERE, "cache", "similar_found.json")


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


found = {}
for pk, p in P.items():
    for side in ("a", "b"):
        code, qid = p[side], p["ll"][p[side]]
        words = [w[0 if side == "a" else 1] for w in p["words"]]
        vals = " ".join('"' + w.replace('"', '\\"') + '"' for w in words)
        for b in sparql(f'SELECT ?w ?f WHERE {{ VALUES ?w {{ {vals} }} ?r prop:P2 entity:Q2 ; prop:P4 entity:{qid} ; prop:P7 ?w ; prop:P3 ?f . }}'):
            found.setdefault(f"{code}|{b['w']['value']}", []).append("File:" + urllib.parse.unquote(b["f"]["value"].split("/")[-1]))
        missing = [w for w in words if not found.get(f"{code}|{w}")]
        print(pk, code, "missing:", missing, flush=True)
        time.sleep(0.3)
json.dump(found, open(OUT, "w"), ensure_ascii=False, indent=0)
print("wrote", OUT, len(found))

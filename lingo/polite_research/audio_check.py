"""Audio status for the shortlist (Deliverable F). One Wikidata Query Service request per language finds lexemes whose
forms carry a pronunciation recording (P443; Lingua Libre recordings are linked this way). Audio never changes a count or
a rank; it is reported separately. "not found" means not linked on Wikidata, not that no recording exists anywhere.
usage: python3 audio_check.py [top_n_languages]  -> out/shortlist.csv"""
import json, csv, os, sys, time, urllib.parse, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
QID = {"Japanese": "Q5287", "Chinese": "Q727694 wd:Q7850 wd:Q9192", "Thai": "Q9217", "Korean": "Q9176", "Javanese": "Q33549", "Burmese": "Q9228",
       "English": "Q1860", "Indonesian": "Q9240", "Tibetan": "Q34271 wd:Q13955", "Malay": "Q9237", "Polish": "Q809", "Tamil": "Q5885",
       "Finnish": "Q1412", "German": "Q188", "French": "Q150", "Italian": "Q652", "Portuguese": "Q5146", "Khmer": "Q9205", "Vietnamese": "Q9199",
       "Spanish": "Q1321", "Russian": "Q7737", "Swedish": "Q9027", "Hindi": "Q1568", "Arabic": "Q13955", "Persian": "Q9168", "Turkish": "Q256",
       "Bengali": "Q9610", "Urdu": "Q1617", "Dutch": "Q7411", "Tagalog": "Q34057", "Czech": "Q9056", "Romanian": "Q7913", "Malayalam": "Q36236"}
QID["Tibetan"] = "Q34271"
TOP = int(sys.argv[1]) if len(sys.argv) > 1 else 15
summ = list(csv.DictReader(open("out/language_summary.csv")))
short = json.load(open("out/shortlist_candidates.json"))
def sparql(q):
    url = "https://query.wikidata.org/sparql?" + urllib.parse.urlencode({"query": q, "format": "json"})
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "LingoDudeVideoBot/0.1 (research; anaqqad/Test)", "Accept": "application/sparql-results+json"})
            return json.load(urllib.request.urlopen(req, timeout=90))["results"]["bindings"]
        except Exception as e:
            print("  retry", e, file=sys.stderr); time.sleep(70)
    return None
out = []
for s in summ[:TOP]:
    lang = s["language"]; picks = short.get(lang, [])
    spell = {}
    for r in picks:
        for f in [r["lemma"]] + [v for v in r["variants_merged"].split(" | ") if v]:
            spell[f] = r["lemma"]
    found = {}
    if lang in QID:
        vals = " ".join(json.dumps(x, ensure_ascii=False) for x in spell)
        q = f"""SELECT ?s ?audio WHERE {{ VALUES ?s {{ {vals} }} VALUES ?lg {{ wd:{QID[lang]} }}
                ?l dct:language ?lg; wikibase:lemma ?lemma; ontolex:lexicalForm ?f. FILTER(STR(?lemma) = ?s) ?f wdt:P443 ?audio. }}"""
        res = sparql(q)
        status_q = "checked" if res is not None else "query failed"
        for b in res or []:
            found.setdefault(spell[b["s"]["value"]], urllib.parse.unquote(b["audio"]["value"].split("FilePath/")[-1]))
        time.sleep(65)  # WDQS allows 1 request per minute during its current outage
    else:
        status_q = "no Wikidata language id configured"
    for r in picks:
        st = "found" if r["lemma"] in found else ("not found (Wikidata lexemes)" if status_q == "checked" else status_q)
        out.append({"language": lang, "rank": s["rank"], "lemma": r["lemma"], "variants": r["variants_merged"], "transliteration": r["transliteration"],
                    "category": r["primary_category"], "gloss": r["english_gloss"][:120], "sources": r["sources"], "confidence": r["confidence"],
                    "evidence_url": r["source_urls"].split(" ")[0], "audio_status": st, "audio_file": ("File:" + found[r["lemma"]]) if r["lemma"] in found else ""})
    print(lang, sum(1 for r in picks if r["lemma"] in found), "/", len(picks), status_q, flush=True)
# recordings already verified by ear for the current cut of the video (lingo/polite.json)
NAME = {"Chinese": "Chinese", "Japanese": "Japanese", "Javanese": "Javanese", "Korean": "Korean", "Thai": "Thai", "Burmese": "Burmese",
        "Vietnamese": "Vietnamese", "English": "English", "Indonesian": "Indonesian", "Malay": "Malay"}
for it in json.load(open("../polite.json"))["items"]:
    lang = it["name"]; rec = it.get("rec") or (it.get("credit") or {}).get("title", "")
    row = next((o for o in out if o["language"] == lang and o["lemma"].casefold() == it["word"].casefold()), None)
    if row: row.update(audio_status="found (verified, used in current video)", audio_file=rec)
    else:
        rk = next((s["rank"] for s in summ if s["language"] == lang), "")
        out.append({"language": lang, "rank": rk, "lemma": it["word"], "variants": "", "transliteration": it.get("roman", ""), "category": "(signature word in current video)",
                    "gloss": it["lit"], "sources": "", "confidence": "", "evidence_url": "", "audio_status": "found (verified, used in current video)", "audio_file": rec})
out.sort(key=lambda o: (int(o["rank"] or 999), o["audio_status"] != "found (verified, used in current video)"))
with open("out/shortlist.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, list(out[0].keys())); w.writeheader(); w.writerows(out)

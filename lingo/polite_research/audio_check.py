"""Audio status for the shortlist (Deliverable F). Searches Wikimedia Commons for a recording of each word.
Audio never changes a count or a rank; it is reported separately.  usage: python3 audio_check.py [top_n_languages]
Writes out/shortlist.csv and caches answers in out/audio_cache.json."""
import json, csv, os, sys, time, urllib.parse, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
ISO3 = {"Japanese": "jpn", "Chinese": "cmn", "Thai": "tha", "Korean": "kor", "Javanese": "jav", "Burmese": "mya", "English": "eng", "Indonesian": "ind",
        "Tibetan": "bod", "Malay": "msa", "Vietnamese": "vie", "Khmer": "khm", "Polish": "pol", "German": "deu", "French": "fra", "Spanish": "spa",
        "Italian": "ita", "Portuguese": "por", "Russian": "rus", "Swedish": "swe", "Tamil": "tam", "Bengali": "ben", "Hindi": "hin", "Urdu": "urd",
        "Persian": "fas", "Turkish": "tur", "Arabic": "ara", "Dutch": "nld", "Tagalog": "tgl", "Czech": "ces", "Finnish": "fin"}
PREFIX = {"Japanese": "Ja-", "Chinese": "Zh-", "Thai": "Th-", "Korean": "Ko-", "English": "En-", "German": "De-", "French": "Fr-", "Spanish": "Es-",
          "Italian": "It-", "Portuguese": "Pt-", "Russian": "Ru-", "Polish": "Pl-", "Swedish": "Sv-", "Dutch": "Nl-", "Vietnamese": "Vi-"}
TOP = int(sys.argv[1]) if len(sys.argv) > 1 else 15
cache = json.load(open("out/audio_cache.json")) if os.path.exists("out/audio_cache.json") else {}
summ = list(csv.DictReader(open("out/language_summary.csv")))
short = json.load(open("out/shortlist_candidates.json"))
def search(q):
    if q in cache: return cache[q]
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({"action": "query", "list": "search", "srnamespace": 6, "srlimit": 20,
                                                                                "srsearch": q, "format": "json"})
    for attempt in range(5):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "LingoDudeVideoBot/0.1 (research; anaqqad/Test)"})
            res = [h["title"] for h in json.load(urllib.request.urlopen(req, timeout=30))["query"]["search"]]
            cache[q] = res; time.sleep(1.0); return res
        except Exception as e:
            time.sleep(5 * (attempt + 1))
    return None
out = []
for s in summ[:TOP]:
    lang = s["language"]; code = ISO3.get(lang, "")
    for r in short.get(lang, []):
        w = r["lemma"]
        hits = search(f'intitle:"{w}" filemime:audio') or []
        good = [t for t in hits if (f"({code})" in t and (t.endswith(f"-{w}.wav") or t.endswith(f"-{w}.ogg") or f"-{w}." in t))
                or (lang in PREFIX and t.lower().startswith(("file:" + PREFIX[lang]).lower()) and w.lower() in t.lower())]
        status = "found" if good else ("possible (check)" if hits else "not found")
        out.append({"language": lang, "rank": s["rank"], "lemma": w, "variants": r["variants_merged"], "transliteration": r["transliteration"],
                    "category": r["primary_category"], "gloss": r["english_gloss"][:120], "sources": r["sources"], "confidence": r["confidence"],
                    "evidence_url": r["source_urls"].split(" ")[0], "audio_status": status,
                    "audio_file": (good or hits or [""])[0] if status != "not found" else ""})
    json.dump(cache, open("out/audio_cache.json", "w"), ensure_ascii=False)
    print(lang, sum(o["audio_status"] == "found" for o in out if o["language"] == lang), "/", len(short.get(lang, [])), flush=True)
with open("out/shortlist.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, list(out[0].keys())); w.writeheader(); w.writerows(out)

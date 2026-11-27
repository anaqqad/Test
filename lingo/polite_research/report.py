"""Deliverables B, C, E (and the data for F) from out/lemmas.json + logs.  usage: python3 report.py
B out/language_summary.csv   C out/source_inventory.csv   E out/ranking_audit.md   F out/shortlist_candidates.json"""
import json, csv, re, os, collections, glob
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
rows = json.load(open("out/lemmas.json"))
CATS = ["1 request", "2 apology", "3 gratitude", "4 courtesy/polite vocabulary", "5 honorific title/address", "6 respectful pronoun",
        "7 honorific vocabulary", "8 humble vocabulary", "9 deferential vocabulary", "10 royal register", "11 polite particle/interjection/greeting",
        "12 other documented"]
PRELIM = {"Japanese": 848, "Thai": 618, "Chinese": 607, "Korean": 262, "Javanese": 149, "Burmese": 116, "Vietnamese": 90, "Khmer": 81,
          "Tibetan": 48, "English": 44, "Indonesian": 43, "Malay": 42}
# productive honorific formatives: words that are a formative + an ordinary word (counted, but shown separately)
FORMATIVE = {"Japanese": r"^(お|御|ご|おん)", "Thai": r"^(พระ|ทรง|ราช)", "Korean": r"님$", "Chinese": r"^(贵|貴|尊|令|敝|拙|舍|家)", "Burmese": r"^(တော်)|တော်$",
             "Khmer": r"^(ព្រះ)", "Tibetan": r"^(སྐུ|ཕྱག|གསུང|ཐུགས|དབུ)"}
# English-Wiktionary size per language (entries read), as a coverage indicator
size = {}
for log in ("run_all_en.log", "rerun_en.log"):
    if os.path.exists(log):
        for l in open(log):
            m = re.match(r"(.+) entries read: (\d+)", l)
            if m: size[m.group(1)] = int(m.group(2))
NATIVE = {"Japanese": "ja", "Korean": "ko", "Chinese": "zh", "Thai": "th", "Vietnamese": "vi", "Indonesian": "id", "Malay": "ms", "Italian": "it",
          "Portuguese": "pt", "Turkish": "tr", "Polish": "pl", "Spanish": "es", "Dutch": "nl", "Russian": "ru", "German": "de", "French": "fr"}
DICT = {"Japanese": "JMdict", "Chinese": "CC-CEDICT", "Javanese": "Poedjosoedarmo 1969 non-Ngoko word list"}
MISSING = {"Thai": "Royal Institute Dictionary (rachasap lists) not openly downloadable", "Korean": "NIKL Standard Korean Dictionary / Urimalsaem bulk data needs an account",
           "Khmer": "Chuon Nath dictionary, Kbuon Reach Sap (1941) royal vocabulary: no open digital copy found",
           "Tibetan": "zhesa dictionaries (Zhe sa'i tshig mdzod rab gsal me long, 1993; Zhe sa'i lag deb, 2002): no open digital copy found",
           "Javanese": "Bausastra Jawa (Poerwadarminta 1939) not parsed", "Burmese": "Myanmar-English Dictionary (MLC) not openly available",
           "Vietnamese": "no open Vietnamese dictionary with honorific labels found", "Malay": "Kamus Dewan (DBP) not openly downloadable",
           "Indonesian": "KBBI labels (hormat/halus) not bulk-downloadable", "Sundanese": "no open undak-usuk word list found",
           "Balinese": "no open sor-singgih word list found"}
by = collections.defaultdict(list)
for r in rows: by[r["language"]].append(r)
summ = []
for lang, rs in by.items():
    cc = collections.Counter(c for r in rs for c in r["categories"].split("; "))
    pc = collections.Counter(r["primary_category"] for r in rs)
    srcs = collections.Counter(s for r in rs for s in r["sources"].split(" | "))
    only = collections.Counter(r["sources"] for r in rs if r["n_sources"] == 1)
    biggest_only = max(only.values()) if only else 0
    # saturation: if one source alone supplies most lemmas, adding sources is still changing the count (not saturated)
    sat = f"{round(100 * biggest_only / max(1, len(rs)))}%"  # share of lemmas that only one source has
    form = sum(1 for r in rs if lang in FORMATIVE and re.search(FORMATIVE[lang], r["lemma"]))
    func = sum(1 for r in rs if r["primary_category"][:2].strip() in ("1", "2", "3"))
    nsrc_types = len({("native" if "Wiktionary" in s and not s.startswith("English") else s) for s in srcs})
    cov = "stronger" if nsrc_types >= 3 or (nsrc_types >= 2 and lang in DICT) else "partial" if nsrc_types >= 2 or size.get(lang, 0) > 20000 else "thin"
    summ.append({"language": lang, "lemmas_total": len(rs), "high_confidence": sum(r["confidence"] == "high" for r in rs),
                 "in_2plus_sources": sum(r["n_sources"] >= 2 for r in rs), "functional_words_(cat_1-3)": func,
                 "register_words_(cat_4-12)": len(rs) - func, "formative_derived": form, "lemmas_excluding_formative_derived": len(rs) - form,
                 **{f"cat {c}": pc.get(c, 0) for c in CATS},
                 "sources_contributing": "; ".join(f"{s} ({n})" for s, n in srcs.most_common()),
                 "english_wiktionary_entries_for_language": size.get(lang, ""), "native_edition_scanned": NATIVE.get(lang, "none"),
                 "specialist_source": DICT.get(lang, "none"), "lemmas_found_in_only_one_source": "; ".join(f"{k} ({v})" for k, v in only.most_common()),
                 "largest_single_source_share": sat, "known_unused_sources": MISSING.get(lang, ""), "coverage": cov,
                 "preliminary_count": PRELIM.get(lang, "")})
summ.sort(key=lambda r: -r["lemmas_total"])
for i, r in enumerate(summ, 1): r["rank"] = i
with open("out/language_summary.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, ["rank"] + [k for k in summ[0] if k != "rank"]); w.writeheader(); w.writerows(summ)

# C: source inventory
sense_counts = collections.Counter(s for r in rows for s in r["sources"].split(" | "))
INV = [
 ("English Wiktionary (kaikki.org wiktextract)", "used", "https://kaikki.org/dictionary/", "machine-readable extraction of en.wiktionary, dump of 2026-10; ~110 languages streamed", "CC BY-SA 4.0 / GFDL"),
 *[(f"{e} Wiktionary (kaikki.org wiktextract)", "used", f"https://kaikki.org/{e}wiktionary/", "native-edition extraction, all languages, scanned for politeness labels in the edition's own language", "CC BY-SA 4.0 / GFDL")
   for e in ("ja", "ko", "zh", "th", "vi", "id", "ms", "it", "pt", "tr", "pl", "es", "nl", "ru", "de", "fr")],
 ("JMdict", "used", "https://www.edrdg.org/jmdict/j_jmdict.html", "JMdict_e.gz of 2026-10-24; senses tagged hon/hum/pol or with a stated function", "CC BY-SA 4.0 (EDRDG)"),
 ("CC-CEDICT", "used", "https://www.mdbg.net/chinese/dictionary?page=cc-cedict", "cedict release of 2026-10-23; definitions labelled polite/honorific/humble or with a stated function", "CC BY-SA 4.0"),
 ("Poedjosoedarmo 1969 (Cornell)", "used", "https://ecommons.cornell.edu/server/api/core/bitstreams/1055992b-f295-4083-bc22-08923e6f3684/content",
  "S. Poedjosoedarmo, 'Wordlist of Javanese Non-Ngoko Vocabularies', Indonesia (Cornell). Krama and Krama Inggil/Andap columns, OCR + column recovery", "journal article, open access"),
 ("Poedjosoedarmo 1968 'Javanese Speech Levels'", "consulted, not parsed", "https://ecommons.cornell.edu/bitstream/handle/1813/53445/INDO_6_0_1107138592_54_81.pdf", "PDF link returned an HTML page from the sandbox", "open access"),
 ("Wikipedia: Thai honorifics / Royal Thai vocabulary (rachasap)", "consulted (background)", "https://en.wikipedia.org/wiki/Thai_honorifics", "no word count used", "CC BY-SA"),
 ("Royal Institute Dictionary (Thai)", "inaccessible", "https://dictionary.orst.go.th/", "no bulk download / licence for reuse", "copyright"),
 ("NIKL Standard Korean Dictionary / Urimalsaem", "inaccessible", "https://opendict.korean.go.kr/", "bulk download needs a registered account; not attempted", "CC BY-SA 2.0 KR"),
 ("Zhe sa'i tshig mdzod rab gsal me long (1993); Zhe sa'i lag deb (2002)", "inaccessible", "https://mandala.library.virginia.edu/", "Tibetan honorific (zhesa) dictionaries; cited in literature, no open digital text found", "copyright"),
 ("Kyoto University paper on Tibetan honorifics", "consulted (background)", "https://repository.kulib.kyoto-u.ac.jp/", "describes the zhesa system; no list extracted", "open access"),
 ("Kbuon Reach Sap (1941); Chuon Nath Khmer dictionary", "inaccessible", "", "Khmer royal vocabulary; no open digital text found", "copyright"),
 ("Bausastra Jawa (Poerwadarminta 1939)", "not used", "", "scans exist; not parsed in this pass (Poedjosoedarmo used instead)", "public domain in some jurisdictions"),
 ("Mendeley Indonesian-Javanese dataset", "consulted, not used", "https://data.mendeley.com/datasets/y3hstv4bfn", "parallel corpus, no register labels per word", "CC BY 4.0"),
 ("Kamus Dewan (Malay), KBBI (Indonesian)", "inaccessible", "https://kbbi.kemdikbud.go.id/", "online lookup only, no bulk labels", "copyright"),
 ("Lingua Libre / Wikimedia Commons", "used for audio status only", "https://commons.wikimedia.org/", "audio availability checked for the shortlist; does not affect counts", "various CC"),
]
with open("out/source_inventory.csv", "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["source", "status", "url", "what was used / why not", "licence", "lemmas_supported"])
    for name, st, url, note, lic in INV: w.writerow([name, st, url, note, lic, sense_counts.get(name, "")])

# F candidates: per language, a spread over categories, multi-source and high-confidence first
short = {}
for lang, rs in by.items():
    pool = sorted(rs, key=lambda r: (-r["n_sources"], r["confidence"] != "high", len(r["lemma"])))
    pick, seen = [], collections.Counter()
    while len(pick) < min(20, len(pool)):
        added = False
        for c in CATS:
            for r in pool:
                if r not in pick and r["primary_category"] == c and seen[c] <= min(seen.values() or [0]) + 2:
                    pick.append(r); seen[c] += 1; added = True; break
            if len(pick) >= 20: break
        if not added:
            pick += [r for r in pool if r not in pick][:20 - len(pick)]; break
    short[lang] = pick
json.dump(short, open("out/shortlist_candidates.json", "w"), ensure_ascii=False, indent=0)
print("\n".join(f'{r["rank"]:>3} {r["language"]:<12} {r["lemmas_total"]:>5}  hc {r["high_confidence"]:>5}  2src {r["in_2plus_sources"]:>4}  func {r["functional_words_(cat_1-3)"]:>3}  noform {r["lemmas_excluding_formative_derived"]:>5}  {r["coverage"]}' for r in summ[:30]))

# E: ranking audit (markdown) against the preliminary four-Wiktionary ranking
prank = {l: i for i, (l, _) in enumerate(sorted(PRELIM.items(), key=lambda x: -x[1]), 1)}
S = {r["language"]: r for r in summ}
L = ["# Ranking audit: preliminary (four Wiktionaries) vs expanded database", "",
     "Preliminary = the count used in the first cut of the video (four Wiktionary editions, counted 2026-10-24).",
     "Expanded = this database (English Wiktionary for ~110 languages, 16 native Wiktionary editions, JMdict, CC-CEDICT,",
     "Poedjosoedarmo's Javanese list), one rule set for every language, spelling variants merged, expressions removed.", "",
     "| Expanded rank | Language | Expanded count | Without formative-derived words | Preliminary rank | Preliminary count | Coverage | Lemmas only one source has (largest share) |",
     "|---|---|---|---|---|---|---|---|"]
for r in summ[:25]:
    l = r["language"]
    L.append(f'| {r["rank"]} | {l} | {r["lemmas_total"]} | {r["lemmas_excluding_formative_derived"]} | {prank.get(l, "-")} | {PRELIM.get(l, "-")} | {r["coverage"]} | {r["largest_single_source_share"]} |')
L += ["", "## Languages in the preliminary top list", ""]
for l, p in sorted(PRELIM.items(), key=lambda x: -x[1]):
    r = S.get(l)
    if not r: L.append(f"- **{l}**: preliminary {p}, now 0 qualifying lemmas."); continue
    d = r["lemmas_total"] - p
    L.append(f'- **{l}**: {p} → {r["lemmas_total"]} ({"+" if d >= 0 else ""}{d}); rank {prank[l]} → {r["rank"]}. Sources: {r["sources_contributing"]}.')
open("out/ranking_audit_table.md", "w").write("\n".join(L) + "\n")

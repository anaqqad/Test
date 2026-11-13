"""Sound inventories from PHOIBLE 2.0 (phoible.csv): per inventory, consonants / vowels / tones, marginal phonemes excluded.
Per language: median total over its inventories, plus the spread. python3 count.py iso [iso ...]"""
import csv, sys, statistics, collections
inv = collections.defaultdict(lambda: {"c": 0, "v": 0, "t": 0})
meta = {}
for r in csv.DictReader(open("phoible.csv", encoding="utf-8")):
    if r["Marginal"] == "TRUE": continue
    k = r["InventoryID"]; meta[k] = (r["ISO6393"], r["LanguageName"], r["Source"], r["SpecificDialect"])
    inv[k][{"consonant": "c", "vowel": "v", "tone": "t"}[r["SegmentClass"]]] += 1
by = collections.defaultdict(list)
for k, d in inv.items(): by[meta[k][0]].append((k, d, meta[k]))
for iso in sys.argv[1:]:
    L = by.get(iso, [])
    if not L: print(iso, "not in PHOIBLE"); continue
    tot = sorted(d["c"] + d["v"] + d["t"] for _, d, _ in L)
    print(f"{iso} {L[0][2][1]}: {len(L)} inventories, totals {tot}, median {statistics.median(tot)}")
    for k, d, m in L: print(f"    #{k} {m[2]:8s} {m[3] or '':25s} C{d['c']} V{d['v']} T{d['t']} = {d['c']+d['v']+d['t']}")

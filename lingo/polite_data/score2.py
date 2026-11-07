import sys,json,unicodedata; sys.path.insert(0,'.')
from catpage import walk
import opencc
t2s=opencc.OpenCC('t2s')
S=json.load(open('polite_sources.json'))
SPACED={"English","Indonesian","Malay","Tagalog","Korean","Italian","Portuguese","Spanish","French","German","Polish","Turkish","Persian","Hindi","Urdu","Bengali","Tamil","Marathi","Malayalam","Kannada","Sinhalese","Mongolian","Balinese","Sundanese","Nepali","Javanese","Khmer"}
def norm(l,w):
    w=unicodedata.normalize("NFKC",w).strip()
    if l=="Chinese": w=t2s.convert(w)
    return w.lower()
res={}
for l,srcs in S.items():
    allw={}
    for s,ws in srcs.items():
        for w in ws: allw.setdefault(w,set()).add(s)
    phrase=set()
    if len(allw)>=20:
        for p in ["phrases","idioms","proverbs","set phrases"]:
            phrase|=walk("en.wiktionary.org",f"Category:{l} {p}")
        if l=="Japanese":
            for c in ["カテゴリ:日本語 成句","カテゴリ:日本語 慣用句","カテゴリ:日本語 ことわざ"]: phrase|=walk("ja.wiktionary.org",c)
    kept={};drop=[]
    for w,ss in allw.items():
        if w in phrase or (l in SPACED and " " in w.strip()): drop.append(w); continue
        kept.setdefault(norm(l,w),set()).update(ss)
    per={s:sum(1 for v in kept.values() if s in v) for s in srcs}
    res[l]={"total":len(kept),"raw":len(allw),"dropped":sorted(drop),"per_source":per,"words":{k:sorted(v) for k,v in sorted(kept.items())}}
    print(f"{l:12s} total {len(kept):5d} raw {len(allw):5d} dropped {len(drop):4d} {per} e.g. {sorted(drop)[:4]}",flush=True)
json.dump(res,open('polite_scores.json','w'),ensure_ascii=False,indent=1)

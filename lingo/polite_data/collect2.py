import sys,json; sys.path.insert(0,'.')
from catpage import walk
src={}
en=json.load(open('en_polite_cats.json'))
for cat in en:
    lang=cat[9:].rsplit(" ",2)[0]
    p=walk("en.wiktionary.org",cat); src.setdefault(lang,{}).setdefault("en",set()).update(p)
    print("en",cat,len(p),flush=True)
JA={"日本語":"Japanese","朝鮮語":"Korean","中国語":"Chinese","閩南語":"Chinese","広東語":"Chinese","客家語":"Chinese","ジャワ語":"Javanese","チベット語":"Tibetan","ベトナム語":"Vietnamese"}
for jl,lang in JA.items():
    p=walk("ja.wiktionary.org",f"カテゴリ:{jl} 敬語",2); src.setdefault(lang,{}).setdefault("ja",set()).update(p); print("ja",jl,len(p),flush=True)
for kl,lang in {"한국어":"Korean","일본어":"Japanese","타이어":"Thai","영어":"English"}.items():
    for k in ["높임말","겸양어"]:
        p=walk("ko.wiktionary.org",f"분류:{kl} {k}",1); src.setdefault(lang,{}).setdefault("ko",set()).update(p); print("ko",kl,k,len(p),flush=True)
for c in ["หมวดหมู่:ราชาศัพท์ภาษาไทย","หมวดหมู่:คำราชาศัพท์ภาษาไทย"]:
    p=walk("th.wiktionary.org",c,1); src.setdefault("Thai",{}).setdefault("th",set()).update(p); print("th",c,len(p),flush=True)
json.dump({l:{k:sorted(v) for k,v in d.items()} for l,d in src.items()},open('polite_sources.json','w'),ensure_ascii=False,indent=1)
print("DONE",flush=True)

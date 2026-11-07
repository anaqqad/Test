"""List every Commons file still needed (not yet downloaded), with direct URL and size, -> out/needed.json"""
import json, os, random, re, subprocess
import fetch_audio as fa
videos = json.loads(subprocess.run(["node", "-e", "import('./videos.mjs').then(m=>console.log(JSON.stringify(m.VIDEOS)))"], capture_output=True, text=True, check=True).stdout)
have = set(os.listdir(os.path.join(fa.CACHE, "raw")))
out = []
for vk in ["sounds", "niche", "conlangs", "revived", "hardest"]:
    man = os.path.join(fa.CACHE, "audio", vk, "manifest.json")
    man = json.load(open(man)) if os.path.exists(man) else {}
    for item in videos[vk]["items"]:
        a = item.get("audio")
        if not a or man.get(item["name"]):
            continue
        if "file" in a:
            titles = [a["file"]]
        elif "seq" in a:
            titles = a["seq"]
        else:
            ts = fa.ll_titles(a["ll"]); rnd = random.Random(item["name"]); chosen = []
            for w in a.get("words") or []:
                hit = [t for t in ts if t.rsplit("-", 1)[-1].rsplit(".", 1)[0].lower() == w.lower()]
                if hit: chosen.append(hit[0])
            pool = [t for t in ts if len(t.rsplit("-", 1)[-1]) < 18 and not re.search(r"\d", t.rsplit("-", 1)[-1])]
            while len(chosen) < a.get("n", 6) and pool:
                chosen.append(pool.pop(rnd.randrange(len(pool))))
            titles = chosen
        for t in titles:
            m = fa.info(t)
            if not m: print("missing", t); continue
            name = re.sub(r"[^\w.-]", "_", m["title"][5:])[:80] + os.path.splitext(__import__("urllib.parse").parse.urlparse(m["url"]).path)[1]
            if name in have: continue
            out.append({"video": vk, "lang": item["name"], "title": m["title"], "url": m["url"], "save_as": name})
json.dump(out, open("out/needed.json", "w"), indent=1, ensure_ascii=False)
print(len(out), "files")

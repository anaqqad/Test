"""Download links for the ranking video's recordings (for the owner to fetch on their own connection)."""
import hashlib, json, subprocess, urllib.parse
import fetch_audio as fa
videos = json.loads(subprocess.run(["node", "-e", "import('./videos.mjs').then(m=>console.log(JSON.stringify(m.VIDEOS)))"], capture_output=True, text=True, check=True).stdout)
out = []
for item in videos["hardest"]["items"]:
    a = item["audio"]
    if "file" in a:
        f = a["file"].replace(" ", "_"); h = hashlib.md5(f.encode()).hexdigest(); q = urllib.parse.quote(f)
        out.append({"lang": item["name"], "word": "(video)", "url": f"https://upload.wikimedia.org/wikipedia/commons/transcoded/{h[0]}/{h[:2]}/{q}/{q}.240p.vp9.webm"})
        continue
    for t in fa.pick_ll(fa.ll_titles(a["ll"]), item["name"], a["ll"], a.get("n", 3)):
        f = t[5:].replace(" ", "_"); h = hashlib.md5(f.encode()).hexdigest()
        out.append({"lang": item["name"], "word": fa.ll_word(t), "url": f"https://upload.wikimedia.org/wikipedia/commons/{h[0]}/{h[:2]}/{urllib.parse.quote(f)}"})
json.dump(out, open("out/hardest_links.json", "w"), indent=1, ensure_ascii=False)
cur = None
for i, x in enumerate(out, 1):
    if x["lang"] != cur:
        cur = x["lang"]; print(f"\n**{cur}**")
    print(f"{i}. {x['url']}   ({x['word']})")

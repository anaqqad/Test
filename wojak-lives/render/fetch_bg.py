"""Finds free-licence photos on Wikimedia Commons and downloads 1280px-wide versions.

    python3 wojak-lives/render/fetch_bg.py OUT_DIR "query one" "query two" ...

Saves <OUT_DIR>/<slug>_<n>.jpg candidates plus credits.json (author + licence for the video description).
"""
import json
import pathlib
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

API = "https://commons.wikimedia.org/w/api.php"
UA = {"User-Agent": "WojakLivesBot/0.1 (personal YouTube project; contact via repo owner)"}


def get(url, tries=5):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code != 429 or i == tries - 1:
                raise
            time.sleep(5 * 2 ** i)  # Wikimedia rate limit: back off


def search(query, limit=4):
    q = urllib.parse.urlencode({
        "action": "query", "format": "json", "generator": "search", "gsrnamespace": 6,
        "gsrsearch": f"{query} filetype:bitmap -painting -drawing", "gsrlimit": 25,
        "prop": "imageinfo", "iiprop": "url|size|extmetadata", "iiurlwidth": 1280})
    pages = json.loads(get(f"{API}?{q}")).get("query", {}).get("pages", {}).values()
    good = []
    for pg in sorted(pages, key=lambda p: p.get("index", 0)):
        ii = pg["imageinfo"][0]
        meta = ii.get("extmetadata", {})
        lic = meta.get("LicenseShortName", {}).get("value", "")
        if ii["width"] < 1200 or not pg["title"].lower().endswith((".jpg", ".jpeg")):
            continue
        if not re.search(r"CC0|CC BY|Public domain", lic, re.I):
            continue
        artist = re.sub("<[^>]+>", "", meta.get("Artist", {}).get("value", "")).strip()
        good.append({"title": pg["title"], "url": ii["thumburl"], "license": lic, "artist": artist,
                     "page": ii["descriptionurl"]})
        if len(good) == limit:
            break
    return good


if __name__ == "__main__":
    out = pathlib.Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    credits_path = out / "credits.json"
    credits = json.loads(credits_path.read_text()) if credits_path.exists() else {}
    for query in sys.argv[2:]:
        slug = re.sub(r"\W+", "_", query.lower()).strip("_")
        for n, hit in enumerate(search(query)):
            name = f"{slug}_{n}.jpg"
            if not (out / name).exists():
                (out / name).write_bytes(get(hit["url"]))
                time.sleep(1.5)
            credits[name] = hit
            print(name, "|", hit["title"], "|", hit["license"])
    credits_path.write_text(json.dumps(credits, indent=1))

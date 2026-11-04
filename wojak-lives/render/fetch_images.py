"""Fetch free background / item photos from Openverse (CC0 + public domain only: no credit needed).

    python3 fetch_images.py sources.json            # {"list/bg/basque.jpg": "basque country mountains", ...}
    python3 fetch_images.py sources.json --skip 1   # re-fetch everything with the next-best result

Keys are paths under assets/. Paths in list/bg/ need a wide image >= 1600 px; others >= 700 px.
Existing files are kept (delete one to re-fetch it, or add "query#2" to take the 2nd candidate).
Always look at a contact sheet afterwards: search results can be off-topic.
"""
import io
import json
import pathlib
import subprocess
import sys
import urllib.parse

from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
API = "https://api.openverse.org/v1/images/?"


def get(url, timeout=40):
    return subprocess.run(["curl", "-sSfL", "-m", str(timeout), "-A", "WojakLives-render/1.0", url],
                          check=True, capture_output=True).stdout


def fetch(dest, query, skip=0):
    pick = skip
    if "#" in query:
        query, n = query.rsplit("#", 1)
        pick = int(n) - 1
    bg = "/bg/" in dest
    q = dict(q=query, license="cc0,pdm", page_size=20, mature="false")
    if bg:
        q.update(aspect_ratio="wide", size="large")
    res = json.loads(get(API + urllib.parse.urlencode(q)))["results"]
    ok = 0
    for r in res:
        if (r.get("width") or 0) < (1600 if bg else 700):
            continue
        try:
            im = Image.open(io.BytesIO(get(r["url"]))).convert("RGB")
        except Exception:
            continue
        if bg and im.width / im.height < 1.3:
            continue
        if ok < pick:
            ok += 1
            continue
        im.thumbnail((2400, 2400))
        out = HERE / "assets" / dest
        out.parent.mkdir(parents=True, exist_ok=True)
        im.save(out, quality=90)
        return f"{dest}  <- {r['url']} ({r['license']})"
    return f"{dest}  !! nothing usable for '{query}'"


def main():
    src = json.load(open(sys.argv[1]))
    skip = int(sys.argv[sys.argv.index("--skip") + 1]) if "--skip" in sys.argv else 0
    for dest, query in src.items():
        if (HERE / "assets" / dest).exists() and "#" not in query and not skip:
            continue
        try:
            print(fetch(dest, query, skip), flush=True)
        except Exception as e:  # network hiccup: report and go on
            print(f"{dest}  !! {e}", flush=True)


if __name__ == "__main__":
    main()

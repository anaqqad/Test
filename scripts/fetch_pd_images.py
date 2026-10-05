#!/usr/bin/env python3
"""Download public-domain artwork for a MathDoc spec from Wikimedia Commons.

Usage:
    python3 scripts/fetch_pd_images.py data/mathdoc-eratosthenes.json

The spec lists images under "assets": {"<key>": {"commons": "File:<title>"}}.
Each file's license is read from Commons metadata before anything is downloaded.
Only "Public domain" / CC0 files are accepted; anything else is reported and skipped,
and the beat that uses it renders as an explicit placeholder card.

Output:
    public/pd/<spec.id>/<key>.jpg      resized to at most 1920 px wide
    public/pd/<spec.id>/credits.json   title, artist, license and source URL per key
"""

from __future__ import annotations

import html
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "https://commons.wikimedia.org/w/api.php"
UA = {"User-Agent": "black-history-room-reels/1.0 (https://github.com/anaqqad/Test)"}
ACCEPTED = ("public domain", "cc0", "pd-")
WIDTH = 1920
# Wikimedia throttles original files and only renders thumbnails at these widths (https://w.wiki/GHai)
STANDARD_WIDTHS = (330, 500, 960, 1280, 1920)


def thumb_url(info: dict) -> str:
    """Largest standard-width thumbnail that doesn't upscale the original."""
    width = info.get("width") or 0
    if width >= WIDTH and info.get("thumburl"):
        return info["thumburl"]
    fitting = [w for w in STANDARD_WIDTHS if w <= width]
    if not fitting:
        return info["url"]
    w = fitting[-1]
    base, name = info["url"].split("?", 1)[0].rsplit("/", 1)
    return f"{base.replace('/commons/', '/commons/thumb/', 1)}/{name}/{w}px-{name}"


def fetch(url: str) -> bytes:
    for attempt in range(8):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code != 429:
                raise
            wait = 15 * (attempt + 1)
            print(f"  rate limited, retrying in {wait}s")
            time.sleep(wait)
    raise SystemExit(f"Commons kept rate-limiting {url}")


def strip_tags(s: str) -> str:
    text = html.unescape(re.sub(r"<[^>]+>", "", s or ""))
    # Commons appends Wikidata statements such as "date QS:P571,+1635-00-00T..." to dates
    return re.sub(r"\s*date QS:.*$", "", text).strip()


def save_jpeg(raw: bytes, target: Path) -> tuple[int, int]:
    """Re-encode at quality 88 so a single painting doesn't weigh several MB. Returns the saved size."""
    from io import BytesIO

    from PIL import Image

    img = Image.open(BytesIO(raw)).convert("RGB")
    if img.width > WIDTH:
        img = img.resize((WIDTH, round(img.height * WIDTH / img.width)), Image.LANCZOS)
    img.save(target, "JPEG", quality=88, optimize=True)
    return img.width, img.height


def main() -> None:
    spec_path = Path(sys.argv[1])
    spec = json.loads(spec_path.read_text())
    assets = spec.get("assets", {})
    out_dir = ROOT / "public" / "pd" / spec["id"]
    out_dir.mkdir(parents=True, exist_ok=True)
    credits_path = out_dir / "credits.json"
    credits = json.loads(credits_path.read_text()) if credits_path.exists() else {}

    todo = {k: v for k, v in assets.items() if not (out_dir / f"{k}.jpg").exists() or k not in credits}
    if not todo:
        print("All images already downloaded.")
        return

    titles = [v["commons"] for v in todo.values()]
    q = urllib.parse.urlencode(
        {
            "action": "query",
            "prop": "imageinfo",
            "iiprop": "url|extmetadata|size",
            "iiurlwidth": WIDTH,
            "format": "json",
            "titles": "|".join(titles),
        }
    )
    data = json.loads(fetch(f"{API}?{q}"))
    # Commons normalises titles (e.g. underscores); map back to our keys
    norm = {n["to"]: n["from"] for n in data["query"].get("normalized", [])}
    by_title = {}
    for page in data["query"]["pages"].values():
        by_title[norm.get(page["title"], page["title"])] = page

    for key, entry in todo.items():
        page = by_title.get(entry["commons"])
        if not page or "imageinfo" not in page:
            print(f"  ! {key}: {entry['commons']} not found on Commons")
            continue
        info = page["imageinfo"][0]
        meta = info.get("extmetadata", {})
        license_name = strip_tags(meta.get("LicenseShortName", {}).get("value", ""))
        if not license_name.lower().startswith(ACCEPTED):
            print(f"  ! {key}: license '{license_name}' is not public domain, skipped")
            continue
        url = thumb_url(info)
        print(f"  fetching {key}: {url}")
        width, height = save_jpeg(fetch(url), out_dir / f"{key}.jpg")
        credits[key] = {
            "title": page["title"],
            "artist": strip_tags(meta.get("Artist", {}).get("value", "")),
            "date": strip_tags(meta.get("DateTimeOriginal", {}).get("value", "")),
            "license": license_name,
            "source": info.get("descriptionurl", ""),
            # pixel size of the saved file: the Reel template needs it to place faces exactly
            "width": width,
            "height": height,
        }
        # save after every file so an interrupted run keeps what it already has
        credits_path.write_text(json.dumps(credits, indent=2, ensure_ascii=False) + "\n")
        print(f"  ok {key}: {page['title']} ({license_name})")
        time.sleep(4)


if __name__ == "__main__":
    main()

"""Download the AWM photos listed in tools/awm_stills.json (the AWM's own 'Low Res' download, ~640 px; all marked
'Copyright expired - public domain') into assets/stills/. Usage: python tools/fetch_awm.py"""
import json, time, urllib.request
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
UA = "WWIIFrontlinesResearch/1.0 (documentary research)"
rows = json.loads((ROOT / "tools/awm_stills.json").read_text(encoding="utf-8"))
for k, r in rows.items():
    out = ROOT / "assets/stills" / r["name"]
    if out.exists(): continue
    with urllib.request.urlopen(urllib.request.Request(r["url"], headers={"User-Agent": UA}), timeout=60) as f:
        out.write_bytes(f.read())
    print(r["name"], out.stat().st_size); time.sleep(0.5)

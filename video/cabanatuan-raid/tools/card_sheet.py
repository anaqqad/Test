"""Contact sheet of rendered overlay cards (one frame at 65 % of each card, composited on dark grey so transparent
cards are readable): python tools/card_sheet.py [ids...] -> build/cards_N.jpg"""
import io, json, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
sb = json.load(open(ROOT / "build/storyboard.json", encoding="utf-8"))
want = set(sys.argv[1:])
ov = [o for o in sb["overlays"] if o["type"] != "ContextTag" and (not want or o["id"] in want) and (ROOT / f"build/overlays/{o['id']}.webm").exists()]
W, H, C = 480, 270, 4
for part in range(0, len(ov), 24):
    chunk = ov[part:part + 24]
    sheet = Image.new("RGB", (W * C, H * ((len(chunk) + C - 1) // C)), (20, 20, 20))
    for i, o in enumerate(chunk):
        t = (o["end"] - o["start"]) * 0.65
        b = subprocess.run(["ffmpeg", "-v", "error", "-c:v", "libvpx-vp9", "-ss", f"{t:.2f}", "-i", str(ROOT / f"build/overlays/{o['id']}.webm"),
                            "-frames:v", "1", "-vf", f"scale={W}:{H}", "-f", "image2pipe", "-c:v", "png", "-"], capture_output=True).stdout
        bg = Image.new("RGBA", (W, H), (70, 70, 70, 255))
        if b:
            bg.alpha_composite(Image.open(io.BytesIO(b)).convert("RGBA"))
        im = bg.convert("RGB"); d = ImageDraw.Draw(im)
        d.rectangle((0, 0, 200, 13), fill=(0, 0, 0)); d.text((2, 1), o["id"], fill=(255, 255, 0))
        sheet.paste(im, ((i % C) * W, (i // C) * H))
    sheet.save(ROOT / f"build/cards_{part // 24}.jpg", quality=86)
    print("sheet", part // 24, len(chunk))

"""Thumbnails for this episode: python tools/thumbs_episode.py -> thumbnail/thumbnail_A.jpg, thumbnail_B.jpg"""
import json
from pathlib import Path
import numpy as np
P = Path(__file__).resolve().parent / "thumbnail.py"
src = P.read_text(encoding="utf-8"); src = src[:src.index('if __name__ == "__main__":')]
g = {"__file__": str(P)}; exec(src, g)
ROOT, T, from_image, W, H = g["ROOT"], g["T"], g["from_image"], g["W"], g["H"]
from PIL import Image, ImageEnhance
# A: the captured U-505 under the U.S. flag, 4 June 1944 (U.S. Navy 80-G-49172, public domain)
im = Image.open(ROOT / "assets/stills/towline_party.jpg").convert("RGB")
im = im.crop((0, 300, 1920, 1380))
ImageEnhance.Brightness(ImageEnhance.Contrast(im).enhance(1.25)).enhance(0.8).save(T / "sub_base.jpg", quality=95)
from_image(T / "sub_base.jpg", "thumbnail_A", "DECLARED", "DEAD?!", "U-505 CREW · LOUISIANA 1944", [(500, 330), (640, 300), (780, 250)], text_x=60, size=128)
# B: Gallery's memo of 14 June 1944, the highlighted sentence (U.S. Navy, public domain)
spans = json.load(open(ROOT / "tools/doc_spans.json", encoding="utf-8"))["doc_memo"]["rects"]
im = Image.open(ROOT / "assets/stills/doc_memo.png").convert("RGB")
x0, y0, cw = 0, 330, 1440
im = im.crop((x0, y0, x0 + cw, y0 + int(cw * 9 / 16))).resize((W, H), Image.LANCZOS)
k = W / cw
a = np.asarray(im).astype(np.float32) * 0.8
hl = np.zeros_like(a[..., 0])
for rx, ry, rw, rh in spans:
    hl[max(0, int((ry - y0) * k)):int((ry - y0 + rh) * k), int((rx - x0) * k):int((rx - x0 + rw) * k)] = 1
band = (np.arange(H)[:, None, None] < 250).astype(np.float32)
a = a * (1 - 0.85 * band)
Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(T / "memo_base.jpg", quality=95)
from_image(T / "memo_base.jpg", "thumbnail_B", "KEEP YOUR", "MOUTHS SHUT?!", "TOP SECRET · JUNE 14, 1944", [(1150, 240), (1120, 300), (1080, 345)], text_x=60, size=112)
from PIL import ImageDraw
out = Image.open(T / "thumbnail_B.jpg").convert("RGB"); d = ImageDraw.Draw(out, "RGBA")
for rx, ry, rw, rh in spans:
    d.rectangle([int((rx - x0) * k) - 4, int((ry - y0) * k) - 2, int((rx - x0 + rw) * k) + 4, int((ry - y0 + rh) * k) + 2], fill=(224, 68, 46, 95))
g["arrow"](out, [(1150, 240), (1120, 300), (1080, 345)])
out.save(T / "thumbnail_B.jpg", quality=92)

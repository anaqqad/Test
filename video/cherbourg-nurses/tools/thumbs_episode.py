"""Thumbnails for this episode: python tools/thumbs_episode.py -> thumbnail/thumbnail_A.jpg, thumbnail_B.jpg"""
import json
from pathlib import Path
import numpy as np
P = Path(__file__).resolve().parent / "thumbnail.py"
src = P.read_text(encoding="utf-8"); src = src[:src.index('if __name__ == "__main__":')]
g = {"__file__": str(P)}; exec(src, g)
ROOT, T, from_image, W, H = g["ROOT"], g["T"], g["from_image"], g["W"], g["H"]
from PIL import Image, ImageEnhance, ImageDraw
# A: the German nurses at Balleroy, 2 July 1944 (U.S. Army Signal Corps, via PhotosNormandie, CC BY-SA 2.0)
im = Image.open(ROOT / "assets/stills/nurses_balleroy.jpg").convert("RGB").crop((0, 560, 1920, 1640))
ImageEnhance.Brightness(ImageEnhance.Contrast(im).enhance(1.2)).enhance(0.82).save(T / "nurses_base.jpg", quality=95)
from_image(T / "nurses_base.jpg", "thumbnail_A", "SENT", "BACK?!", "GERMAN NURSES · NORMANDY 1944", [(380, 330), (520, 360), (640, 410)], text_x=60, size=140)
# B: 1929 Geneva Convention, art. 12, the highlighted sentence (Library of Congress, public domain)
spans = json.load(open(ROOT / "tools/doc_spans.json", encoding="utf-8"))["doc_art12"]["rects"]
im = Image.open(ROOT / "assets/stills/doc_art12.png").convert("RGB")
x0, y0, cw = 60, 780, 1300
im = im.crop((x0, y0, x0 + cw, y0 + int(cw * 9 / 16))).resize((W, H), Image.LANCZOS)
k = W / cw
a = np.asarray(im).astype(np.float32) * 0.78
a = a * (1 - 0.85 * (np.arange(H)[:, None, None] < 240))
Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(T / "law_base.jpg", quality=95)
pts = [(1200, 230), (1120, 290), (1000, 335)]
from_image(T / "law_base.jpg", "thumbnail_B", "\"SHALL BE", "SENT BACK\"?!", "GENEVA CONVENTION · 1929", pts, text_x=60, size=108)
out = Image.open(T / "thumbnail_B.jpg").convert("RGB"); d = ImageDraw.Draw(out, "RGBA")
for rx, ry, rw, rh in spans:
    d.rectangle([int((rx - x0) * k) - 4, int((ry - y0) * k) - 2, int((rx - x0 + rw) * k) + 4, int((ry - y0 + rh) * k) + 2], fill=(224, 68, 46, 95))
g["arrow"](out, pts)
out.save(T / "thumbnail_B.jpg", quality=92)

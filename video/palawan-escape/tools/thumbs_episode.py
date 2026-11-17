"""Thumbnails for this episode: python tools/thumbs_episode.py -> thumbnail/thumbnail_A.jpg, thumbnail_B.jpg"""
from pathlib import Path
import json
P = Path(__file__).resolve().parent / "thumbnail.py"
src = P.read_text(encoding="utf-8"); src = src[:src.index('if __name__ == "__main__":')]
g = {"__file__": str(P)}; exec(src, g)
ROOT, T, from_image, W, H = g["ROOT"], g["T"], g["from_image"], g["W"], g["H"]
import numpy as np
from PIL import Image, ImageEnhance

# A: one of the camp's air raid shelters, by the fence, with the bay behind (USAF 58405AC, NARA 342-FH, public domain)
im = Image.open(ROOT / "assets/stills/shelter_fence_1945.jpg").convert("L").convert("RGB")
w, h = im.size
x0, y0, cw = int(w * 0.09), int(h * 0.2), int(w * 0.81)
im = im.crop((x0, y0, x0 + cw, y0 + int(cw * 9 / 16))).resize((W, H), Image.LANCZOS)
a = np.asarray(ImageEnhance.Contrast(im).enhance(1.35)).astype(np.float32)
band = np.clip(1 - (np.arange(H) - 210) / 170, 0, 1)[:, None, None]
a = a * (1 - 0.72 * band)
Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(T / "shelter_base.jpg", quality=95)
from_image(T / "shelter_base.jpg", "thumbnail_A", "150 WENT IN.", "11 CAME OUT.", "PALAWAN · DEC 14, 1944", [(560, 560), (420, 545), (300, 525)], text_x=40, size=118)
# B: the prison camp at Puerto Princesa, March 1945 (Signal Corps, NARA 111-SCA album 2985, public domain)
crop = json.load(open(ROOT / "tools/crops.json", encoding="utf-8"))["camp_front_1945.jpg"]
im = Image.open(ROOT / "assets/stills/camp_front_1945.jpg").convert("L").convert("RGB")
w, h = im.size
x0, y0, cw = int(w * crop[0]), int(h * (crop[1] + 0.12)), int(w * crop[2])
im = im.crop((x0, y0, x0 + cw, y0 + int(cw * 9 / 16))).resize((W, H), Image.LANCZOS)
a = np.asarray(ImageEnhance.Contrast(im).enhance(1.3)).astype(np.float32)
band = np.clip(1 - (np.arange(H) - 210) / 170, 0, 1)[:, None, None]
a = a * (1 - 0.7 * band)
Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(T / "camp_base.jpg", quality=95)
from_image(T / "camp_base.jpg", "thumbnail_B", "THE AIR RAID", "WAS A LIE.", "PALAWAN · DEC 14, 1944", [(760, 330), (700, 390), (640, 440)], text_x=40, size=116)

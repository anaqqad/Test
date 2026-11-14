"""Thumbnails for this episode: python tools/thumbs_episode.py -> thumbnail/thumbnail_A.jpg, thumbnail_B.jpg"""
from pathlib import Path
P = Path(__file__).resolve().parent / "thumbnail.py"
src = P.read_text(encoding="utf-8"); src = src[:src.index('if __name__ == "__main__":')]
g = {"__file__": str(P)}; exec(src, g)
ROOT, T, from_image, W, H = g["ROOT"], g["T"], g["from_image"], g["W"], g["H"]
from PIL import Image, ImageEnhance
# A: a young German prisoner, November 1944 (U.S. Army Signal Corps SC 196558, public domain; cap badges blurred)
im = Image.open(ROOT / "assets/stills/young_pows_1944.jpg").convert("RGB").crop((0, 0, 1700, 956))
ImageEnhance.Brightness(ImageEnhance.Contrast(im).enhance(1.25)).enhance(0.9).save(T / "pow_base.jpg", quality=95)
from_image(T / "pow_base.jpg", "thumbnail_A", "YOU SPEAK", "GERMAN?!", "GERMAN POWs · 1944", [(590, 470), (660, 420), (735, 360)], text_x=50, size=128)
# B: "A Daily Scene in Busy New Ulm, 1918" (postcard, public domain)
im = Image.open(ROOT / "assets/stills/new_ulm_1918.jpg").convert("RGB").crop((10, 10, 950, 539))
ImageEnhance.Contrast(im).enhance(1.35).save(T / "street_base.jpg", quality=95)
from_image(T / "street_base.jpg", "thumbnail_B", "THE WHOLE TOWN", "SPOKE GERMAN?!", "NEW ULM, MINNESOTA", [(800, 440), (900, 385), (990, 335)], text_x=50, size=104)

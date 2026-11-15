"""Thumbnails for this episode: python tools/thumbs_episode.py -> thumbnail/thumbnail_A.jpg, thumbnail_B.jpg"""
from pathlib import Path
P = Path(__file__).resolve().parent / "thumbnail.py"
src = P.read_text(encoding="utf-8"); src = src[:src.index('if __name__ == "__main__":')]
g = {"__file__": str(P)}; exec(src, g)
ROOT, T, from_image, W, H = g["ROOT"], g["T"], g["from_image"], g["W"], g["H"]
from PIL import Image, ImageEnhance
# A: a German prisoner at Camp Wallace, Texas, 1943 (U.S. Army Signal Corps SC 184883, public domain)
im = Image.open(ROOT / "assets/stills/wallace_watchmaker.jpg").convert("RGB").crop((400, 0, 1920, 855))
ImageEnhance.Brightness(ImageEnhance.Contrast(im).enhance(1.3)).enhance(0.8).save(T / "pow_base.jpg", quality=95)
from_image(T / "pow_base.jpg", "thumbnail_A", "1,000 BURNED", "THEIR UNIFORMS?!", "GERMAN POWs IN AMERICA", [(560, 560), (660, 560), (760, 520)], text_x=40, size=104)
# B: Camp Butner, N.C., wartime postcard (State Archives of North Carolina, no known restrictions)
im = Image.open(ROOT / "assets/stills/butner_postcard.jpg").convert("RGB").crop((0, 70, 1280, 790))
ImageEnhance.Contrast(im).enhance(1.25).save(T / "camp_base.jpg", quality=95)
from_image(T / "camp_base.jpg", "thumbnail_B", "THEY WATCHED", "ONE FILM...", "CAMP BUTNER · 1945", [(760, 470), (860, 420), (950, 370)], text_x=40, size=118)

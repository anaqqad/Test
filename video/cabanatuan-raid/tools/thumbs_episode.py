"""Thumbnail for this episode (Sealed Orders' layout in our colours, real Signal Corps photo):
python tools/thumbs_episode.py -> thumbnail/thumbnail_A.jpg"""
from pathlib import Path
P = Path(__file__).resolve().parent / "thumbnail.py"
src = P.read_text(encoding="utf-8"); src = src[:src.index('if __name__ == "__main__":')]
g = {"__file__": str(P)}; exec(src, g)
ROOT = g["ROOT"]
g["true_story"](ROOT / "assets/stills/sc201655_abbott.jpg", "thumbnail_A", "CABANATUAN", "1945", "511 FREED IN ONE NIGHT",
                cx=0.3, focus=(0.62, 0.42), zoom=1.15, kw_w=700)

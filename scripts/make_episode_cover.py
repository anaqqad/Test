#!/usr/bin/env python3
"""Episode cover (3000x3000) in the show style: full-bleed sepia portrait, show badge top-left,
white serif title at the bottom, gold Cinzel subtitle. Public-domain / CC0 photos only.

Usage:
    python3 scripts/make_episode_cover.py PHOTO CX CY SIDE OUT.jpg "Line one|Line two" "Subtitle"
(CX, CY = crop centre as 0..1 of the photo; SIDE = crop side as a fraction of the photo width.)
"""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps
import numpy as np
S=3000
src,cx,cy,side,out,title,sub=sys.argv[1],float(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4]),sys.argv[5],sys.argv[6],sys.argv[7]
im=Image.open(src).convert('RGB'); w,h=im.size; sd=side*w
box=(int(cx*w-sd/2),int(cy*h-sd/2),int(cx*w+sd/2),int(cy*h+sd/2))
im=im.crop(box).resize((S,S),Image.LANCZOS).filter(ImageFilter.UnsharpMask(4,80,2))
im=ImageOps.grayscale(im).convert('RGB')
im=ImageEnhance.Contrast(im).enhance(1.15)
a=np.asarray(im).astype(float)/255
# warm sepia tint + vignette + dark bottom for the title
tint=np.array([1.0,0.93,0.82]); a=a*tint
y,x=np.mgrid[0:S,0:S]/S
vig=1-0.55*np.clip(((x-0.5)**2+(y-0.42)**2)*2.2,0,1)
bot=1-0.9*np.clip((y-0.5)/0.42,0,1)**1.3
a=a*vig[...,None]*bot[...,None]
img=Image.fromarray((np.clip(a,0,1)*255).astype('uint8'))
d=ImageDraw.Draw(img)
# badge: the show cover in a circle, top-left
logo=Image.open('publish/podcast/cover-3000.jpg').convert('RGB').resize((520,520),Image.LANCZOS)
m=Image.new('L',(520,520),0); ImageDraw.Draw(m).ellipse((0,0,519,519),fill=255)
d.ellipse((110,110,650,650),fill=(245,236,215)); img.paste(logo,(120,120),m)
d=ImageDraw.Draw(img)
def fit(text,font,maxw,size):
    while ImageFont.truetype(font,size).getlength(text)>maxw: size-=4
    return ImageFont.truetype(font,size)
TF='/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'
lines=title.split('|'); y0=S-160
sf=fit(sub,'blender/assets/Cinzel.ttf',S-400,150)
sh=sf.getbbox(sub)[3]; y0-=sh
d.text((S/2,y0),sub,font=sf,fill=(232,190,90),anchor='ma',stroke_width=4,stroke_fill=(0,0,0))
y0-=60
for ln in reversed(lines):
    f=fit(ln,TF,S-300,430); hh=f.getbbox(ln)[3]
    y0-=hh
    d.text((S/2,y0),ln,font=f,fill=(255,255,255),anchor='ma',stroke_width=10,stroke_fill=(0,0,0))
    y0-=50
img.save(out,quality=92)
img.resize((600,600),Image.LANCZOS).save(out.replace('.jpg','-small.jpg'),quality=88)

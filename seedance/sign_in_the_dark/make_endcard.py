import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
cover, font, e1, e2, out = sys.argv[1:6]
W,H=1440,2560
bg=Image.open(cover).convert("RGB")
# blurred, darkened cover as background
b=bg.resize((W, int(bg.height*W/bg.width))).crop((0,0,W,H)) if bg.height*W/bg.width>=H else bg.resize((int(bg.width*H/bg.height),H))
b=b.crop(((b.width-W)//2,0,(b.width-W)//2+W,H)).filter(ImageFilter.GaussianBlur(40))
b=Image.blend(b, Image.new("RGB",(W,H),(10,6,24)), 0.55)
# sharp cover in the middle with a soft shadow
cw=980; ch=int(bg.height*cw/bg.width)
c=bg.resize((cw,ch))
x=(W-cw)//2; y=360
sh=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(sh)
d.rectangle((x+18,y+28,x+cw+18,y+ch+28),fill=(0,0,0,200)); sh=sh.filter(ImageFilter.GaussianBlur(30))
b=b.convert("RGBA"); b.alpha_composite(sh); b.paste(c,(x,y))
d=ImageDraw.Draw(b)
gold=(236,196,110); white=(255,255,255)
def line(text, size, yy, color, emoji=None):
    f=ImageFont.truetype(font,size)
    tw=d.textlength(text,font=f); es=int(size*1.15) if emoji else 0
    total=tw+(es+24 if emoji else 0); x0=(W-total)/2
    for dx,dy in [(4,4),(0,4),(4,0)]: d.text((x0+dx,yy+dy),text,font=f,fill=(0,0,0))
    d.text((x0,yy),text,font=f,fill=color)
    if emoji:
        em=Image.open(emoji).convert("RGBA").resize((es,es)); b.alpha_composite(em,(int(x0+tw+24),int(yy+size*0.05)))
top=y+ch+110
line("MY BOOKS ARE AVAILABLE", 78, top, white)
line("ON AMAZON KINDLE", 92, top+110, gold, e1)
line("LINK IN COMMENTS", 84, top+290, white, e2)
b.convert("RGB").save(out)
print("saved", out)

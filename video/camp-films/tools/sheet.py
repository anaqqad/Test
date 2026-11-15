"""Contact sheet of a film: N frames evenly spaced (or a time range), each labelled with its timestamp."""
import subprocess, sys, io
from PIL import Image, ImageDraw
src, out = sys.argv[1], sys.argv[2]
n = int(sys.argv[3]) if len(sys.argv) > 3 else 30
t0 = float(sys.argv[4]) if len(sys.argv) > 4 else 0
dur = float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",src]).decode())
t1 = float(sys.argv[5]) if len(sys.argv) > 5 else dur
W, H, C = 320, 180, 6
sheet = Image.new("RGB", (W*C, H*((n+C-1)//C)))
for i in range(n):
    t = t0 + (t1-t0)*(i+0.5)/n
    png = subprocess.run(["ffmpeg","-v","error","-ss",f"{t:.2f}","-i",src,"-frames:v","1","-vf",f"scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2","-f","image2pipe","-c:v","png","-"],capture_output=True).stdout
    if not png: continue
    im = Image.open(io.BytesIO(png)); d = ImageDraw.Draw(im)
    d.rectangle([0,0,62,16],fill=(0,0,0)); d.text((3,2),f"{int(t//60)}:{t%60:04.1f}",fill=(255,255,0))
    sheet.paste(im, ((i%C)*W, (i//C)*H))
sheet.save(out)

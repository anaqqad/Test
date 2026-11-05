"""QC contact sheets of the final video: python tools/qc_sheet.py [step seconds] -> build/qc_final_N.jpg, frames labelled with their time."""
import io, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
src = ROOT / "out" / f"{ROOT.name}.mp4"
step = float(sys.argv[1]) if len(sys.argv) > 1 else 4.0
dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(src)]))
W, H, C = 256, 144, 8
ts = [t * step + 1 for t in range(int(dur // step))]
for part in range(0, len(ts), 64):
    chunk = ts[part:part + 64]
    sheet = Image.new("RGB", (W * C, H * ((len(chunk) + C - 1) // C)))
    for i, t in enumerate(chunk):
        b = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", str(src), "-frames:v", "1", "-vf", f"scale={W}:{H}", "-f", "image2pipe", "-c:v", "png", "-"], capture_output=True).stdout
        im = Image.open(io.BytesIO(b)).convert("RGB")
        d = ImageDraw.Draw(im); d.rectangle((0, 0, 44, 12), fill=(0, 0, 0)); d.text((2, 1), f"{int(t // 60)}:{int(t % 60):02d}", fill=(255, 255, 0))
        sheet.paste(im, ((i % C) * W, (i // C) * H))
    sheet.save(ROOT / f"build/qc_final_{part // 64}.jpg", quality=88)
    print("sheet", part // 64)

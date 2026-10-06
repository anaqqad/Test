# Regenerate only the last shot of "The Car" with LTX-Video on a local GPU (free, no API).
# pip install -U diffusers transformers accelerate sentencepiece imageio imageio-ffmpeg
# python ltx_ending.py   -> ltx_ending.mp4 (silent, ~3 s); then run splice.sh
import torch
from diffusers import LTXImageToVideoPipeline
from diffusers.utils import export_to_video, load_image

PROMPT = (
    "Night, heavy rain, orange streetlight glow, cinematic photoreal. A woman in a long camel raincoat with "
    "auburn hair, her back to the camera, keeps hugging a Black woman in a hairnet and a grey cardigan over a "
    "light-blue uniform. A small 8-year-old Black boy, only waist-high to the women, wrapped in a grey blanket, "
    "runs in from the open car door on the left and wraps his arms around both women's waists. The mother "
    "pulls him in, crying with relief. Slow gentle camera push-in, raindrops glowing, wet reflections."
)
NEGATIVE = (
    "worst quality, blurry, deformed hands, morphing faces, adult-sized child, tall boy, extra people, "
    "text, subtitles, watermark, logo, jitter, flicker"
)

pipe = LTXImageToVideoPipeline.from_pretrained("Lightricks/LTX-Video", torch_dtype=torch.bfloat16).to("cuda")
image = load_image("start_frame.png").resize((480, 864))  # LTX needs sizes divisible by 32
frames = pipe(
    image=image, prompt=PROMPT, negative_prompt=NEGATIVE,
    width=480, height=864, num_frames=73, num_inference_steps=50,
    generator=torch.Generator("cuda").manual_seed(7),
).frames[0]
export_to_video(frames, "ltx_ending.mp4", fps=24)
print("wrote ltx_ending.mp4")

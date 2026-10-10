# Wan 2.2 video generation (local, free)

Open-weight image/text-to-video model, run in ComfyUI on the RTX 3090 Ti (24 GB). No API, no per-clip cost.

## Install (Windows, once)
    powershell -ExecutionPolicy Bypass -File video\install_wan22.ps1
Options: `-InstallDir D:\AI` (default `C:\AI`), `-WithT2V` (also text-to-video, +29 GB).
Needs the NVIDIA driver (`nvidia-smi` works) and ~45 GB free disk. Re-run to resume a broken download.

Downloads ComfyUI portable (~2 GB) and into `ComfyUI\models\`:
- `diffusion_models/wan2.2_i2v_{high,low}_noise_14B_fp8_scaled` (14.3 GB each)
- `text_encoders/umt5_xxl_fp8_e4m3fn_scaled` (6.7 GB), `vae/wan_2.1_vae` (0.25 GB)
- `loras/wan2.2_i2v_lightx2v_4steps_lora_v1_{high,low}_noise` (1.2 GB each, 4-step speed-up)

## Use
1. `C:\AI\ComfyUI_windows_portable\run_nvidia_gpu.bat`, open http://127.0.0.1:8188
2. Workflow -> Browse Templates -> Video -> "Wan 2.2 14B Image to Video".
3. Load a start image, write a motion prompt (what moves + camera move), Run. Output in `ComfyUI\output\`.
Start at 640x640 or 832x480, 81 frames (~5 s at 16 fps); go to 1280x720 once it works.

## Measured
- Not yet run on the 3090 Ti; note s/clip here.

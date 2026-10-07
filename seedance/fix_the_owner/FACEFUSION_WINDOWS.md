# Swap the man's face in "The Owner" with FaceFusion (free, local, RTX 3090 Ti)

Only the big man's face (and the painting of him) is changed. The girl and the manager are left alone,
and the original audio is kept.

## 1. Make the new face (one image)
Generate one front-facing, well-lit photo of a fictional man in any image tool, for example:

> Photoreal portrait of a fictional Black man in his 40s, front-facing, neutral expression, short
> grey-streaked locs tied back, thick black-rimmed glasses, full salt-and-pepper beard, small scar through
> the left eyebrow, soft studio light, plain background. Original person, not resembling any celebrity.

Check that it looks like nobody famous. Save it as `new_face.jpg` in this folder.
(Glasses may not carry over in a face swap; the face shape, beard and skin will.)

## 2. Install FaceFusion (once)
Needs Git, Miniconda and an up-to-date NVIDIA driver. In "Anaconda Prompt":

    cd %USERPROFILE%
    git clone https://github.com/facefusion/facefusion
    cd facefusion
    conda create -n facefusion python=3.12 -y
    conda activate facefusion
    conda install conda-forge::cuda-runtime=12.8 conda-forge::cudnn=9.8 -y
    conda install conda-forge::libcublas=12.8 conda-forge::libcufft=11 -y
    python install.py cuda@12

Tested with FaceFusion 3.9.1 (2026-10): the runtime is now a positional argument (`cuda@12` or `cuda@13`),
the old `--onnxruntime cuda` form is rejected. The pip step takes 10+ minutes. Check the GPU is seen with
`python -c "import onnxruntime as o; print(o.get_available_providers())"` (must list CUDAExecutionProvider).

If a step fails, follow https://docs.facefusion.io/installation (the exact versions change between releases).

## 3. Run it
Put `the_owner_no_pop.mp4` (the file I sent) and `new_face.jpg` in this folder, then double-click
`run_facefusion.bat`. The result is `the_owner_new_face.mp4`.

Before the first run, check the flag names for your version:

    python facefusion.py headless-run --help

## 4. Check the result
- Every shot of the man shows the new face, including the painting.
- The girl and the manager are unchanged. If one of them got swapped, lower `DISTANCE` in the .bat
  (e.g. 0.25). If some shots of the man were missed, raise it a little (e.g. 0.35). In 3.9.1 the distance is
  (1 - cosine similarity) / 2 with default 0.3; at 0.5 the manager was swapped too.
- The painting is too different from his live face (smaller, smiling) to match pass 1 even at 0.65, so the
  .bat runs a second pass that uses the painting face itself as the reference.
- Hooded shots where his face is in shadow may not swap; that's fine, the face is hidden there anyway.
- Test on a short clip first: `ffmpeg -ss 18 -to 26 -i the_owner_no_pop.mp4 -c:v libx264 -crf 14 -c:a copy test_18_26.mp4`,
  then `run_facefusion.bat test_18_26.mp4 test_out.mp4 108` (it covers the manager, the man and the painting).

License note: in 3.9.1 the default swap model is hyperswap_1a_256 (ResearchRAIL, no commercial use);
inswapper_128 and simswap are non-commercial too. For a page that earns money, set `SWAP_MODEL=ghost_2_256`
(Apache-2.0) in the .bat. The gfpgan_1.4 enhancer is Apache-2.0.

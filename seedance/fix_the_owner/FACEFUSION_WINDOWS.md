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
    python install.py --onnxruntime cuda

If a step fails, follow https://docs.facefusion.io/installation (the exact versions change between releases).

## 3. Run it
Put `the_owner_no_pop.mp4` (the file I sent) and `new_face.jpg` in this folder, then double-click
`run_facefusion.bat`. The result is `the_owner_new_face.mp4`.

Before the first run, check the flag names for your version:

    python facefusion.py headless-run --help

## 4. Check the result
- Every shot of the man shows the new face, including the painting.
- The girl and the manager are unchanged. If one of them got swapped, lower `--reference-face-distance`
  in the .bat (e.g. 0.4). If some shots of the man were missed, raise it (e.g. 0.6).
- Hooded shots where his face is in shadow may not swap; that's fine, the face is hidden there anyway.

License note: the default swap model (inswapper) is for non-commercial use. If the page earns money,
check FaceFusion's model licenses and pick one that allows it.

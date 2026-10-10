# Installs ComfyUI (Windows portable, NVIDIA) + Wan 2.2 14B image-to-video models.
# Run in PowerShell:
#   powershell -ExecutionPolicy Bypass -File video\install_wan22.ps1
#   powershell -ExecutionPolicy Bypass -File video\install_wan22.ps1 -InstallDir D:\AI -WithT2V
# Downloads resume if interrupted (just re-run). Needs ~45 GB free (+29 GB with -WithT2V).
param(
    [string]$InstallDir = "C:\AI",
    [switch]$WithT2V
)
$ErrorActionPreference = "Stop"

$hf22 = "https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged/resolve/main/split_files"
$hf21 = "https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files"
$comfyUrl = "https://github.com/comfyanonymous/ComfyUI/releases/latest/download/ComfyUI_windows_portable_nvidia.7z"

function Get-File($url, $dest) {
    if (Test-Path $dest) {
        $want = (Invoke-WebRequest -Uri $url -Method Head -MaximumRedirection 10 -UseBasicParsing).Headers["Content-Length"]
        if ($want -and (Get-Item $dest).Length -eq [int64]"$want") { Write-Host "ok    $(Split-Path $dest -Leaf)"; return }
    }
    New-Item -ItemType Directory -Force -Path (Split-Path $dest) | Out-Null
    Write-Host "get   $(Split-Path $dest -Leaf)"
    & curl.exe -L --fail --retry 5 -C - -o $dest $url
    if ($LASTEXITCODE -ne 0) { throw "download failed: $url" }
}

# 1. GPU check
if (-not (Get-Command nvidia-smi -ErrorAction SilentlyContinue)) { throw "nvidia-smi not found: install/update the NVIDIA driver first." }
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader

# 2. ComfyUI portable
New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null
$root = Join-Path $InstallDir "ComfyUI_windows_portable"
if (-not (Test-Path (Join-Path $root "run_nvidia_gpu.bat"))) {
    $archive = Join-Path $InstallDir "ComfyUI_windows_portable_nvidia.7z"
    Get-File $comfyUrl $archive
    $7z = @("$env:ProgramFiles\7-Zip\7z.exe", "${env:ProgramFiles(x86)}\7-Zip\7z.exe") | Where-Object { Test-Path $_ } | Select-Object -First 1
    if (-not $7z) {
        Write-Host "Installing 7-Zip via winget..."
        winget install --id 7zip.7zip -e --accept-package-agreements --accept-source-agreements
        $7z = "$env:ProgramFiles\7-Zip\7z.exe"
    }
    & $7z x $archive "-o$InstallDir" -y | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "extract failed" }
    Remove-Item $archive
}
$models = Join-Path $root "ComfyUI\models"

# 3. Wan 2.2 models (fp8, fit a 24 GB card)
$files = @(
    @("$hf22/diffusion_models/wan2.2_i2v_high_noise_14B_fp8_scaled.safetensors", "diffusion_models"),
    @("$hf22/diffusion_models/wan2.2_i2v_low_noise_14B_fp8_scaled.safetensors",  "diffusion_models"),
    @("$hf21/text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors",               "text_encoders"),
    @("$hf22/vae/wan_2.1_vae.safetensors",                                         "vae"),
    # 4-step speed LoRAs (optional in the workflow, ~4x faster)
    @("$hf22/loras/wan2.2_i2v_lightx2v_4steps_lora_v1_high_noise.safetensors",     "loras"),
    @("$hf22/loras/wan2.2_i2v_lightx2v_4steps_lora_v1_low_noise.safetensors",      "loras")
)
if ($WithT2V) {
    $files += ,@("$hf22/diffusion_models/wan2.2_t2v_high_noise_14B_fp8_scaled.safetensors", "diffusion_models")
    $files += ,@("$hf22/diffusion_models/wan2.2_t2v_low_noise_14B_fp8_scaled.safetensors",  "diffusion_models")
}
foreach ($f in $files) {
    Get-File $f[0] (Join-Path (Join-Path $models $f[1]) (Split-Path $f[0] -Leaf))
}

Write-Host ""
Write-Host "Done. Start ComfyUI with: $root\run_nvidia_gpu.bat"
Write-Host "Then open http://127.0.0.1:8188 -> Workflow -> Browse Templates -> Video -> 'Wan 2.2 14B Image to Video'."

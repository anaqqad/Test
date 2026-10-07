@echo off
rem Swap only the big man's face in the_owner_no_pop.mp4, in two passes. Flags checked against
rem FaceFusion 3.9.1 (headless-run --help). Original audio is copied back untouched at the end.
rem   pass 1: reference = largest face at frame 540 (22.5 s) = the man himself
rem   pass 2: reference = 2nd largest face at frame 540 = the framed photo of him on the wall
rem           (smaller, smiling and painted, so pass 1 does not match it)
rem Usage: run_facefusion.bat [input.mp4] [output.mp4] [reference frame] [reference face distance]
rem   defaults: the_owner_no_pop.mp4 -> the_owner_new_face.mp4, frame 540, distance 0.3
rem   test clip: run_facefusion.bat test_18_26.mp4 test_out.mp4 108   (22.5 s - 18 s = 4.5 s = frame 108)
rem
rem DISTANCE: in 3.9.1 this is (1 - cosine similarity) / 2. 0.3 is the default; at 0.5 the manager
rem           gets swapped too. Lower it if the wrong person is swapped, raise it if shots are missed.
rem SWAP_MODEL: hyperswap_1a_256 = 3.9.1 default, best quality, ResearchRAIL license (no commercial use).
rem             ghost_2_256 = Apache-2.0, commercially usable, a bit softer.
rem             inswapper_128 = the classic model, non-commercial only.
setlocal
rem Resolve relative input/output names against this folder.
cd /d "%~dp0"
set "SWAP_MODEL=hyperswap_1a_256"
set "DISTANCE=0.3"
set "IN=%~dp0the_owner_no_pop.mp4"
set "OUT=%~dp0the_owner_new_face.mp4"
set "REF_FRAME=540"
if not "%~1"=="" set "IN=%~f1"
if not "%~2"=="" set "OUT=%~f2"
if not "%~3"=="" set "REF_FRAME=%~3"
if not "%~4"=="" set "DISTANCE=%~4"
set "PASS1=%~dp0_swap_pass1.mp4"
set "PASS2=%~dp0_swap_pass2.mp4"

call conda activate facefusion
cd /d "%USERPROFILE%\facefusion"
call :swap "%IN%" "%PASS1%" 0 || goto :eof
call :swap "%PASS1%" "%PASS2%" 1 || goto :eof

rem Put the original audio back as a stream copy, so it is bit-identical to the input.
rem FaceFusion 3.9.1 returns one extra frame and a black last frame. Keep the first N-1 swapped
rem frames and repeat the last good one, so the video has exactly the input's N frames (30.08 s).
for /f %%n in ('ffprobe -v error -select_streams v:0 -show_entries stream^=nb_frames -of csv^=p^=0 "%IN%"') do set "FRAMES=%%n"
set /a KEEP=FRAMES-1
ffmpeg -y -v error -i "%PASS2%" -i "%IN%" -filter_complex "[0:v]trim=end_frame=%KEEP%,tpad=stop=1:stop_mode=clone[v]" ^
  -map "[v]" -map 1:a:0 -c:v libx264 -crf 16 -preset slow -pix_fmt yuv420p -c:a copy "%OUT%"
del "%PASS1%" "%PASS2%"
echo Done: %OUT%
endlocal
goto :eof

:swap
python facefusion.py headless-run ^
  --source-paths "%~dp0new_face.jpg" ^
  --target-path "%~1" ^
  --output-path "%~2" ^
  --processors face_swapper face_enhancer ^
  --face-swapper-model %SWAP_MODEL% ^
  --face-enhancer-model gfpgan_1.4 ^
  --face-enhancer-blend 60 ^
  --face-selector-mode reference ^
  --face-selector-order large-small ^
  --reference-face-position %3 ^
  --reference-frame-number %REF_FRAME% ^
  --reference-face-distance %DISTANCE% ^
  --execution-providers cuda ^
  --output-video-quality 90
exit /b %errorlevel%

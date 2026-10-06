@echo off
rem Swap only the big man's face in the_owner_no_pop.mp4. Reference = his face at frame 540 (22.5 s),
rem where he is the largest face on screen. Audio is kept.
call conda activate facefusion
cd /d "%USERPROFILE%\facefusion"
python facefusion.py headless-run ^
  --source-paths "%~dp0new_face.jpg" ^
  --target-path "%~dp0the_owner_no_pop.mp4" ^
  --output-path "%~dp0the_owner_new_face.mp4" ^
  --processors face_swapper face_enhancer ^
  --face-selector-mode reference ^
  --face-selector-order large-small ^
  --reference-face-position 0 ^
  --reference-frame-number 540 ^
  --reference-face-distance 0.5 ^
  --execution-providers cuda ^
  --output-video-quality 90
pause

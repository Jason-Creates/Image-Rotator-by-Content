# Image Auto Orientator

Epson FastFoto

Photos from the scanner were scanned into jpg files at 0, 90, 270 rotations.



## Workflow

1. Scan photos

2. Run AutoOrent script

3. Scan for corrupt files with BadPeggy, and rerun above script if needed.

4. Scan & Remove duplicate photos using DupeGuru.



## How it works

This script uses the enhanced photo (filename with `_a.jpg`) use for rotation correction. Once the correct rotation is determined, it will apply the same rotation to the orginial jpg file (without `_a` ) and it will apply the predicted rotation + 180 to the back photo if it exists (filename with `_b.jpg`).

Correctly rotated images will be created with `-rot` appended to the filename (e.g. `Bin4_a-rot.jpg`, `Bin4-rot.jpg`, `Bin4_b-rot`). Orignial, enhanced, and back will not be overwritten, so make sure you have enough harddrive space to accomidate the extra files.



The script uses the Machine Learning Model here

[amaye15/Beit-Base-Image-Orientation-Fixer · Hugging Face](https://huggingface.co/amaye15/Beit-Base-Image-Orientation-Fixer)





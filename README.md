# Image Auto Orientator

Epson FastFoto

Photos from the scanner were scanned into jpg files at 0, 90, 180, 270 rotations.

## Workflow

1. Scan photos using Epson FastFoto or whatever

2. Run AutoOrent script

3. Scan for corrupt files with BadPeggy, and rerun above script if needed.

4. Scan & Remove duplicate photos using DupeGuru.

## Requirements

* [jpegtran](https://jpegclub.org/jpegtran/) installed

* Scanned photos with the following naming scheme:
  
  > This is the default naming scheme for EPSON FastFoto
  
  | Filename    | Purpose                |
  | ----------- | ---------------------- |
  | *.jpg       | Orginal Photo          |
  | *_a.jpg     | Enhanced Photo         |
  | *_b.jpg     | Back of Photo          |
  | *-rot.jpg   | Orginal Photo Rotated  |
  | *_a-rot.jpg | Enhanced Photo Rotated |
  | *_b-rot.jpg | Back of Photo Rotated  |

* All Original, Enhanced, and Back photo files have rotations that match that set (e.g. the Enhanced photo is rotated 90 deg from orginal photo is *not* allowed). 

* Install the following Python modules...

```shell
pip install transformers
pip install tqdm
pip install pillow
```

## How it Works

This script uses the enhanced photo (filename with `_a.jpg`) use for rotation correction. Once the correct rotation is determined, it will apply the same rotation to the orginial jpg file (without `_a` ) and it will apply the predicted rotation + 180 to the back photo if it exists (filename with `_b.jpg`).

Correctly rotated images will be created with `-rot` appended to the filename (e.g. `Bin4_a-rot.jpg`, `Bin4-rot.jpg`, `Bin4_b-rot`). Orignial, enhanced, and back will not be overwritten, so make sure you have enough harddrive space to accommodate the extra files.

The script uses the Machine Learning Model here:

[amaye15/Beit-Base-Image-Orientation-Fixer · Hugging Face](https://huggingface.co/amaye15/Beit-Base-Image-Orientation-Fixer)



Change `input_folder` variable to the path where your photos are located and run the script.

```shell
python AutoPhotoOrient.py
```



# -*- coding: utf-8 -*-
"""

Losslessly Rotate JPG photos based on picture content.

Model from:
https://huggingface.co/amaye15/Beit-Base-Image-Orientation-Fixer

This script assumes:
   > Filenaming uses the below pattern:
        *.jpg       > Orginal Photo
        *_a.jpg     > Enhanced Photo
        *_b.jpg     > Back of Photo
        *-rot.jpg   > Orginal Photo Rotated
        *_a-rot.jpg > Enhanced Photo Rotated
        *_b-rot.jpg > Back of Photo Rotated
   > Original, Enhanced, and Back photo files have rotations that match. 
   > jpegtran is installed and callable from current path otherwise specify its location below. 
"""

from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
import os
import subprocess
import tqdm
from pathlib import Path

input_folder = r"C:\Pictures\FastFoto"


def getBackImageRotation(frontRotAngle):
    return (frontRotAngle + 180) % 360

def lossless_rotate_jpeg_jpegtran(image_path, rotation_degrees):
    """Losslessly rotates a JPEG using jpegtran (truly lossless)."""

    try:
        if rotation_degrees not in [0, 90, 180, 270]:
            raise ValueError("Rotation must be 0, 90, 180, or 270.")

        base_name, ext = os.path.splitext(image_path)
        new_image_path = f"{base_name}-rot{ext}"

        # Construct the jpegtran command
        command = [
            r"jpegtran",  # Path to jpegtran (adjust if needed)
            "-copy", "all", # Copy all metadata
            "-rotate", str(rotation_degrees),
            image_path,
            new_image_path
        ]

        subprocess.run(command, check=True)
        #print(f"Image rotated (losslessly) and saved as {new_image_path}")

    except FileNotFoundError:
        print("Error: jpegtran not found. Make sure it's installed and in your PATH.")
    except ValueError as e:
        print(f"Error: {e}")
    except subprocess.CalledProcessError as e:
        print(f"Error rotating image: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


def process_image(filepath):
    image = Image.open(filepath)
    
    inputs = processor(images=image, return_tensors="pt")
    outputs = model(**inputs)
    logits = outputs.logits

    predicted_class_idx = logits.argmax(-1).item()
    predicted_angle = int(model.config.id2label[predicted_class_idx])
    #print("Predicted angle:", predicted_angle)
    
    input_path = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    base, ext = os.path.splitext(filename)
    org_filepath = os.path.join(input_path, f'{base[:-2]}{ext}')
    back_filepath = os.path.join(input_path, f'{base[:-2]}_b{ext}')
    
    if predicted_angle != 0:
        # Rotate Enhanced Photo
        lossless_rotate_jpeg_jpegtran(filepath, predicted_angle)
        
        # Rotate Orginal Photo if exists
        if os.path.isfile(org_filepath):
            lossless_rotate_jpeg_jpegtran(org_filepath, predicted_angle)

        # Rotate Back Photo if exists
        if os.path.isfile(back_filepath):
            bk_rotation = getBackImageRotation(predicted_angle)
            if bk_rotation != 0:
                lossless_rotate_jpeg_jpegtran(back_filepath, bk_rotation)
    image.close()

if __name__ == "__main__":
    processor = AutoImageProcessor.from_pretrained("amaye15/Beit-Base-Image-Orientation-Fixer")
    model = AutoModelForImageClassification.from_pretrained("amaye15/Beit-Base-Image-Orientation-Fixer")
    
    
    # Search thru only Enhanced Photos (recursive)
    input_folder = Path(input_folder)
    image_files = list(input_folder.rglob("*_a.jpg"))
    
    for image_path in tqdm.tqdm(image_files, desc="Processing Images"):
        filename = os.path.basename(image_path)
        base, ext = os.path.splitext(filename)
        in_dir = os.path.dirname(image_path)
        
        rotFilepath = os.path.join(in_dir, base) + f'-rot{ext}'
    
        # Don't process file if "*-rot.jpg" already exists.
        if not os.path.isfile(rotFilepath):
            process_image(image_path)
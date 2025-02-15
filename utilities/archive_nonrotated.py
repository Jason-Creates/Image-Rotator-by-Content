# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 20:39:34 2025

@author: Jason

Move non-rotated images out of the 
folder if rotated image file exists.
"""

import os
import shutil

def move_rotated_images(source_folder, destination_folder):
    """
    Recursively searches a folder for .jpg files and their corresponding -rot.jpg files.
    If both exist, moves the .jpg file to the destination folder, maintaining the 
    original folder structure relative to the source folder.

    Args:
        source_folder: The path to the folder to search.
        destination_folder: The path to the folder to move the .jpg files to.
    """

    for root, _, files in os.walk(source_folder):
        for file in files:
            if file.endswith(".jpg") and not file.endswith("-rot.jpg"):  # Check for .jpg, but not -rot.jpg
                base_name = file[:-4]  # Extract filename without .jpg
                rot_file = base_name + "-rot.jpg"
                rot_file_path = os.path.join(root, rot_file)

                if os.path.exists(rot_file_path):
                    source_image_path = os.path.join(root, file)

                    # Create corresponding directory structure in destination
                    relative_path = os.path.relpath(root, source_folder)  # Get path relative to source
                    destination_path = os.path.join(destination_folder, relative_path)
                    os.makedirs(destination_path, exist_ok=True) # Create if it doesn't exist.

                    destination_image_path = os.path.join(destination_path, file)
                    shutil.move(source_image_path, destination_image_path)
                    print(f"Moved {file} to {destination_image_path}")


source_folder = r"C:\Users\jason\Pictures\FastFoto"
destination_folder = r"C:\Users\jason\Pictures\FastFoto NonRotated"

move_rotated_images(source_folder, destination_folder)

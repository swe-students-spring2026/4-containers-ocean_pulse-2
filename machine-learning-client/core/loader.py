"""
Image loading utility module.

This module provides functionality to load image files from a folder
and return them as (filename, image) pairs using OpenCV.
"""

# pylint: disable=no-member

import os
import cv2


def load_images(folder):
    """
    Load images from a specified folder.

    Args:
        folder (str): Path to the directory containing images.

    Returns:
        list: A list of tuples (filename, image), where image is a cv2 image object.
    """
    images = []

    for file in os.listdir(folder):
        if file.lower().endswith((".jpg", ".png", ".jpeg")):
            path = os.path.join(folder, file)
            img = cv2.imread(path)

            if img is None:
                print(f"[SKIP] cannot read image: {path}")
                continue

            images.append((file, img))

    return images

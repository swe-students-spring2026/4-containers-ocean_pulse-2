"""
Main pipeline for processing images and predicting focus scores.

- Loads images from a shared directory (/shared/img)
- Runs an AI model on each image
- Stores results (including images) to MongoDB
"""

import sys
import os
import time
import shutil

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "db-upload"))

from loader import load_images  # pylint: disable=wrong-import-position
from model import predict_focus  # pylint: disable=wrong-import-position
from writer import write_json  # pylint: disable=wrong-import-position
from upload import upload_results  # pylint: disable=wrong-import-position,import-error

IMG_DIR = "/shared/img"


def main():
    """
    Main function.
    """
    processed = set()

    clear_dir(IMG_DIR)

    while True:
        images = load_images(IMG_DIR)

        new_images = [(p, img) for p, img in images if p not in processed]

        results = []
        db_entries = []

        for img_path, img in new_images:
            score = predict_focus(img)
            focused = score > 0.5

            processed.add(img_path)

            results.append(
                {"image": img_path, "focused": focused, "confidence": float(score)}
            )

            db_entries.append(
                {
                    "image_name": img_path,
                    "image": img,
                    "focused": focused,
                    "confidence": float(score),
                }
            )

            try:
                file_path = os.path.join(IMG_DIR, img_path)

                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"[CLEAN] deleted {img_path}")

            except Exception as e:
                print(f"[WARN] failed to delete {img_path}: {e}")

        if db_entries:
            print("Uploading ... \n")
            upload_results(db_entries)
            print(f"[OK] uploaded {len(db_entries)} result(s) to MongoDB")
        else:
            print("[WARN] no images found to process")

        time.sleep(10)


def clear_dir(path):
    """Simple function that clears up a given directory."""
    for name in os.listdir(path):
        file_path = os.path.join(path, name)

        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)


if __name__ == "__main__":
    main()

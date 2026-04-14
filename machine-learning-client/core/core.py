"""
Main pipeline for processing images and predicting focus scores.

- Loads images from a shared directory (/shared/img)
- Runs an AI model on each image
- Stores results (including images) to MongoDB
- Also writes a local JSON backup to /app/output
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "db-upload"))

from loader import load_images  # pylint: disable=wrong-import-position
from model import predict_focus  # pylint: disable=wrong-import-position
from writer import write_json  # pylint: disable=wrong-import-position
from upload import upload_results  # pylint: disable=wrong-import-position,import-error

IMG_DIR = "/shared/img"
OUT_FILE = "/app/output/result.json"


def main():
    """
    Main function.
    """
    images = load_images(IMG_DIR)

    results = []
    db_entries = []

    for img_path, img in images:
        score = predict_focus(img)
        focused = score > 0.5

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

    write_json(OUT_FILE, results)

    print("Uploading ... \n")

    if db_entries:
        upload_results(db_entries)
        print(f"[OK] uploaded {len(db_entries)} result(s) to MongoDB")
    else:
        print("[WARN] no images found to process")


if __name__ == "__main__":
    main()

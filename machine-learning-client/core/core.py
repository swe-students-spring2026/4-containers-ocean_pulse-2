"""
Main pipeline for processing images and predicting focus scores.

- Loads images from a shared directory (/shared/img)
- Runs an AI model on each image
- Outputs results as JSON files (stored in /app/output)
"""

from loader import load_images
from model import predict_focus
from writer import write_json

IMG_DIR = "/shared/img"
OUT_FILE = "/app/output/result.json"


def main():
    """
    Main function.
    """
    images = load_images(IMG_DIR)

    results = []

    for img_path, img in images:
        score = predict_focus(img)

        results.append(
            {"image": img_path, "focused": score > 0.5, "confidence": float(score)}
        )

    write_json(OUT_FILE, results)


if __name__ == "__main__":
    main()

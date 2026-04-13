"""
Utility module for writing model results to JSON files.
"""

import json
import os


def write_json(path, results):
    """
    Write prediction results to a JSON file.

    Args:
        path (str): Output file path.
        results (list): List of prediction results.

    Returns:
        None
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)

    data = {"results": results}

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

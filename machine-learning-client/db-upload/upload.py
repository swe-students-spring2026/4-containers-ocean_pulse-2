"""
MongoDB upload module for storing image analysis results.

Stores each processed image (as base64) along with its
focus analysis metadata into a MongoDB collection.
"""

import os
import base64
from datetime import datetime, timezone

import cv2
from pymongo import MongoClient

# pylint: disable=no-member

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://mongodb:27017")
DB_NAME = os.environ.get("MONGO_DB", "ocean_pulse")
COLLECTION = "results"

mongo_client = MongoClient(MONGO_URI)


def get_collection():
    """Return the MongoDB collection handle."""
    return mongo_client[DB_NAME][COLLECTION]


def encode_image(img):
    """Encode an OpenCV image to a base64 JPEG string."""
    _, buf = cv2.imencode(".jpg", img)
    return base64.b64encode(buf).decode("utf-8")


def upload_result(img_name, img, focused, confidence):
    """
    Upload a single image analysis result to MongoDB.

    Args:
        img_name (str): Original filename of the image.
        img (numpy.ndarray): The OpenCV image array.
        focused (bool): Whether the person is focused.
        confidence (float): Focus confidence score (0-1).
    """
    collection = get_collection()
    doc = {
        "image_name": img_name,
        "image_data": encode_image(img),
        "focused": focused,
        "confidence": confidence,
        "timestamp": datetime.now(timezone.utc),
    }
    collection.insert_one(doc)


def upload_results(results_list):
    """
    Upload multiple image analysis results to MongoDB.

    Args:
        results_list (list): List of dicts with keys:
            image_name, image, focused, confidence.
    """
    collection = get_collection()
    docs = []
    for item in results_list:
        docs.append(
            {
                "image_name": item["image_name"],
                "image_data": encode_image(item["image"]),
                "focused": item["focused"],
                "confidence": item["confidence"],
                "timestamp": datetime.now(timezone.utc),
            }
        )
    if docs:
        collection.insert_many(docs)

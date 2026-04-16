"""
Ocean Pulse web application.

Serves a dashboard showing attention-tracking results
stored in MongoDB by the machine learning client.
"""

import os
import base64
from io import BytesIO
from datetime import datetime
from zoneinfo import ZoneInfo

from flask import Flask, render_template, send_file, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://mongodb:27017")
DB_NAME = os.environ.get("MONGO_DB", "ocean_pulse")

mongo_client = MongoClient(MONGO_URI)

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

if os.path.exists("/shared/img"):
    SHARED_IMGS = "/shared/img"
else:
    SHARED_IMGS = os.path.join(PROJECT_ROOT, "img")

os.makedirs(SHARED_IMGS, exist_ok=True)


def get_collection():
    """Return the MongoDB results collection."""
    return mongo_client[DB_NAME]["results"]


@app.route("/")
def home():
    """Render the dashboard with results from MongoDB."""

    collection = get_collection()
    records = list(collection.find().sort("timestamp", -1))

    attention_counter = sum(1 for r in records if not r.get("focused", True))

    return render_template(
        "index.html",
        attention_counter=attention_counter,
        records=records,
    )


@app.route("/images/<record_id>")
def get_image(record_id):
    """Serve an image stored in MongoDB by its document _id."""
    try:
        oid = ObjectId(record_id)
    except Exception:  # pylint: disable=broad-except
        return "Image not found", 404

    collection = get_collection()
    doc = collection.find_one({"_id": oid})

    if not doc or "image_data" not in doc:
        return "Image not found", 404

    img_bytes = base64.b64decode(doc["image_data"])
    return send_file(BytesIO(img_bytes), mimetype="image/jpeg")


@app.route("/upload-image", methods=["POST"])
def upload_image():
    """Receive one captured browser image and save it to the shared image folder"""
    data = request.get_json(silent=True)

    if not data or "image" not in data:
        return jsonify({"error": "No image received"}), 400

    image_data = data["image"]

    try:
        if "," in image_data:
            image_data = image_data.split(",", 1)[1]

        image_bytes = base64.b64decode(image_data)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"img_{timestamp}.jpg"
        filepath = os.path.join(SHARED_IMGS, filename)

        with open(filepath, "wb") as f:
            f.write(image_bytes)

        return jsonify({"message": "Image saved successfully", "filename": filename})
    except Exception as e:  # pylint: disable=broad-exception-caught
        return jsonify({"error": str(e)}), 500


@app.route("/api/status")
def status():
    collection = get_collection()
    records = list(collection.find().sort("timestamp", -1))

    attention_counter = sum(1 for r in records if not r.get("focused"))

    def format_ts(ts):
        if ts:
            ts = ts.replace(tzinfo=ZoneInfo("UTC")).astimezone(
                ZoneInfo("America/New_York")
            )
            return ts.strftime("%Y-%m-%d %H:%M:%S")
        return "N/A"

    return jsonify(
        {
            "attention_counter": attention_counter,
            "records": [
                {
                    "_id": str(r["_id"]),
                    "focused": r.get("focused", False),
                    "confidence": r.get("confidence", 0),
                    "timestamp": format_ts(r.get("timestamp")),
                }
                for r in records
                if not r.get("focused")
            ],
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

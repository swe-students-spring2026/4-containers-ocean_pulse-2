import os
import base64
from io import BytesIO

from flask import Flask, render_template, send_file
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://mongodb:27017")
DB_NAME = os.environ.get("MONGO_DB", "ocean_pulse")

mongo_client = MongoClient(MONGO_URI)


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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

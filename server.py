from flask import Flask, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)
latest_location = None
API_KEY = os.getenv("API_KEY", "changeme123")

def check_key():
    key = request.headers.get("X-API-Key") or request.args.get("api_key")
    return key == API_KEY

@app.route("/location", methods=["POST"])
def receive_location():
    global latest_location
    if not check_key():
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json()
    if not data or "latitude" not in data or "longitude" not in data:
        return jsonify({"error": "Invalid payload"}), 400
    latest_location = {
        "latitude": data["latitude"],
        "longitude": data["longitude"],
        "accuracy_meters": data.get("accuracy_meters", 0),
        "received_at": datetime.now().isoformat()
    }
    return jsonify({"status": "ok"})

@app.route("/get_location", methods=["GET"])
def get_location():
    if not check_key():
        return jsonify({"error": "Unauthorized"}), 401
    if latest_location is None:
        return jsonify({"error": "No location yet"}), 404
    return jsonify(latest_location)

@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "running", "has_location": latest_location is not None})

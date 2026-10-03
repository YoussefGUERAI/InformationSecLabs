from pathlib import Path

from flask import Flask, request

STATIC_DIR = Path(__file__).resolve().parent / "static"
app = Flask(__name__, static_folder=str(STATIC_DIR))

ALLOWED_ORIGINS = {
    "http://publisher-one.test:8001",
    "http://publisher-two.test:8002",
}

REQUIRED_EVENT_FIELDS = {
    "analytics_id",
    "publisher",
    "page",
    "page_title",
    "timestamp",
}


@app.after_request
def add_cors_headers(response):
    origin = request.headers.get("Origin")

    if origin in ALLOWED_ORIGINS:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        response.vary.add("Origin")

    return response


@app.route("/collect", methods=["POST", "OPTIONS"])
def collect_event():
    origin = request.headers.get("Origin")

    if origin not in ALLOWED_ORIGINS:
        return {"error": "Origin is not allowed"}, 403

    if request.method == "OPTIONS":
        return "", 204

    event = request.get_json(silent=True)
    if not isinstance(event, dict):
        return {"error": "A JSON event is required"}, 400

    missing_fields = sorted(REQUIRED_EVENT_FIELDS.difference(event))
    if missing_fields:
        return {"error": "Missing required fields", "fields": missing_fields}, 400

    return "", 204


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9100, debug=True)

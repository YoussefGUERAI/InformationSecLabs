from flask import Flask, render_template, request


app = Flask(__name__)


@app.route("/")
def home():
    print("\n========== NEW VISIT ==========")
    print("IP address      :", request.remote_addr)
    print("HTTP method     :", request.method)
    print("User-Agent      :", request.headers.get("User-Agent"))
    print("Accept-Language :", request.headers.get("Accept-Language"))

    # Preferred response formats and compression algorithms.
    print("Accept          :", request.headers.get("Accept"))
    print("Accept-Encoding :", request.headers.get("Accept-Encoding"))

    # Navigation context. Referer may be absent for direct navigation.
    print("Referer         :", request.headers.get("Referer"))
    print("Sec-Fetch-Site  :", request.headers.get("Sec-Fetch-Site"))
    print("Sec-Fetch-Mode  :", request.headers.get("Sec-Fetch-Mode"))
    print("Sec-Fetch-Dest  :", request.headers.get("Sec-Fetch-Dest"))

    # Browser, operating-system, and device hints (mainly Chromium).
    print("Sec-CH-UA       :", request.headers.get("Sec-CH-UA"))
    print("CH-UA-Platform  :", request.headers.get("Sec-CH-UA-Platform"))
    print("CH-UA-Mobile    :", request.headers.get("Sec-CH-UA-Mobile"))

    # Security-related navigation preference.
    print("Upgrade HTTPS   :", request.headers.get("Upgrade-Insecure-Requests"))
    print("================================\n")

    return render_template("index.html")


@app.post("/collect")
def collect_features():
    payload = request.get_json(silent=True)

    if not isinstance(payload, dict):
        return {"status": "error", "message": "Expected a JSON object."}, 400

    collection_type = payload.get("collectionType")

    if collection_type == "fingerprint":
        fingerprint = payload.get("fingerprint")

        if (
            not isinstance(fingerprint, str)
            or len(fingerprint) != 64
            or any(character not in "0123456789abcdef" for character in fingerprint)
        ):
            return {
                "status": "error",
                "message": "Expected a lowercase SHA-256 fingerprint.",
            }, 400

        print("\n======= FINGERPRINT IDENTIFIER =======")
        print("SHA-256           :", fingerprint)
        print("======================================\n")

        return {"status": "ok"}

    features = payload.get("features")

    if collection_type != "behavioral" or not isinstance(features, dict):
        return {
            "status": "error",
            "message": "Expected fingerprint data or behavioral features.",
        }, 400

    heading = f"{collection_type.upper()} FEATURES"
    print(f"\n======= {heading} =======")
    for name, value in features.items():
        print(f"{name:<18}: {value}")
    print("================================\n")

    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)

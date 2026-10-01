from pathlib import Path

from flask import Flask

STATIC_DIR = Path(__file__).resolve().parent / "static"
app = Flask(__name__, static_folder=str(STATIC_DIR))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9100, debug=True)

"""
app.py
------
Entry point for the ZeNA AI Assistant backend.

Run with:  python app.py
Server starts on http://localhost:5000
All chat endpoints are mounted under /api (see routes/chat.py).
"""

from flask import Flask, jsonify
from flask_cors import CORS

from database.db import init_db
from routes.chat import chat_bp


def create_app():
    app = Flask(__name__)

    # Allow the Vite dev server (default :5173) and any frontend origin
    # to call the API during local development. Tighten this in production
    # to your actual website domain.
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Create SQLite tables on startup if they don't exist yet
    init_db()

    app.register_blueprint(chat_bp, url_prefix="/api")

    @app.route("/")
    def health_check():
        return jsonify({"status": "ok", "service": "ZeNA AI Assistant backend"})

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

"""Flask application entrypoint for real-time anomaly scoring."""

from __future__ import annotations

from pathlib import Path

from flask import Flask

from src.api.routes import api_bp, load_model_if_exists


def create_app(model_path: str = "models/isolation_forest.joblib") -> Flask:
    app = Flask(__name__)
    app.register_blueprint(api_bp)

    loaded_model = load_model_if_exists(Path(model_path))
    app.config["MODEL"] = loaded_model

    @app.errorhandler(RuntimeError)
    def handle_runtime_error(err):
        return {"error": str(err)}, 503

    return app


if __name__ == "__main__":
    flask_app = create_app()
    flask_app.run(host="0.0.0.0", port=5000, debug=False)

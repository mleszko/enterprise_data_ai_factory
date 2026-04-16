"""Flask route handlers for anomaly scoring."""

from __future__ import annotations

from pathlib import Path

import joblib
import numpy as np
from flask import Blueprint, current_app, jsonify, request

from src.ml.features_numpy import RollingFeatureConfig, transform_sales_series_to_features

api_bp = Blueprint("api", __name__)


def _get_model():
    model = current_app.config.get("MODEL")
    if model is None:
        raise RuntimeError("Model not loaded")
    return model


@api_bp.get("/health")
def health() -> tuple:
    return jsonify({"status": "ok"}), 200


@api_bp.post("/score")
def score_sales_series() -> tuple:
    payload = request.get_json(silent=True) or {}
    sales = payload.get("sales")
    if not isinstance(sales, list) or len(sales) < 48:
        return (
            jsonify(
                {
                    "error": "sales must be a list with at least 48 numeric points",
                }
            ),
            400,
        )

    values = np.asarray(sales, dtype=np.float64)
    features = transform_sales_series_to_features(values, RollingFeatureConfig())

    model = _get_model()
    # Senior robustness pattern: normalize model outputs to ndarray boundaries.
    # Some test doubles or wrapped models can return Python lists, while sklearn
    # estimators typically return ndarrays. Coercing once avoids fragile code.
    preds = np.asarray(model.predict(features))
    scores = np.asarray(model.decision_function(features))

    return (
        jsonify(
            {
                "window_count": int(features.shape[0]),
                "anomaly_count": int((preds == -1).sum()),
                "predictions": preds.tolist(),
                "scores": scores.tolist(),
            }
        ),
        200,
    )


def load_model_if_exists(path: Path):
    if path.exists():
        return joblib.load(path)
    return None

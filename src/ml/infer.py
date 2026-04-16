"""Inference entrypoint for retail anomaly model."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
import numpy as np

from src.ml.features_numpy import RollingFeatureConfig, transform_sales_series_to_features


def score_series(input_path: Path, model_path: Path, output_path: Path) -> None:
    payload = json.loads(input_path.read_text(encoding="utf-8"))
    sales = np.asarray(payload["sales"], dtype=np.float64)

    features = transform_sales_series_to_features(sales, RollingFeatureConfig())
    pipeline = joblib.load(model_path)

    predictions = pipeline.predict(features)
    scores = pipeline.decision_function(features)

    result = {
        "window_count": int(features.shape[0]),
        "anomaly_count": int((predictions == -1).sum()),
        "predictions": predictions.tolist(),
        "scores": scores.tolist(),
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Score anomaly model")
    parser.add_argument("--input", required=True, type=Path, help="JSON file with sales list")
    parser.add_argument("--model", required=True, type=Path, help="Model artifact path")
    parser.add_argument("--output", required=True, type=Path, help="Output score path")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    score_series(args.input, args.model, args.output)

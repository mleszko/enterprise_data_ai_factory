"""Training entrypoint for retail anomaly model."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
import numpy as np

from src.ml.features_numpy import RollingFeatureConfig, transform_sales_series_to_features
from src.ml.pipeline import AnomalyPipelineConfig, build_anomaly_pipeline


def _load_sales_series(path: Path) -> np.ndarray:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return np.asarray(payload["sales"], dtype=np.float64)


def train_model(input_path: Path, model_path: Path) -> None:
    sales = _load_sales_series(input_path)
    features = transform_sales_series_to_features(sales, RollingFeatureConfig())

    pipeline = build_anomaly_pipeline(AnomalyPipelineConfig())
    pipeline.fit(features)

    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, model_path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train anomaly model")
    parser.add_argument("--input", required=True, type=Path, help="JSON file with sales list")
    parser.add_argument("--output", required=True, type=Path, help="Output model artifact path")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    train_model(args.input, args.output)

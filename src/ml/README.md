# src/ml/

Machine learning core for retail anomaly detection.

## Files

- `features_numpy.py`: Vectorized rolling-window feature engineering.
- `pipeline.py`: sklearn `Pipeline` factory (`StandardScaler -> PCA -> IsolationForest`).
- `train.py`: CLI training entrypoint.
- `infer.py`: CLI inference entrypoint.

## Senior Usage Notes

- Keep feature extraction vectorized to avoid Python loop overhead.
- Use one sklearn `Pipeline` object for both training and inference to prevent train/serve skew.
- Persist only model artifacts built from deterministic configs and documented seeds.

## Quick Commands

- Train:
  - `python3 -m src.ml.train --input data/training/sales_series.json --output models/isolation_forest.joblib`
- Infer:
  - `python3 -m src.ml.infer --input data/inference/sales_series.json --model models/isolation_forest.joblib --output artifacts/latest_scores.json`

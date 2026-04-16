# tests/

Targeted tests validating the core platform layers.

## Test Files

- `test_features_numpy.py`: rolling-window and feature engineering checks.
- `test_pipeline.py`: sklearn pipeline fit/predict behavior.
- `test_spark_etl.py`: PySpark cleansing and aggregation semantics.
- `test_api.py`: Flask `/health` and `/score` endpoint behavior.

## Run

`python3 -m pytest tests/test_features_numpy.py tests/test_pipeline.py tests/test_api.py tests/test_spark_etl.py`

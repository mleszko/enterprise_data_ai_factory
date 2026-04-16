import numpy as np

from src.ml.features_numpy import (
    RollingFeatureConfig,
    build_rolling_window_matrix,
    transform_sales_series_to_features,
)


def test_build_rolling_window_matrix_shapes_expected():
    series = np.arange(60, dtype=float)
    cfg = RollingFeatureConfig(window_size=10, stride=2, min_required_observations=20)

    windows = build_rolling_window_matrix(series, cfg)

    assert windows.shape == (26, 10)
    assert windows[0, 0] == 0.0
    assert windows[1, 0] == 2.0


def test_transform_sales_series_to_features_returns_dense_scaled_matrix():
    series = np.linspace(10, 100, 96)

    features = transform_sales_series_to_features(series)

    assert features.ndim == 2
    assert features.shape[1] == 7
    assert np.isfinite(features).all()

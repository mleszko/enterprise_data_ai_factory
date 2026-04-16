"""NumPy-centric feature engineering for retail time-series signals."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np


@dataclass(frozen=True)
class RollingFeatureConfig:
    """Configuration for transforming a 1D series into windowed features."""

    window_size: int = 24
    stride: int = 1
    min_required_observations: int = 48


def _validate_series(series: np.ndarray, config: RollingFeatureConfig) -> np.ndarray:
    """Validate and coerce a raw series to a contiguous float ndarray."""
    if config.window_size <= 1:
        raise ValueError("window_size must be > 1")
    if config.stride <= 0:
        raise ValueError("stride must be > 0")

    array = np.asarray(series, dtype=np.float64)
    if array.ndim != 1:
        raise ValueError("series must be 1-dimensional")
    if array.size < config.min_required_observations:
        raise ValueError(
            "series is shorter than min_required_observations; "
            "provide a longer history for stable window statistics"
        )
    if np.isnan(array).all():
        raise ValueError("series cannot be all NaN")

    # Senior practice: impute NaN once at boundary, then keep core math branch pure.
    if np.isnan(array).any():
        mean_value = np.nanmean(array)
        array = np.where(np.isnan(array), mean_value, array)

    return np.ascontiguousarray(array)


def build_rolling_window_matrix(series: Iterable[float], config: RollingFeatureConfig) -> np.ndarray:
    """Convert a 1D signal into a 2D rolling-window matrix.

    Each row is one temporal context window. This matrix representation unlocks
    vectorized feature extraction over all windows simultaneously.
    """
    validated = _validate_series(np.asarray(list(series), dtype=np.float64), config)
    if validated.size < config.window_size:
        raise ValueError("series length must be >= window_size")

    n_rows = (validated.size - config.window_size) // config.stride + 1
    row_starts = np.arange(n_rows)[:, None] * config.stride
    col_offsets = np.arange(config.window_size)[None, :]
    return validated[row_starts + col_offsets]


def _safe_scale(values: np.ndarray, epsilon: float = 1e-8) -> np.ndarray:
    """Scale each column with numerical-stability guard."""
    means = values.mean(axis=0)
    stds = values.std(axis=0)
    return (values - means) / np.maximum(stds, epsilon)


def engineer_numpy_features(window_matrix: np.ndarray) -> np.ndarray:
    """Engineer dense anomaly features from rolling windows.

    Features are intentionally vectorized. We avoid Python loops to reduce
    interpreter overhead and to keep cache-friendly contiguous array math.
    """
    if window_matrix.ndim != 2:
        raise ValueError("window_matrix must be 2-dimensional")
    if window_matrix.shape[1] < 4:
        raise ValueError("window_matrix needs at least 4 points per window")

    mean_ = window_matrix.mean(axis=1)
    std_ = window_matrix.std(axis=1)
    min_ = window_matrix.min(axis=1)
    max_ = window_matrix.max(axis=1)

    # Trend proxy: difference between second half and first half means.
    midpoint = window_matrix.shape[1] // 2
    first_half_mean = window_matrix[:, :midpoint].mean(axis=1)
    second_half_mean = window_matrix[:, midpoint:].mean(axis=1)
    half_delta = second_half_mean - first_half_mean

    # Last-step momentum captures sudden movement near scoring time.
    last_step_delta = window_matrix[:, -1] - window_matrix[:, -2]

    stacked = np.column_stack(
        [
            mean_,
            std_,
            min_,
            max_,
            max_ - min_,
            half_delta,
            last_step_delta,
        ]
    )

    # Senior practice: normalize engineered features before PCA/IForest so the
    # downstream model focuses on structure rather than raw unit scale.
    return _safe_scale(stacked)


def transform_sales_series_to_features(
    series: Iterable[float], config: RollingFeatureConfig | None = None
) -> np.ndarray:
    """One-shot transformation from raw sales vector to ML-ready matrix."""
    config = config or RollingFeatureConfig()
    windows = build_rolling_window_matrix(series, config)
    return engineer_numpy_features(windows)

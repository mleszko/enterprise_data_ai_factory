"""scikit-learn pipeline factory for anomaly detection."""

from __future__ import annotations

from dataclasses import dataclass

from sklearn.decomposition import PCA
from sklearn.ensemble import IsolationForest
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


@dataclass(frozen=True)
class AnomalyPipelineConfig:
    """Configuration values for reproducible anomaly training/inference."""

    pca_components: int = 3
    contamination: float = 0.03
    random_state: int = 42
    n_estimators: int = 200


def build_anomaly_pipeline(config: AnomalyPipelineConfig | None = None) -> Pipeline:
    """Build a full preprocessing+model pipeline.

    Senior practice: never split preprocessing and model objects for production
    anomaly systems. A single Pipeline prevents train/serve skew and makes
    serialization straightforward.
    """
    config = config or AnomalyPipelineConfig()

    pipeline = Pipeline(
        steps=[
            ("standard_scaler", StandardScaler()),
            (
                "pca",
                PCA(
                    n_components=config.pca_components,
                    random_state=config.random_state,
                ),
            ),
            (
                "isolation_forest",
                IsolationForest(
                    contamination=config.contamination,
                    n_estimators=config.n_estimators,
                    random_state=config.random_state,
                ),
            ),
        ]
    )
    return pipeline

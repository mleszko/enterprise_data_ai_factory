import numpy as np

from src.ml.pipeline import AnomalyPipelineConfig, build_anomaly_pipeline


def test_pipeline_fit_predict_shapes():
    rng = np.random.default_rng(42)
    x = rng.normal(size=(300, 7))
    x[:5] += 6.0

    pipe = build_anomaly_pipeline(AnomalyPipelineConfig(pca_components=3, contamination=0.05))
    pipe.fit(x)

    preds = pipe.predict(x)
    scores = pipe.decision_function(x)

    assert preds.shape == (300,)
    assert scores.shape == (300,)
    assert set(np.unique(preds)).issubset({-1, 1})

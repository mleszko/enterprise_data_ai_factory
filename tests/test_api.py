from src.api.app import create_app


class DummyModel:
    def predict(self, features):
        return [1 for _ in range(len(features))]

    def decision_function(self, features):
        return [0.2 for _ in range(len(features))]


def test_health_and_score_endpoints():
    app = create_app(model_path="models/non_existing.joblib")
    app.config["TESTING"] = True
    app.config["MODEL"] = DummyModel()

    client = app.test_client()

    health = client.get("/health")
    assert health.status_code == 200

    payload = {"sales": list(range(1, 100))}
    scored = client.post("/score", json=payload)
    assert scored.status_code == 200
    data = scored.get_json()
    assert "window_count" in data
    assert "anomaly_count" in data

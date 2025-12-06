from fastapi.testclient import TestClient
from main import app
from config import get_settings
from model import ObservabilityModel


client = TestClient(app)


def test_health_returns_env_and_cpu():
    """Validate /health returns settings from environment."""
    resp = client.get("/health")
    assert resp.status_code == 200

    data = resp.json()

    assert "app_env" in data
    assert "cpu_burn_ms" in data
    assert isinstance(data["cpu_burn_ms"], int)
    assert data["cpu_burn_ms"] > 0


def test_model_prediction_logic():
    """Direct model functional test."""
    model = ObservabilityModel()
    result = model.predict([1, 2, 3])
    assert result == 6.0


def test_predict_endpoint():
    """Ensure /predict endpoint returns prediction + telemetry attributes."""
    resp = client.post("/predict", json={"features": [1, 2, 3]})
    assert resp.status_code == 200

    body = resp.json()
    assert "prediction" in body
    assert body["prediction"] == 6.0

    assert "latency_ms" in body
    assert "cpu_burn_ms" in body
    assert body["cpu_burn_ms"] == get_settings().cpu_burn_ms

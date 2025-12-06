from fastapi.testclient import TestClient
from main import app
from config import get_settings
from model import ResourceAwareModel

client = TestClient(app)


def test_health_env_and_cpu():
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert "env" in data
    assert "cpu_burn_ms" in data
    # Default CPU burn should be positive
    assert data["cpu_burn_ms"] > 0


def test_model_predict():
    model = ResourceAwareModel()
    result = model.predict([1.0, 2.0, 3.0])
    assert result == 6.0


def test_predict_endpoint():
    settings = get_settings()
    payload = {"features": [0.5, 1.5, 2.0]}
    resp = client.post("/predict", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["prediction"] == 4.0
    assert data["model_name"] == "simple-linear-resource-aware"
    assert data["cpu_burn_ms"] == settings.cpu_burn_ms

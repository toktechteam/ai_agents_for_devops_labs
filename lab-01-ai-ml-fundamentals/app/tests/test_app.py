from fastapi.testclient import TestClient
from main import app
from model import SimpleLinearModel

client = TestClient(app)


def test_model_predict():
    model = SimpleLinearModel()
    result = model.predict([1.0, 2.0, 3.0])
    assert result == 6.0


def test_health_default_env():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "env" in data


def test_predict_with_features():
    payload = {"features": [0.5, 1.5, 2.0]}
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["prediction"] == 4.0
    assert data["model_name"] == "simple-linear-demo"
    assert isinstance(data["latency_ms"], int)

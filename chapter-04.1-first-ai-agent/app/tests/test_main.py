from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_health_endpoint():
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["version"] == "1.0.0"


def test_alerts_endpoint():
    payload = {"type": "high_cpu", "service": "payment-api"}
    resp = client.post("/alerts", json=payload)
    assert resp.status_code == 200

    data = resp.json()
    assert data["alert"] == payload
    assert "plan" in data
    assert "steps" in data
    assert "episodic_id" in data
    assert "memory_snapshot" in data

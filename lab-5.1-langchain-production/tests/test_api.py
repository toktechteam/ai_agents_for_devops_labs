import json
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_root():
    res = client.get("/")
    assert res.status_code == 200
    assert "running" in res.json()["message"]


def test_investigation():
    payload = {"alert": "High CPU on pod test-pod"}
    res = client.post("/investigate", json=payload)

    assert res.status_code == 200

    data = res.json()

    assert "analysis" in data
    assert "logs" in data
    assert "metrics" in data
    assert "remediation" in data
    assert "cost" in data

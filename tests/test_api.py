from fastapi.testclient import TestClient

from src.api.app import app


def test_health_endpoint_ok():
    client = TestClient(app)
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"



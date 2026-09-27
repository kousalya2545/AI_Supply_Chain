from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_root():
    response = client.get("/")

    assert response.status_code == 200

    body = response.json()

    assert "application" in body
    assert body["status"] == "running"


def test_data_status():
    response = client.get("/api/data/status")

    assert response.status_code == 200

    body = response.json()

    assert body["status"] == "success"
    assert "datasets" in body


def test_dashboard():
    response = client.get("/api/analytics/dashboard")

    assert response.status_code == 200

    body = response.json()

    assert "total_orders" in body
    assert "late_orders" in body


def test_routing_evaluation():
    response = client.get("/api/evaluation/routing")

    assert response.status_code == 200

    body = response.json()

    assert 0 <= body["intent_accuracy"] <= 1


def test_evaluation_summary():
    response = client.get("/api/evaluation/summary")

    assert response.status_code == 200

    body = response.json()

    assert body["status"] == "success"


def test_audit_endpoint():
    response = client.get("/api/audit/recent")

    assert response.status_code == 200

    body = response.json()

    assert body["status"] == "success"


def test_query():
    response = client.post(
        "/api/query",
        json={
            "query": "Why is product P00003 at inventory risk?"
        }
    )

    assert response.status_code == 200

    body = response.json()

    assert body["intent"] == "inventory_risk"
    assert body["confidence"] >= 0
    assert "evidence" in body

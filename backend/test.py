from fastapi.testclient import TestClient

from backend.main import app


def test_get_users():
    client = TestClient(app)
    response = client.get("/api/users")
    assert response.status_code == 200
    assert response.json() == [{"username": "admin"}]
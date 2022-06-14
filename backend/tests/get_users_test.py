def test_get_users(client):
    response = client.get("/api/honkai")
    assert response.status_code == 200
def test_get_categories(client):
    resp = client.get("/categories")
    data = resp.get_json()

    assert resp.status_code == 200
    assert data["success"] is True
    assert "food" in data["categories"]
    assert "salary" in data["categories"]

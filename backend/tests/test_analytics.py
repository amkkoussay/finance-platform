def _create_txn(client, headers, **overrides):
    payload = {
        "date": "2024-06-15",
        "category": "food",
        "amount": 50,
        "description": "Lunch",
        "is_income": False,
    }
    payload.update(overrides)
    return client.post("/transactions", json=payload, headers=headers)


def test_get_summary(client, auth_headers):
    _create_txn(client, auth_headers, category="salary", amount=1000, is_income=True)
    _create_txn(client, auth_headers, category="food", amount=100, is_income=False)

    resp = client.get("/analytics/summary", headers=auth_headers)
    data = resp.get_json()["summary"]

    assert resp.status_code == 200
    assert data["total_income"] == 1000
    assert data["total_expense"] == 100
    assert data["balance"] == 900
    assert data["transaction_count"] == 2


def test_get_by_category(client, auth_headers):
    _create_txn(client, auth_headers, category="food", amount=50, date="2024-06-10")
    _create_txn(client, auth_headers, category="transport", amount=30, date="2024-06-12")

    resp = client.get("/analytics/by-category?month=2024-06", headers=auth_headers)
    data = resp.get_json()["data"]

    assert resp.status_code == 200
    assert data.get("food") == 50
    assert data.get("transport") == 30


def test_get_monthly(client, auth_headers):
    _create_txn(client, auth_headers)

    resp = client.get("/analytics/monthly?months=3", headers=auth_headers)
    data = resp.get_json()["data"]

    assert resp.status_code == 200
    assert len(data) == 3
    assert data[0]["month"] < data[-1]["month"]


def test_get_spending_rate(client, auth_headers):
    _create_txn(client, auth_headers, amount=30)

    resp = client.get("/analytics/spending-rate?days=30", headers=auth_headers)
    data = resp.get_json()["rate"]

    assert resp.status_code == 200
    assert "daily_average" in data
    assert "total_period" in data


def test_analytics_requires_auth(client):
    resp = client.get("/analytics/summary")
    assert resp.status_code == 401

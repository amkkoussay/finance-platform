from datetime import datetime, timezone


def _date_months_ago(months_ago, day=10):
    """Return a YYYY-MM-DD string `months_ago` months before today."""
    cursor = datetime.now(timezone.utc).replace(tzinfo=None, day=1)
    for _ in range(months_ago):
        prev_month = cursor.month - 1 or 12
        prev_year = cursor.year - 1 if cursor.month == 1 else cursor.year
        cursor = cursor.replace(year=prev_year, month=prev_month, day=1)
    return cursor.replace(day=day).strftime("%Y-%m-%d")


def _create_txn(client, headers, **overrides):
    payload = {
        "date": "2024-06-15",
        "category": "food",
        "amount": 50,
        "description": "",
        "is_income": False,
    }
    payload.update(overrides)
    return client.post("/transactions", json=payload, headers=headers)


def test_monthly_forecast_increasing_trend(client, auth_headers):
    # Spending climbs every month: 100 -> 150 -> 200 -> 250 -> 300 -> 350
    for i, months_ago in enumerate(range(5, -1, -1)):
        _create_txn(
            client, auth_headers, date=_date_months_ago(months_ago), amount=100 + i * 50
        )

    resp = client.get("/predictions/monthly-forecast", headers=auth_headers)
    data = resp.get_json()["forecast"]

    assert resp.status_code == 200
    assert data["trend"] == "increasing"
    # Next month should be forecast higher than the most recent actual month
    assert data["forecast_next_month"] > data["history"][-1]["total"]


def test_category_forecast_for_valid_category(client, auth_headers):
    _create_txn(client, auth_headers, date=_date_months_ago(1), category="transport", amount=40)
    _create_txn(client, auth_headers, date=_date_months_ago(0), category="transport", amount=60)

    resp = client.get("/predictions/category-forecast/transport", headers=auth_headers)
    data = resp.get_json()["forecast"]

    assert resp.status_code == 200
    assert data["category"] == "transport"
    assert "forecast_next_month" in data


def test_category_forecast_rejects_invalid_category(client, auth_headers):
    resp = client.get("/predictions/category-forecast/not-a-category", headers=auth_headers)
    assert resp.status_code == 400


def test_category_forecast_rejects_salary(client, auth_headers):
    resp = client.get("/predictions/category-forecast/salary", headers=auth_headers)
    assert resp.status_code == 400


def test_recommendations_returns_ranked_savings(client, auth_headers):
    _create_txn(client, auth_headers, date=_date_months_ago(0), category="food", amount=300)
    _create_txn(client, auth_headers, date=_date_months_ago(0), category="entertainment", amount=100)

    resp = client.get("/predictions/recommendations", headers=auth_headers)
    data = resp.get_json()["recommendations"]

    assert resp.status_code == 200
    assert len(data) >= 2
    # Highest spend category should yield the highest projected savings, first in the list
    assert data[0]["category"] == "food"
    assert data[0]["estimated_annual_savings"] > data[1]["estimated_annual_savings"]


def test_predictions_require_auth(client):
    resp = client.get("/predictions/monthly-forecast")
    assert resp.status_code == 401

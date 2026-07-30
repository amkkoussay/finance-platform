import io


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


def test_create_transaction_success(client, auth_headers):
    resp = _create_txn(client, auth_headers)
    data = resp.get_json()

    assert resp.status_code == 201
    assert data["success"] is True
    assert data["transaction"]["category"] == "food"
    assert data["transaction"]["amount"] == 50


def test_create_invalid_category(client, auth_headers):
    resp = _create_txn(client, auth_headers, category="not-a-category")
    data = resp.get_json()

    assert resp.status_code == 400
    assert data["success"] is False


def test_create_invalid_amount(client, auth_headers):
    resp = _create_txn(client, auth_headers, amount=-10)
    data = resp.get_json()

    assert resp.status_code == 400
    assert data["success"] is False


def test_create_without_token_is_rejected(client):
    resp = _create_txn(client, headers={})
    assert resp.status_code == 401


def test_get_transactions(client, auth_headers):
    _create_txn(client, auth_headers)
    _create_txn(client, auth_headers, category="transport", amount=20)

    resp = client.get("/transactions", headers=auth_headers)
    data = resp.get_json()

    assert resp.status_code == 200
    assert data["success"] is True
    assert len(data["transactions"]) == 2


def test_delete_transaction(client, auth_headers):
    create_resp = _create_txn(client, auth_headers)
    txn_id = create_resp.get_json()["transaction"]["id"]

    resp = client.delete(f"/transactions/{txn_id}", headers=auth_headers)
    data = resp.get_json()

    assert resp.status_code == 200
    assert data["success"] is True

    get_resp = client.get(f"/transactions/{txn_id}", headers=auth_headers)
    assert get_resp.status_code == 404


def test_bulk_upload(client, auth_headers):
    csv_content = (
        "date,category,amount,description,is_income\n"
        "2024-06-01,food,20,Snacks,false\n"
        "2024-06-02,salary,1000,Paycheck,true\n"
    )
    data = {
        "file": (io.BytesIO(csv_content.encode("utf-8")), "transactions.csv"),
    }

    resp = client.post(
        "/transactions/bulk-upload",
        data=data,
        content_type="multipart/form-data",
        headers=auth_headers,
    )
    result = resp.get_json()

    assert resp.status_code == 200
    assert result["success"] is True
    assert result["imported"] == 2
    assert result["errors"] == []

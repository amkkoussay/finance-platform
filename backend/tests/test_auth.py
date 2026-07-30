def test_register_success(client):
    resp = client.post(
        "/auth/register",
        json={
            "email": "new@example.com",
            "username": "newuser",
            "password": "password123",
            "confirm_password": "password123",
        },
    )
    data = resp.get_json()

    assert resp.status_code == 201
    assert data["success"] is True
    assert data["user"]["email"] == "new@example.com"
    assert data["user"]["username"] == "newuser"


def test_register_duplicate_email(client, registered_user):
    resp = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",  # already used by registered_user fixture
            "username": "someoneelse",
            "password": "password123",
            "confirm_password": "password123",
        },
    )
    data = resp.get_json()

    assert resp.status_code == 400
    assert data["success"] is False


def test_register_weak_password(client):
    resp = client.post(
        "/auth/register",
        json={
            "email": "weak@example.com",
            "username": "weakuser",
            "password": "123",
            "confirm_password": "123",
        },
    )
    data = resp.get_json()

    assert resp.status_code == 400
    assert data["success"] is False


def test_login_success(client, registered_user):
    resp = client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "password123"},
    )
    data = resp.get_json()

    assert resp.status_code == 200
    assert data["success"] is True
    assert data["user"]["email"] == "test@example.com"
    assert data["user"]["token"]


def test_login_invalid_credentials(client, registered_user):
    resp = client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "wrong-password"},
    )
    data = resp.get_json()

    assert resp.status_code == 401
    assert data["success"] is False


def test_register_returns_token(client):
    resp = client.post(
        "/auth/register",
        json={
            "email": "tokened@example.com",
            "username": "tokeneduser",
            "password": "password123",
            "confirm_password": "password123",
        },
    )
    data = resp.get_json()

    assert resp.status_code == 201
    assert data["user"]["token"]


def test_protected_route_without_token_is_rejected(client):
    resp = client.get("/transactions")
    data = resp.get_json()

    assert resp.status_code == 401
    assert data["success"] is False


def test_protected_route_with_invalid_token_is_rejected(client):
    resp = client.get(
        "/transactions", headers={"Authorization": "Bearer not-a-real-token"}
    )
    assert resp.status_code == 401


def test_user_cannot_access_another_users_transaction(client, registered_user, auth_headers):
    # A second user's transaction should be invisible even if you know its id
    other_resp = client.post(
        "/auth/register",
        json={
            "email": "other@example.com",
            "username": "otheruser",
            "password": "password123",
            "confirm_password": "password123",
        },
    )
    other_token = other_resp.get_json()["user"]["token"]
    other_headers = {"Authorization": f"Bearer {other_token}"}

    create_resp = client.post(
        "/transactions",
        json={
            "date": "2024-06-15",
            "category": "food",
            "amount": 50,
            "description": "Lunch",
            "is_income": False,
        },
        headers=auth_headers,
    )
    txn_id = create_resp.get_json()["transaction"]["id"]

    resp = client.get(f"/transactions/{txn_id}", headers=other_headers)
    assert resp.status_code == 404

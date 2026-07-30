import pytest

from app import create_app
from config import TestConfig
from models import db


@pytest.fixture
def app():
    """A fresh Flask app with an in-memory SQLite database for each test."""
    flask_app = create_app(TestConfig)
    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def registered_user(client):
    """Registers a user and returns {user_id, email, username, token}."""
    resp = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "password123",
            "confirm_password": "password123",
        },
    )
    return resp.get_json()["user"]


@pytest.fixture
def auth_headers(registered_user):
    """Authorization header for `registered_user`, ready to pass into any
    protected-route request: `client.get(url, headers=auth_headers)`."""
    return {"Authorization": f"Bearer {registered_user['token']}"}

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Base application configuration, pulled from environment variables with sane defaults."""

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI", "sqlite:///finance.db"
    )
    # No fallback: a missing SECRET_KEY must fail loudly at app creation
    # (see create_app in app.py) instead of silently signing JWTs with a
    # publicly known default. Set SECRET_KEY in the environment or a
    # backend/.env file; see backend/.env.example.
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False


class TestConfig(Config):
    """Configuration used by the pytest suite — isolated in-memory database."""

    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    TESTING = True
    SECRET_KEY = "test-key"

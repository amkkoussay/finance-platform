from app import app
from models import db


def init_db():
    """Create all database tables from the SQLAlchemy models."""
    with app.app_context():
        db.create_all()
    print("Database initialized successfully")


if __name__ == "__main__":
    init_db()

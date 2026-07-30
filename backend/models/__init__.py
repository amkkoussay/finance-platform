from flask_sqlalchemy import SQLAlchemy

# Single shared SQLAlchemy instance used across the whole app
db = SQLAlchemy()

# Import models so they register with SQLAlchemy's metadata
# (must come after `db` is defined to avoid circular imports)
from models.user import User  # noqa: E402,F401
from models.transaction import Transaction  # noqa: E402,F401

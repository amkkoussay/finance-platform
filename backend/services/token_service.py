from datetime import datetime, timedelta, timezone

import jwt
from flask import current_app

from services.validation import ValidationError


def generate_token(user_id):
    """Create a signed JWT that identifies `user_id`, valid for JWT_EXPIRATION_HOURS."""
    from constants import JWT_EXPIRATION_HOURS

    now = datetime.now(timezone.utc)
    payload = {
        "user_id": user_id,
        "iat": now,
        "exp": now + timedelta(hours=JWT_EXPIRATION_HOURS),
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")


def decode_token(token):
    """Validate a JWT and return the user_id it was issued for.

    Raises ValidationError (-> 401 at the route layer) if the token is
    missing, malformed, expired, or signed with the wrong key.
    """
    if not token:
        raise ValidationError("Authentication token is required")

    try:
        payload = jwt.decode(
            token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
        )
    except jwt.ExpiredSignatureError:
        raise ValidationError("Session expired, please log in again")
    except jwt.InvalidTokenError:
        raise ValidationError("Invalid authentication token")

    user_id = payload.get("user_id")
    if user_id is None:
        raise ValidationError("Invalid authentication token")
    return user_id

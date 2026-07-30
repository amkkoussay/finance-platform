from functools import wraps

from flask import g, jsonify, request

from services.token_service import decode_token
from services.validation import ValidationError


def token_required(view_func):
    """Require a valid `Authorization: Bearer <token>` header.

    On success, sets `g.user_id` to the authenticated user's id so the
    route/service layer never has to trust a client-supplied user_id again.
    On failure, short-circuits with a 401 before the view runs.
    """

    @wraps(view_func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        token = None
        if auth_header.startswith("Bearer "):
            token = auth_header[len("Bearer "):].strip()

        try:
            g.user_id = decode_token(token)
        except ValidationError as e:
            return jsonify({"success": False, "error": str(e)}), 401

        return view_func(*args, **kwargs)

    return wrapper

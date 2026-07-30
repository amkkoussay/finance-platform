from flask import Blueprint, jsonify

from constants import CATEGORIES

bp = Blueprint("categories", __name__, url_prefix="/categories")


@bp.route("", methods=["GET"])
def get_categories():
    """Static list of allowed transaction categories.

    Public on purpose: it's fixed, non-sensitive reference data (used to
    populate the category <select> on the frontend), so it doesn't need a
    logged-in user like the rest of the API.
    """
    return jsonify({"success": True, "categories": CATEGORIES}), 200

from flask import Blueprint, jsonify, request

from services.auth_service import AuthService
from services.validation import ValidationError

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    try:
        user = AuthService.register(
            email=data.get("email"),
            username=data.get("username"),
            password=data.get("password"),
            confirm_password=data.get("confirm_password"),
        )
        return jsonify({"success": True, "user": user}), 201
    except ValidationError as e:
        return jsonify({"success": False, "error": str(e)}), 400


@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    try:
        user = AuthService.login(
            email=data.get("email"),
            password=data.get("password"),
        )
        return jsonify({"success": True, "user": user}), 200
    except ValidationError as e:
        return jsonify({"success": False, "error": str(e)}), 401

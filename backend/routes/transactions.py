from flask import Blueprint, g, jsonify, request

from middleware import token_required
from services.transaction_service import TransactionService
from services.validation import ValidationError

bp = Blueprint("transactions", __name__, url_prefix="/transactions")


@bp.route("", methods=["POST"])
@token_required
def create_transaction():
    data = request.get_json(silent=True) or {}
    try:
        txn = TransactionService.create(
            user_id=g.user_id,
            date=data.get("date"),
            category=data.get("category"),
            amount=data.get("amount"),
            description=data.get("description"),
            is_income=data.get("is_income", False),
        )
        return jsonify({"success": True, "transaction": txn}), 201
    except ValidationError as e:
        return jsonify({"success": False, "error": str(e)}), 400


@bp.route("", methods=["GET"])
@token_required
def get_transactions():
    try:
        txns = TransactionService.get_all(g.user_id)
        return jsonify({"success": True, "transactions": txns}), 200
    except ValidationError as e:
        return jsonify({"success": False, "error": str(e)}), 404


@bp.route("/<int:transaction_id>", methods=["GET"])
@token_required
def get_transaction(transaction_id):
    try:
        txn = TransactionService.get_by_id(transaction_id, g.user_id)
        return jsonify({"success": True, "transaction": txn}), 200
    except ValidationError as e:
        return jsonify({"success": False, "error": str(e)}), 404


@bp.route("/<int:transaction_id>", methods=["PUT"])
@token_required
def update_transaction(transaction_id):
    data = request.get_json(silent=True) or {}
    try:
        txn = TransactionService.update(
            transaction_id=transaction_id,
            user_id=g.user_id,
            date=data.get("date"),
            category=data.get("category"),
            amount=data.get("amount"),
            description=data.get("description"),
            is_income=data.get("is_income", False),
        )
        return jsonify({"success": True, "transaction": txn}), 200
    except ValidationError as e:
        return jsonify({"success": False, "error": str(e)}), 400


@bp.route("/<int:transaction_id>", methods=["DELETE"])
@token_required
def delete_transaction(transaction_id):
    try:
        TransactionService.delete(transaction_id, g.user_id)
        return jsonify({"success": True, "message": "Deleted"}), 200
    except ValidationError as e:
        return jsonify({"success": False, "error": str(e)}), 404


@bp.route("/bulk-upload", methods=["POST"])
@token_required
def bulk_upload():
    file = request.files.get("file")

    if not file:
        return jsonify({"success": False, "error": "CSV file is required"}), 400

    try:
        result = TransactionService.bulk_upload(g.user_id, file)
        return jsonify({"success": True, **result}), 200
    except ValidationError as e:
        return jsonify({"success": False, "error": str(e)}), 400

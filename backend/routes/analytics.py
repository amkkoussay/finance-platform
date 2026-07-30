from flask import Blueprint, g, jsonify, request

from middleware import token_required
from services.analytics_service import AnalyticsService
from services.validation import ValidationError

bp = Blueprint("analytics", __name__, url_prefix="/analytics")


@bp.route("/summary", methods=["GET"])
@token_required
def summary():
    try:
        data = AnalyticsService.get_summary(g.user_id)
        return jsonify({"success": True, "summary": data}), 200
    except ValidationError as e:
        return jsonify({"success": False, "error": str(e)}), 404


@bp.route("/by-category", methods=["GET"])
@token_required
def by_category():
    month = request.args.get("month")
    try:
        data = AnalyticsService.get_by_category(g.user_id, month)
        return jsonify({"success": True, "data": data}), 200
    except ValidationError as e:
        return jsonify({"success": False, "error": str(e)}), 400


@bp.route("/monthly", methods=["GET"])
@token_required
def monthly():
    months = request.args.get("months", 6, type=int)
    try:
        data = AnalyticsService.get_monthly(g.user_id, months)
        return jsonify({"success": True, "data": data}), 200
    except ValidationError as e:
        return jsonify({"success": False, "error": str(e)}), 404


@bp.route("/spending-rate", methods=["GET"])
@token_required
def spending_rate():
    days = request.args.get("days", 30, type=int)
    try:
        data = AnalyticsService.get_spending_rate(g.user_id, days)
        return jsonify({"success": True, "rate": data}), 200
    except ValidationError as e:
        return jsonify({"success": False, "error": str(e)}), 400

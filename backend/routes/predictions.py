from flask import Blueprint, g, jsonify, request

from middleware import token_required
from services.prediction_service import PredictionService
from services.validation import ValidationError

bp = Blueprint("predictions", __name__, url_prefix="/predictions")


@bp.route("/monthly-forecast", methods=["GET"])
@token_required
def monthly_forecast():
    try:
        data = PredictionService.monthly_forecast(g.user_id)
        return jsonify({"success": True, "forecast": data}), 200
    except ValidationError as e:
        return jsonify({"success": False, "error": str(e)}), 400


@bp.route("/category-forecast/<category>", methods=["GET"])
@token_required
def category_forecast(category):
    try:
        data = PredictionService.category_forecast(g.user_id, category)
        return jsonify({"success": True, "forecast": data}), 200
    except ValidationError as e:
        return jsonify({"success": False, "error": str(e)}), 400


@bp.route("/recommendations", methods=["GET"])
@token_required
def recommendations():
    cut_percent = request.args.get("cut_percent", 10, type=int)
    try:
        data = PredictionService.recommendations(g.user_id, cut_percent)
        return jsonify({"success": True, "recommendations": data}), 200
    except ValidationError as e:
        return jsonify({"success": False, "error": str(e)}), 400

"""Spending forecasts, built with a hand-written linear regression.

No scikit-learn / pandas / numpy: those need compiled C/Fortran extensions
(BLAS, LAPACK) that are painful or impossible to build on Termux/ARM. Ordinary
least-squares for a single feature (month index -> total spend) is just two
sums, so plain Python is all this needs.
"""

from constants import EXPENSE_CATEGORIES
from services.analytics_service import AnalyticsService
from services.validation import ValidationError, validate_category, validate_user_exists
from models import db

# How many past months of history feed the regression, and how far ahead we
# forecast (1 == "next month").
HISTORY_MONTHS = 6
FORECAST_HORIZON = 1

# Below this we don't trust the fit enough to word it as "increasing" /
# "decreasing" -- there just isn't enough signal in a couple of data points.
MIN_MONTHS_FOR_TREND = 3


def linear_regression(x_values, y_values):
    """Ordinary least-squares fit for y = slope * x + intercept.

    Pure Python, no external libraries. Returns (slope, intercept).
    If every x value is identical (zero variance) returns slope 0 and the
    mean of y as the intercept, instead of dividing by zero.
    """
    n = len(x_values)
    if n == 0:
        return 0.0, 0.0

    x_mean = sum(x_values) / n
    y_mean = sum(y_values) / n

    numerator = sum((x_values[i] - x_mean) * (y_values[i] - y_mean) for i in range(n))
    denominator = sum((x_values[i] - x_mean) ** 2 for i in range(n))

    if denominator == 0:
        return 0.0, y_mean

    slope = numerator / denominator
    intercept = y_mean - slope * x_mean
    return slope, intercept


def predict(slope, intercept, x):
    return slope * x + intercept


def _trend_label(slope, y_mean):
    """Classify a slope as increasing/decreasing/stable relative to the
    average level of spending, so a $1/month drift on a $2000 budget reads
    as "stable" rather than "increasing"."""
    if y_mean == 0:
        threshold = 1.0
    else:
        threshold = max(abs(y_mean) * 0.02, 1.0)

    if slope > threshold:
        return "increasing"
    if slope < -threshold:
        return "decreasing"
    return "stable"


class PredictionService:
    @staticmethod
    def monthly_forecast(user_id):
        """Forecast next month's total expense from the last HISTORY_MONTHS."""
        validate_user_exists(user_id, db)

        history = AnalyticsService.get_monthly(user_id, HISTORY_MONTHS)
        xs = list(range(len(history)))
        ys = [m["total"] for m in history]

        slope, intercept = linear_regression(xs, ys)
        next_x = len(history) + FORECAST_HORIZON - 1
        forecast = max(predict(slope, intercept, next_x), 0)

        y_mean = sum(ys) / len(ys) if ys else 0
        has_enough_data = sum(1 for y in ys if y > 0) >= MIN_MONTHS_FOR_TREND

        return {
            "history": history,
            "forecast_next_month": round(forecast, 2),
            "trend": _trend_label(slope, y_mean) if has_enough_data else "insufficient_data",
            "monthly_change": round(slope, 2),
        }

    @staticmethod
    def category_forecast(user_id, category):
        """Forecast next month's spend in a single category."""
        validate_user_exists(user_id, db)
        validate_category(category)

        if category == "salary":
            raise ValidationError("Cannot forecast income categories")

        history = AnalyticsService.get_monthly_by_category(user_id, category, HISTORY_MONTHS)
        xs = list(range(len(history)))
        ys = [m["total"] for m in history]

        slope, intercept = linear_regression(xs, ys)
        next_x = len(history) + FORECAST_HORIZON - 1
        forecast = max(predict(slope, intercept, next_x), 0)

        y_mean = sum(ys) / len(ys) if ys else 0
        has_enough_data = sum(1 for y in ys if y > 0) >= MIN_MONTHS_FOR_TREND

        return {
            "category": category,
            "history": history,
            "forecast_next_month": round(forecast, 2),
            "trend": _trend_label(slope, y_mean) if has_enough_data else "insufficient_data",
        }

    @staticmethod
    def recommendations(user_id, cut_percent=10):
        """"If you cut category X by cut_percent%, you'd save $Y/year."

        Ranked by projected annual savings, based on each category's most
        recent monthly total (falls back to the average of the available
        history if last month happened to be zero).
        """
        validate_user_exists(user_id, db)

        recs = []
        for category in EXPENSE_CATEGORIES:
            history = AnalyticsService.get_monthly_by_category(user_id, category, HISTORY_MONTHS)
            totals = [m["total"] for m in history]
            if not any(totals):
                continue

            recent = totals[-1] if totals[-1] > 0 else (sum(totals) / len(totals))
            monthly_savings = recent * (cut_percent / 100)
            annual_savings = monthly_savings * 12

            if annual_savings <= 0:
                continue

            recs.append(
                {
                    "category": category,
                    "current_monthly_spend": round(recent, 2),
                    "cut_percent": cut_percent,
                    "estimated_monthly_savings": round(monthly_savings, 2),
                    "estimated_annual_savings": round(annual_savings, 2),
                }
            )

        recs.sort(key=lambda r: r["estimated_annual_savings"], reverse=True)
        return recs[:5]

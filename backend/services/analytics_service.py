from datetime import timedelta

from models import db
from models.transaction import Transaction
from services.validation import ValidationError, validate_user_exists
from time_utils import utcnow


class AnalyticsService:
    @staticmethod
    def get_summary(user_id):
        validate_user_exists(user_id, db)
        txns = Transaction.query.filter_by(user_id=int(user_id)).all()

        total_income = sum(t.amount for t in txns if t.is_income)
        total_expense = sum(t.amount for t in txns if not t.is_income)

        return {
            "total_income": round(total_income, 2),
            "total_expense": round(total_expense, 2),
            "balance": round(total_income - total_expense, 2),
            "transaction_count": len(txns),
        }

    @staticmethod
    def get_by_category(user_id, month=None):
        validate_user_exists(user_id, db)

        if month is None:
            month = utcnow().strftime("%Y-%m")

        try:
            year, mon = (int(part) for part in month.split("-"))
        except (ValueError, AttributeError):
            raise ValidationError("Invalid month format. Expected YYYY-MM")

        txns = Transaction.query.filter_by(user_id=int(user_id), is_income=False).all()

        result = {}
        for t in txns:
            if t.date.year == year and t.date.month == mon:
                result[t.category] = round(result.get(t.category, 0) + t.amount, 2)

        return result

    @staticmethod
    def get_monthly(user_id, months=6):
        validate_user_exists(user_id, db)

        txns = Transaction.query.filter_by(user_id=int(user_id), is_income=False).all()
        totals_by_month = {}
        for t in txns:
            key = t.date.strftime("%Y-%m")
            totals_by_month[key] = totals_by_month.get(key, 0) + t.amount

        # Build the list of the last `months` month keys, oldest first
        cursor = utcnow().replace(day=1)
        month_keys = []
        for _ in range(months):
            month_keys.append(cursor.strftime("%Y-%m"))
            prev_month = cursor.month - 1 or 12
            prev_year = cursor.year - 1 if cursor.month == 1 else cursor.year
            cursor = cursor.replace(year=prev_year, month=prev_month, day=1)
        month_keys.reverse()

        return [
            {"month": m, "total": round(totals_by_month.get(m, 0), 2)}
            for m in month_keys
        ]

    @staticmethod
    def get_monthly_by_category(user_id, category, months=6):
        """Same shape as get_monthly(), but totals only one expense category.
        Used by the forecasting engine to fit a trend per category.
        """
        validate_user_exists(user_id, db)

        txns = Transaction.query.filter_by(
            user_id=int(user_id), is_income=False, category=category
        ).all()
        totals_by_month = {}
        for t in txns:
            key = t.date.strftime("%Y-%m")
            totals_by_month[key] = totals_by_month.get(key, 0) + t.amount

        cursor = utcnow().replace(day=1)
        month_keys = []
        for _ in range(months):
            month_keys.append(cursor.strftime("%Y-%m"))
            prev_month = cursor.month - 1 or 12
            prev_year = cursor.year - 1 if cursor.month == 1 else cursor.year
            cursor = cursor.replace(year=prev_year, month=prev_month, day=1)
        month_keys.reverse()

        return [
            {"month": m, "total": round(totals_by_month.get(m, 0), 2)}
            for m in month_keys
        ]

    @staticmethod
    def get_spending_rate(user_id, days=30):
        validate_user_exists(user_id, db)

        if days <= 0:
            raise ValidationError("days must be a positive integer")

        cutoff = (utcnow() - timedelta(days=days)).date()
        txns = Transaction.query.filter_by(user_id=int(user_id), is_income=False).all()
        total = sum(t.amount for t in txns if t.date >= cutoff)

        return {
            "daily_average": round(total / days, 2),
            "total_period": round(total, 2),
        }

from datetime import datetime

from constants import CATEGORIES


class ValidationError(Exception):
    """Raised whenever input data fails a validation rule."""

    pass


def validate_user_exists(user_id, db):
    """Ensure a user with this id exists. Returns the User instance."""
    from models.user import User

    if user_id is None:
        raise ValidationError("user_id is required")

    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        raise ValidationError("user_id must be an integer")

    user = db.session.get(User, user_id)
    if not user:
        raise ValidationError("User not found")
    return user


def validate_email(email):
    """Very basic email format check: must contain '@' and a '.' after it."""
    if not email or "@" not in email:
        raise ValidationError("Invalid email format")

    domain_part = email.split("@")[-1]
    if "." not in domain_part or domain_part.startswith(".") or domain_part.endswith("."):
        raise ValidationError("Invalid email format")

    return email


def validate_password(password, confirm_password=None):
    """Check password length and, optionally, that it matches a confirmation."""
    if not password or len(password) < 6:
        raise ValidationError("Password must be at least 6 characters long")

    if confirm_password is not None and password != confirm_password:
        raise ValidationError("Passwords do not match")

    return password


def validate_category(category):
    if category not in CATEGORIES:
        raise ValidationError(f"Invalid category. Must be one of {CATEGORIES}")
    return category


def validate_date(date_str):
    """Check the date is a string in YYYY-MM-DD format. Returns a date object."""
    if not date_str:
        raise ValidationError("Date is required")
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        raise ValidationError("Invalid date format. Expected YYYY-MM-DD")


def validate_amount(amount):
    """Check the amount is a positive number. Returns it as a float."""
    try:
        amount = float(amount)
    except (TypeError, ValueError):
        raise ValidationError("Amount must be a number")

    if amount <= 0:
        raise ValidationError("Amount must be a positive number")

    return amount


def validate_transaction_belongs_to_user(transaction_id, user_id, db):
    """Ensure the transaction exists and belongs to the given user. Returns the Transaction."""
    from models.transaction import Transaction

    if user_id is None:
        raise ValidationError("user_id is required")

    try:
        transaction_id = int(transaction_id)
        user_id = int(user_id)
    except (TypeError, ValueError):
        raise ValidationError("transaction_id and user_id must be integers")

    txn = db.session.get(Transaction, transaction_id)
    if not txn or txn.user_id != user_id:
        raise ValidationError("Transaction not found")

    return txn

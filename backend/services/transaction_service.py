import csv
import io

from models import db
from models.transaction import Transaction
from services.validation import (
    ValidationError,
    validate_amount,
    validate_category,
    validate_date,
    validate_transaction_belongs_to_user,
    validate_user_exists,
)


class TransactionService:
    @staticmethod
    def create(user_id, date, category, amount, description, is_income):
        validate_user_exists(user_id, db)
        parsed_date = validate_date(date)
        validate_category(category)
        parsed_amount = validate_amount(amount)

        txn = Transaction(
            user_id=int(user_id),
            date=parsed_date,
            category=category,
            amount=parsed_amount,
            description=description,
            is_income=bool(is_income),
        )
        db.session.add(txn)
        db.session.commit()
        return txn.to_dict()

    @staticmethod
    def get_all(user_id):
        validate_user_exists(user_id, db)
        txns = (
            Transaction.query.filter_by(user_id=int(user_id))
            .order_by(Transaction.date.desc())
            .all()
        )
        return [t.to_dict() for t in txns]

    @staticmethod
    def get_by_id(transaction_id, user_id):
        txn = validate_transaction_belongs_to_user(transaction_id, user_id, db)
        return txn.to_dict()

    @staticmethod
    def update(transaction_id, user_id, date, category, amount, description, is_income):
        txn = validate_transaction_belongs_to_user(transaction_id, user_id, db)
        parsed_date = validate_date(date)
        validate_category(category)
        parsed_amount = validate_amount(amount)

        txn.date = parsed_date
        txn.category = category
        txn.amount = parsed_amount
        txn.description = description
        txn.is_income = bool(is_income)

        db.session.commit()
        return txn.to_dict()

    @staticmethod
    def delete(transaction_id, user_id):
        txn = validate_transaction_belongs_to_user(transaction_id, user_id, db)
        db.session.delete(txn)
        db.session.commit()

    @staticmethod
    def bulk_upload(user_id, csv_file):
        """Parse a CSV file (date, category, amount, description, is_income) and
        create one transaction per row. Rows that fail validation are skipped
        and reported in `errors` rather than aborting the whole upload."""
        validate_user_exists(user_id, db)

        raw = csv_file.read()
        if isinstance(raw, bytes):
            raw = raw.decode("utf-8")
        reader = csv.DictReader(io.StringIO(raw))

        imported = 0
        errors = []

        for i, row in enumerate(reader, start=1):
            try:
                is_income_raw = str(row.get("is_income", "")).strip().lower()
                TransactionService.create(
                    user_id=user_id,
                    date=(row.get("date") or "").strip(),
                    category=(row.get("category") or "").strip(),
                    amount=row.get("amount"),
                    description=row.get("description", ""),
                    is_income=is_income_raw in ("1", "true", "yes"),
                )
                imported += 1
            except ValidationError as e:
                errors.append({"row": i, "error": str(e)})

        return {"imported": imported, "errors": errors}

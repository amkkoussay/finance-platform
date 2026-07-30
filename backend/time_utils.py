from datetime import datetime, timezone


def utcnow():
    """Current UTC time as a naive datetime (matches the naive `db.DateTime`
    columns used throughout the models/services), without relying on the
    deprecated `datetime.utcnow()`.
    """
    return datetime.now(timezone.utc).replace(tzinfo=None)

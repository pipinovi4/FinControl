# backend/app/utils/decorators/db.py

from functools import wraps
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
import logging

logger = logging.getLogger(__name__)


def handle_exceptions(default_return=None, raise_404: bool = False):
    """
    Decorator to handle exceptions in DB services.

    Args:
        default_return: Value to return if error occurs (e.g., [] or None).
        raise_404: Raise 404 if result is None.

    Returns:
        Decorated function with exception handling and optional rollback.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                if raise_404 and result is None:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
                return result
            except SQLAlchemyError as e:
                db = getattr(args[0], "db", None)
                if db:
                    db.rollback()
                logger.exception("Database error in %s: %s", func.__name__, str(e))
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"DB error: {str(e)}")

        return wrapper

    return decorator

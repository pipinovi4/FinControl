# backend/app/utils/decorators/db.py

from functools import wraps
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError


def handle_exceptions(default_return=None, raise_404: bool = False):
    """
    Decorator for wrapping DB methods in try/except.

    Args:
        default_return: Value to return if exception occurs.
        raise_404: If True, raises 404 if result is None.

    Returns:
        Decorated function that handles SQLAlchemyError and raises HTTPException.
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
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"DB error: {str(e)}")
        return wrapper
    return decorator

import logging
from functools import wraps
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
import asyncio

logger = logging.getLogger(__name__)

def handle_exceptions(default_return=None, raise_404: bool = False):
    """
    Universal decorator to handle exceptions in DB services.

    Works with both sync and async functions.

    Args:
        default_return: Value to return if an error occurs.
        raise_404: Raise 404 if result is None.

    Returns:
        Decorated function with exception handling.
    """
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            try:
                result = await func(*args, **kwargs)
                if raise_404 and result is None:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
                return result
            except SQLAlchemyError as e:
                db = getattr(args[0], "db", None)
                if db:
                    await db.rollback()
                logger.exception("Async DB error in %s: %s", func.__name__, str(e))
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"DB error: {str(e)}")

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                if raise_404 and result is None:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
                return result
            except SQLAlchemyError as e:
                db = getattr(args[0], "db", None)
                if db:
                    db.rollback()
                logger.exception("Sync DB error in %s: %s", func.__name__, str(e))
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"DB error: {str(e)}")

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper

    return decorator

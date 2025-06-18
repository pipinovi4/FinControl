# backend/app/utils/decorators/route.py

from fastapi import HTTPException
from functools import wraps
from sqlalchemy.exc import SQLAlchemyError
import inspect
import logging

logger = logging.getLogger(__name__)


def handle_route_exceptions(default_status_code: int = 500):
    """
    Decorator to handle exceptions in FastAPI routes.

    Args:
        default_status_code (int): Status code for unexpected errors.

    Returns:
        Decorated route handler with unified error responses.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                if inspect.iscoroutinefunction(func):
                    return await func(*args, **kwargs)
                return func(*args, **kwargs)
            except HTTPException:
                raise
            except SQLAlchemyError as e:
                logger.exception("Database error in %s: %s", func.__name__, str(e))
                raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
            except Exception as e:
                logger.exception("Unhandled error in %s: %s", func.__name__, str(e))
                raise HTTPException(status_code=default_status_code, detail=f"Unexpected error: {str(e)}")
        return wrapper
    return decorator

from fastapi import HTTPException
from functools import wraps
from sqlalchemy.exc import SQLAlchemyError
from typing import Callable, Any, Awaitable
import logging
import traceback

logger = logging.getLogger(__name__)

def handle_route_exceptions(default_status_code: int = 500):
    """
    Decorator for handling unexpected errors inside FastAPI route handlers.

    Args:
        default_status_code (int): Fallback HTTP status code for unknown exceptions.

    Returns:
        Callable: A decorated async route handler with automatic error handling.
    """
    def decorator(func: Callable[..., Awaitable[Any]]):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except HTTPException:
                raise
            except SQLAlchemyError as e:
                logger.error(
                    "Database error in route '%s': %s\n%s",
                    func.__name__,
                    str(e),
                    traceback.format_exc(),
                )
                raise HTTPException(status_code=500, detail="Internal database error")
            except Exception as e:
                logger.error(
                    "Unhandled exception in route '%s': %s\n%s",
                    func.__name__,
                    str(e),
                    traceback.format_exc(),
                )
                raise HTTPException(
                    status_code=default_status_code,
                    detail="An unexpected error occurred"
                )
        return wrapper
    return decorator

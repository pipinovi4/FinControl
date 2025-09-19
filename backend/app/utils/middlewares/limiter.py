from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Request
from slowapi.errors import RateLimitExceeded
from functools import wraps

# IP-based limiter
limiter = Limiter(key_func=get_remote_address)

# Custom decorator for per-endpoint rate limits
def rate_limit(limit: str):
    """
    Decorator to apply rate limit to specific endpoint.
    Example usage:
    @rate_limit("5/minute") - Allow 5 requests per minute.
    @rate_limit("10/hour") - Allow 10 requests per hour.
    """

    # Initializing the limiter with enabled flag
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            # Apply the rate limit to the request
            # `limiter.limit` checks if the request exceeds the limit
            response = await limiter.limit(limit, request)

            # If rate limit exceeded, respond with 429
            if response.status_code == 429:
                raise RateLimitExceeded()

            return await func(request, *args, **kwargs)

        return wrapper
    return decorator

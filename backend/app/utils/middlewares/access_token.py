from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import jwt

from backend.app.core.settings import settings


class AccessTokenMiddleware(BaseHTTPMiddleware):
    """
    Middleware for validating JWT access tokens on HTTP requests.

    This middleware:
    🔹 Extracts the "Authorization: Bearer <token>" header.
    🔹 Verifies the JWT using the configured secret.
    🔹 On success, attaches the decoded payload to `request.state.user`.
    🔹 On failure, returns 401 Unauthorized with an error message.

    Usage:
        app.add_middleware(AccessTokenMiddleware)
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        # Define the paths that need authorization
        # protected_paths = ["/api/entities", "/api/analyze"]  # paths for CRUD and ANALYZE
        protected_paths = []

        # Check if the path is protected
        if any(request.url.path.startswith(path) for path in protected_paths):
            token = request.headers.get("Authorization")

            # Check format
            if token and token.startswith("Bearer "):
                try:
                    # Decode token
                    payload = jwt.decode(token[7:], settings.JWT_SECRET, algorithms=["HS256"])
                    request.state.user = payload
                except jwt.PyJWTError:
                    return Response(status_code=401, content="Invalid token")
            else:
                return Response(status_code=401, content="Missing token")

        # Continue processing the request
        return await call_next(request)

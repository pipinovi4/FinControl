# backend/app/middlewares/ws_access_token.py

from starlette.types import ASGIApp, Scope, Receive, Send
from starlette.websockets import WebSocket
import jwt

from backend.app.core.settings import settings


class WebSocketAuthMiddleware:
    """
    ASGI middleware for authenticating WebSocket connections using JWT.

    This middleware:
    🔹 Intercepts all WebSocket upgrade requests.
    🔹 Extracts and validates the "Authorization: Bearer <token>" header.
    🔹 On success, injects the decoded payload into `scope["user"]`.
    🔹 On failure, closes the WebSocket with policy violation code 4401.

    Usage:
        app.add_middleware(WebSocketAuthMiddleware)
    """

    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        # Only intercept websocket connections
        if scope["type"] == "websocket":
            headers = dict(scope.get("headers") or [])
            token = headers.get(b"authorization")

            # Check for "Bearer <token>" format
            if token and token.decode().startswith("Bearer "):
                try:
                    token_str = token.decode().split("Bearer ")[1]

                    # Decode JWT using app secret
                    payload = jwt.decode(token_str, settings.JWT_SECRET, algorithms=["HS256"])

                    # Inject decoded token payload into scope
                    scope["user"] = payload

                except jwt.PyJWTError:
                    # Invalid token — close connection
                    await WebSocket(scope, receive, send).close(code=4401)
                    return
            else:
                # Missing or malformed Authorization header
                await WebSocket(scope, receive, send).close(code=4401)
                return

        # Continue to next middleware or app
        await self.app(scope, receive, send)

# backend/app/utils/websocket.py

from functools import wraps
from fastapi import WebSocket
from fastapi.websockets import WebSocketDisconnect
import logging

logger = logging.getLogger(__name__)

def handle_ws_exceptions(func):
    """
    Decorator to gracefully handle exceptions in WebSocket endpoint handlers.

    🔹 Logs disconnect events (e.g., when the client closes the connection).
    🔹 Logs unexpected exceptions and sends an error message to the client.
    🔹 Ensures WebSocket is closed with code 1011 (Internal Error) on failure.

    Usage:
        @handle_ws_exceptions
        async def some_ws_handler(ws: WebSocket): ...

    Args:
        func: An async WebSocket handler that accepts `WebSocket` as first argument.

    Returns:
        Wrapped handler with exception safety.
    """
    @wraps(func)
    async def wrapper(websocket: WebSocket, *args, **kwargs):
        try:
            await func(websocket, *args, **kwargs)
        except WebSocketDisconnect:
            # Normal client disconnect (no need to panic)
            logger.info(f"[WS] Disconnected: {websocket.client}")
        except Exception as e:
            # Unexpected error – send to client and close
            logger.exception(f"[WS] Error: {str(e)}")
            try:
                await websocket.send_json({"error": str(e)})
            except Exception:
                pass  # If even sending the error fails — ignore
            await websocket.close(code=1011)

    return wrapper

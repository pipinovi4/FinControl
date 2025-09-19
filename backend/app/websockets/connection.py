from fastapi import WebSocket, WebSocketDisconnect
import logging
import json

logger = logging.getLogger(__name__)


class WebSocketConnection:
    """
    Robust WebSocket connection wrapper for real-time communication.
    Provides lifecycle management, JSON messaging, and graceful shutdown.
    """

    def __init__(self, websocket: WebSocket):
        self.websocket = websocket
        self.connection_id = id(self.websocket)
        self.active = False

    async def connect(self):
        try:
            await self.websocket.accept()
            self.active = True
            logger.info(f"[WS:{self.connection_id}] Connected")
        except Exception as e:
            logger.exception(f"[WS:{self.connection_id}] Connection failed: {e}")
            raise

    async def send_text(self, message: str):
        try:
            await self.websocket.send_text(message)
        except Exception as e:
            logger.exception(f"[WS:{self.connection_id}] Failed to send text: {e}")

    async def send_json(self, data: dict):
        try:
            await self.websocket.send_text(json.dumps(data))
        except Exception as e:
            logger.exception(f"[WS:{self.connection_id}] Failed to send JSON: {e}")

    async def receive_json(self) -> dict | None:
        try:
            data = await self.websocket.receive_text()
            return json.loads(data)
        except WebSocketDisconnect:
            logger.info(f"[WS:{self.connection_id}] Disconnected during receive")
            self.active = False
        except Exception as e:
            logger.exception(f"[WS:{self.connection_id}] Failed to receive JSON: {e}")
        return None

    async def close(self, code: int = 1000):
        if self.active:
            try:
                await self.websocket.close(code=code)
                logger.info(f"[WS:{self.connection_id}] Closed")
            except Exception as e:
                logger.exception(f"[WS:{self.connection_id}] Error during close: {e}")
            finally:
                self.active = False

from enum import Enum

from backend.app.schemas.auth import LoginRequest


class LoginTypes(Enum):
    BOT = "BOT"
    WEB = "WEB"

LoginRequestT = LoginRequest | None


__all__ = [
    "LoginRequestT",
    "LoginTypes",
]
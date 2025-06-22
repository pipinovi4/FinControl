from enum import Enum
from typing import Optional

from backend.app.schemas.sessions import RefreshRequest


class RefreshTypes(Enum):
    BOT = "BOT"
    WEB = "WEB"

RefreshRequestT = Optional[RefreshRequest]

__all__ = [
    "RefreshTypes",
    "RefreshRequestT",
]
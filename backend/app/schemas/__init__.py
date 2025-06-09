from backend.app.schemas.base import SchemaBase
from backend.app.schemas.sessions import RefreshToken

RefreshTokenOut = RefreshToken.out

__all__ = [
    "SchemaBase",
    "RefreshToken", "RefreshTokenOut"
]

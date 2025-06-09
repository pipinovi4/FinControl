# Namespace wrapper for accessing RefreshToken-related schemas
from .base import RefreshTokenBase
from .out import RefreshTokenOut

class RefreshToken:
    base = RefreshTokenBase
    out = RefreshTokenOut

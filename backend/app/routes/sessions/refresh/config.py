from typing import Dict, Tuple, Optional, Type
from pydantic import BaseModel

from backend.app.permissions import PermissionRole
from backend.app.schemas.sessions import RefreshRequest, TokenPair
from backend.app.routes.sessions.refresh.types import RefreshTypes

class RefreshTypesCls(BaseModel):
    web: Optional[Tuple[RefreshTypes, None, Type[BaseModel]]] = None
    bot: Optional[Tuple[RefreshTypes, Type[BaseModel], Type[BaseModel]]] = None

class RefreshWebResponse(BaseModel):
    status: int = 200

ROLE_REGISTRY: Dict[PermissionRole, Tuple[str, RefreshTypesCls]] = {
    PermissionRole.ADMIN: (
        "/admin",
        RefreshTypesCls(
            web=(RefreshTypes.WEB, None, RefreshWebResponse),
            bot=(RefreshTypes.BOT, RefreshRequest, TokenPair),
        ),
    ),
    PermissionRole.WORKER: (
        "/worker",
        RefreshTypesCls(
            web=(RefreshTypes.WEB, None, RefreshWebResponse),
            bot=(RefreshTypes.BOT, RefreshRequest, TokenPair),
        ),
    ),
    PermissionRole.BROKER: (
        "/broker",
        RefreshTypesCls(
            web=(RefreshTypes.WEB, None, RefreshWebResponse),
        ),
    ),
    PermissionRole.CLIENT: (
        "/client",
        RefreshTypesCls(
            bot=(RefreshTypes.BOT, RefreshRequest, TokenPair),
        ),
    ),
}

__all__ = [
    "ROLE_REGISTRY",
    "RefreshTypesCls",
    "RefreshWebResponse",
]

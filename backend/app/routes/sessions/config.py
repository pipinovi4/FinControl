from typing import Dict, Tuple

from backend.app.permissions import PermissionRole
from backend.app.schemas.sessions import RefreshRequest
from backend.app.routes.sessions.types import RefreshTypes, RefreshRequestT

# Define the structure for the ROLE_REGISTRY with an additional `path` field for each role.
ROLE_REGISTRY: Dict[PermissionRole, Tuple[str, Dict[RefreshTypes, RefreshRequestT]]] = {
    PermissionRole.ADMIN: (
        "/admin",  # Path for admin refresh endpoint
        {
            RefreshTypes.WEB: None,  # Tokes are inside the cookies
            RefreshTypes.BOT: RefreshRequest,  # Admin does not use bot refresh
        }
    ),
    PermissionRole.WORKER: (
        "/worker",  # Path for worker refresh endpoint
        {
            RefreshTypes.WEB: None,  # Tokes are inside the cookies
            RefreshTypes.BOT: RefreshRequest,  # Worker does not use bot refresh
        }
    ),
    PermissionRole.CLIENT: (
        "/client",  # Path for client refresh endpoint
        {
            RefreshTypes.BOT: RefreshRequest,  # Client only uses bot refresh (if implemented)
        }
    ),
    PermissionRole.BROKER: (
        "/broker",  # Path for broker refresh endpoint
        {
            RefreshTypes.WEB: None,  # Tokes are inside the cookies
        }
    ),
}

__all__ = [
    "ROLE_REGISTRY",
]

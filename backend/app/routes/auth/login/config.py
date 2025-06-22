from typing import Dict, Tuple, List

from backend.app.permissions import PermissionRole
from backend.app.routes.auth.login.types import LoginTypes


ROLE_REGISTRY: Dict[PermissionRole, Tuple[str, List[LoginTypes]]] = {
    PermissionRole.ADMIN: (
        "/admin",  # Path for admin login
        [LoginTypes.WEB, LoginTypes.BOT]
    ),
    PermissionRole.WORKER: (
        "/worker",  # Path for worker login
        [LoginTypes.WEB, LoginTypes.BOT]
    ),
    PermissionRole.CLIENT: (
        "/client",  # Path for client login
        [LoginTypes.BOT]
    ),
    PermissionRole.BROKER: (
        "/broker",  # Path for broker login
        [LoginTypes.WEB]
    ),
}

__all__ = [
    "ROLE_REGISTRY",
]
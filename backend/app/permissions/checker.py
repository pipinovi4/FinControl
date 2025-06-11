from fastapi import Depends, HTTPException, status
from backend.app.permissions.enums import PermissionRole

from backend.app.schemas.entities.User.out import UserOut

# TODO: Replace with actual implementation
# Dependency to extract current user from token or telegram ID
def get_current_user():
    pass
#     raise NotImplementedError("get_current_user will be implemented in services/auth.py")

def require_role(*roles: PermissionRole):
    """
    Dependency that restricts access to users with specified roles.

    Usage:
        @router.get("/admin-only", dependencies=[Depends(require_admin)])

    Args:
        *roles: One or more PermissionRole values that are allowed.

    Returns:
        UserOut instance if allowed, otherwise raises 403.
    """

    def wrapper(user: UserOut = Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return user

    return wrapper


# Shortcuts
require_admin = require_role(PermissionRole.ADMIN)
require_staff = require_role(
    PermissionRole.ADMIN,
    PermissionRole.BROKER,
    PermissionRole.WORKER
)
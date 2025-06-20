def create_refresh_router():
    from .refresh_router import generate_refresh_handler, refresh_router
    from backend.app.permissions import PermissionRole

    generate_refresh_handler(PermissionRole.ADMIN, "/admin")
    generate_refresh_handler(PermissionRole.WORKER, "/worker")
    generate_refresh_handler(PermissionRole.BROKER, "/broker")

    return refresh_router


__all__ = ["create_refresh_router"]
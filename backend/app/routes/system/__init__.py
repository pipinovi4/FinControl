from fastapi import APIRouter

def create_system_router() -> APIRouter:
    system_router = APIRouter()

    from .ping import router as ping
    from .routes_info import router as info
    from .status import router as status
    from .dashboard import router as dashboard

    system_router.include_router(ping)
    system_router.include_router(info)
    system_router.include_router(status)
    system_router.include_router(dashboard)

    return system_router

__all__ = ["create_system_router"]

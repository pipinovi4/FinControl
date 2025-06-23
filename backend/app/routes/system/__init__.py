from fastapi import APIRouter

def create_system_router() -> APIRouter:
    system_router = APIRouter()

    from .ping import router as ping
    from .routes_info import router as info
    from .status import router as status

    system_router.include_router(ping)
    system_router.include_router(info)
    system_router.include_router(status)

    return system_router

__all__ = ["create_system_router"]

from fastapi import APIRouter


def create_refresh_router() -> APIRouter:
    refresh_router = APIRouter()

    from .router_factory import create_refresh_routers

    for router in create_refresh_routers():
        refresh_router.include_router(router)

    return refresh_router


__all__ = ["create_refresh_router"]
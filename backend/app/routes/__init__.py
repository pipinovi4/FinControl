from fastapi import APIRouter


def create_api_router() -> APIRouter:
    from backend.app.routes.auth import create_login_router, create_register_router
    from backend.app.routes.sessions import create_refresh_router
    from backend.app.routes.crud_route import create_crud_router

    router = APIRouter(prefix="/api")

    router.include_router(create_login_router(), prefix="/auth/login", tags=["Auth"])
    router.include_router(create_register_router(), prefix="/auth/register", tags=["Auth"])
    router.include_router(create_refresh_router(), prefix="/auth/refresh", tags=["Auth"])
    router.include_router(create_crud_router(), prefix="/entities", tags=["CRUD"])

    return router

__all__ = ["create_api_router"]

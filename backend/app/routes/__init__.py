from fastapi import APIRouter


def create_api_router() -> APIRouter:
    from .auth import create_login_router, create_register_router, reset_password_router
    from .entities import create_crud_router, create_analyze_router
    from .sessions import create_refresh_router

    router = APIRouter(prefix="/api")

    # Auth endpoints
    router.include_router(create_login_router(), prefix="/auth/login", tags=["Auth"])
    router.include_router(create_register_router(), prefix="/auth/register", tags=["Auth"])
    router.include_router(create_refresh_router(), prefix="/auth/refresh", tags=["Auth"])
    router.include_router(reset_password_router, prefix="/auth/reset", tags=["Auth"])

    # Entity CRUD endpoints
    router.include_router(create_crud_router(), prefix="/entities", tags=["CRUD"])

    # Analysis endpoints
    router.include_router(create_analyze_router(), prefix="/analyze", tags=["Analyze"])

    return router


__all__ = ["create_api_router"]

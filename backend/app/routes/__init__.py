from fastapi import APIRouter

def create_api_router() -> APIRouter:
    # from backend.app.routes.entities import create_analyze_websocket_router
    from .auth import login_router, create_register_router, reset_password_router
    from .entities import create_crud_router, create_analyze_router, admin_dashboard_router, worker_dashboard_router, broker_dashboard_router
    from .sessions import create_refresh_router, logout_router
    from .system import create_system_router

    router = APIRouter(prefix="/api")


    # System endpoints
    router.include_router(create_system_router(), prefix="/system", tags=["System"])

    # Auth endpoints
    router.include_router(login_router, prefix="/auth/login", tags=["Auth"])
    router.include_router(create_register_router(), prefix="/auth/register", tags=["Auth"])
    router.include_router(reset_password_router, prefix="/auth/reset", tags=["Auth"])

    # Session endpoints
    router.include_router(create_refresh_router(), prefix="/session/refresh", tags=["Auth"])
    router.include_router(logout_router, prefix="/session/logout", tags=["Auth"])

    # Entity CRUD endpoints
    router.include_router(create_crud_router(), prefix="/entities", tags=["CRUD"])

    # Analysis endpoints
    router.include_router(create_analyze_router(), prefix="/analyze", tags=["Analyze"])

    # Dashboard endpoints
    router.include_router(admin_dashboard_router, prefix="/dashboard/admin", tags=["Admin"])
    router.include_router(worker_dashboard_router, prefix="/dashboard/worker", tags=["Admin"])
    router.include_router(broker_dashboard_router, prefix="/dashboard/broker", tags=["Admin"])

    #
    # router.include_router(create_analyze_websocket_router(), prefix="/analyze", tags=["Analyze"])

    return router


__all__ = ["create_api_router"]

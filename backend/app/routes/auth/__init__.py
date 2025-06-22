"""
Auth Route Factory

This file assembles all auth-related routes (login + register)
into the FastAPI application using reusable handler generators.

Supports:
    - Lazy imports (for performance and dependency optimization)
    - Per-role login/register paths

Exported Callables:
- create_login_router()
- create_register_router()

To mount:
    app.include_router(create_login_router(), prefix="/auth/login", tags=["Auth"])
    app.include_router(create_register_router(), prefix="/auth/register", tags=["Auth"])
"""

from backend.app.routes.auth.reset_password.reset_password_router import router as reset_password_router

from fastapi import APIRouter

def create_login_router() -> APIRouter:
    login_router = APIRouter()

    from backend.app.routes.auth.login.router_factory import create_login_routers

    for router in create_login_routers():
        login_router.include_router(router)

    return login_router


def create_register_router() -> APIRouter:
    register_router = APIRouter()

    from backend.app.routes.auth.register.router_factory import create_register_routers

    for router in create_register_routers():
        register_router.include_router(router)

    return register_router

# Explicit module exports
__all__ = [
    "create_login_router",
    "create_register_router",
    "reset_password_router"
]

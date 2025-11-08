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

from .reset_password.reset_password_router import router as reset_password_router
from .login import login_router
from .register import register_invite_router

from fastapi import APIRouter



def create_register_router() -> APIRouter:
    register_router = APIRouter()

    from app.routes.auth.register.router_factory import create_register_routers

    for router in create_register_routers():
        register_router.include_router(router)

    return register_router

# Explicit module exports
__all__ = [
    "login_router",
    "create_register_router",
    "reset_password_router",
    "register_invite_router"
]

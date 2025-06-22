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
    refresh_router = APIRouter()

    from backend.app.routes.auth.login.router_factory import create_login_routers

    for router in create_login_routers():
        refresh_router.include_router(router)

    return refresh_router


__all__ = ["create_login_router"]

def create_register_router():
    # Lazy import to avoid unnecessary module loading and circular deps
    from backend.app.routes.auth.register.register_router import generate_register_handler, register_router

    # Import all services and schemas needed for each role registration
    from backend.app.services.entities import (
        AdminService, WorkerService, ClientService, BrokerService,
    )
    from backend.app.schemas.entities.admin_schema import AdminSchema
    from backend.app.schemas.entities.worker_schema import WorkerSchema
    from backend.app.schemas.entities.client_schema import ClientSchema
    from backend.app.schemas.entities.broker_schema import BrokerSchema

    # Define registration routes:
    # - Path (string)
    # - Corresponding service class (to create user)
    # - Pydantic schema used for input validation
    # - Method name inside the service to call (e.g., register_admin)
    register_definitions = [
        ("/admin", AdminService, AdminSchema.Create, "register_admin"),
        ("/worker", WorkerService, WorkerSchema.Create, "register_worker"),
        ("/broker", BrokerService, BrokerSchema.Create, "register_broker"),
        ("/client", ClientService, ClientSchema.Create, "register_client"),
    ]

    # Generate each handler dynamically using the definitions
    for path, service, schema, method_name in register_definitions:
        generate_register_handler(path, service, schema, method_name)

    # Return router with all registered registration endpoints
    return register_router

# Explicit module exports
__all__ = [
    "create_login_router",
    "create_register_router",
    "reset_password_router"
]

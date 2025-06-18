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

def create_login_router():
    # Lazy import to prevent circular dependencies and reduce startup overhead
    from .login_router import generate_login_handler, login_router
    from backend.app.permissions import PermissionRole

    # Define login endpoints per role and URL path
    login_definitions = [
        (PermissionRole.ADMIN, "/admin"),
        (PermissionRole.WORKER, "/worker"),
        (PermissionRole.BROKER, "/broker"),
        (PermissionRole.CLIENT, "/client"),
    ]

    # Dynamically generate handlers for each role-path pair
    for role, path in login_definitions:
        generate_login_handler(role, path)

    # Return router with all registered login endpoints
    return login_router


def create_register_router():
    # Lazy import to avoid unnecessary module loading and circular deps
    from .register_router import generate_register_handler, register_router

    # Import all services and schemas needed for each role registration
    from backend.app.services.entities import (
        AdminService, WorkerService, ClientServices, BrokerService,
    )
    from backend.app.schemas.entities.Admin import AdminSchema
    from backend.app.schemas.entities.Worker import WorkerSchema
    from backend.app.schemas.entities.Client import ClientSchema
    from backend.app.schemas.entities.Broker import BrokerSchema

    # Define registration routes:
    # - Path (string)
    # - Corresponding service class (to create user)
    # - Pydantic schema used for input validation
    # - Method name inside the service to call (e.g., register_admin)
    register_definitions = [
        ("/admin", AdminService, AdminSchema.Create, "register_admin"),
        ("/worker", WorkerService, WorkerSchema.Create, "register_worker"),
        ("/broker", BrokerService, BrokerSchema.Create, "register_broker"),
        ("/client", ClientServices, ClientSchema.Create, "register_client"),
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
]

"""
CRUD Route Factory

This file assembles all entity-related CRUD routes (create, read, update, delete)
into a single unified FastAPI router using reusable factory functions.

Supports:
    - Lazy imports (prevents circular dependencies and improves startup time)
    - Per-role, per-action endpoints
    - Unified mounting interface for all entity endpoints

Exported Callable:
- create_crud_router()

To mount:
    app.include_router(create_crud_router(), prefix="/entities", tags=["Entities"])
"""

from fastapi import APIRouter

def create_crud_router() -> APIRouter:
    # Main router for all entity-related operations
    crud_router = APIRouter(tags=["Entities"])

    # Lazy import to avoid circular deps and unused modules
    from .router_factories import create_router_factory, read_router_factory, update_router_factory, delete_router_factory

    # Attach each action-specific router
    crud_router.include_router(create_router_factory())
    crud_router.include_router(read_router_factory())
    crud_router.include_router(update_router_factory())
    crud_router.include_router(delete_router_factory())

    return crud_router


__all__ = [
    "create_crud_router",
]

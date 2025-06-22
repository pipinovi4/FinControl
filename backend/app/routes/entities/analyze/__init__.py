"""
Analyze Route Factory

This file assembles all analyze-related routes (per-role, per-type metrics)
into a unified FastAPI router using reusable route generators.

Supports:
    - Role-specific, type-mapped endpoints
    - Lazy imports to reduce startup overhead
    - Clean export of `create_analyze_router()` for routing

Exported Callable:
- create_analyze_router()

To mount:
    app.include_router(create_analyze_router(), prefix="/analyze", tags=["Analyze"])
"""

from fastapi import APIRouter

def create_analyze_router() -> APIRouter:
    # Main router for all analyze endpoints
    analyze_router = APIRouter()

    # Lazy import to avoid circular dependencies
    from .router_factory import create_analyze_routers

    # Attach all analysis routes
    for router in create_analyze_routers():
        analyze_router.include_router(router)

    return analyze_router


__all__ = [
    "create_analyze_router",
]

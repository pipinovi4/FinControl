"""
Analyze Route Factory

This file assembles all analyze-related routes (per-role, per-type metrics)
into a unified FastAPI router using reusable route generators.

Supports:
    - Role-specific, type-mapped endpoints
    - WebSocket-based real-time metrics
    - Lazy imports to reduce startup overhead
    - Clean export of `create_analyze_router()` and `create_analyze_websocket_router()`

Exported Callables:
- create_analyze_router()
- create_analyze_websocket_router()

To mount:
    app.include_router(create_analyze_router(), prefix="/analyze", tags=["Analyze"])
    app.include_router(create_analyze_websocket_router(), tags=["Analyze 🔌"])
"""

from fastapi import APIRouter

def create_analyze_router() -> APIRouter:
    """Main router for all GET-based analyze endpoints."""
    analyze_router = APIRouter()

    # Lazy import to avoid circular dependencies
    from .router_factory import create_analyze_routers

    for router in create_analyze_routers():
        analyze_router.include_router(router)

    return analyze_router


def create_analyze_websocket_router() -> APIRouter:
    """Main router for all WebSocket-based analyze endpoints."""
    ws_router = APIRouter()

    # Lazy import to avoid circular dependencies
    from .websocket_factory import create_analyze_ws_routers

    for router in create_analyze_ws_routers():
        ws_router.include_router(router)

    return ws_router


__all__ = [
    "create_analyze_router",
    "create_analyze_websocket_router",
]

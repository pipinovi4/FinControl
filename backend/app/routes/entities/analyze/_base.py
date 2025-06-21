# routes/entities/analyze/_base.py
"""
Reusable helper to attach analysis endpoints for different user roles.
Each route is registered under:    /<role>/analyze

Keeps FastAPI-specific glue (path, tags, wrapper) out of the factories.
"""

from typing import Awaitable, Callable
from fastapi import APIRouter

from backend.app.utils.decorators import handle_route_exceptions


# ─────────────────────────────────────────────────────────────
# Wrapper for analysis endpoints (always GET, nobody expected)
# ─────────────────────────────────────────────────────────────
def generate_analyze_endpoints(
    router: APIRouter,
    *,
    path: str,  # e.g. "clients_growth"
    handler: Callable[..., Awaitable],
    tags: list[str],
    wrapper: Callable[[Callable[..., Awaitable]], Callable[..., Awaitable]] = handle_route_exceptions,
) -> None:
    """
    Attach a GET endpoint at `/<role>/analyze/<path>` to a router.

    Args:
        router:  APIRouter instance scoped to a specific role
        path:    URL subpath (relative to /analyze/) for the metric
        handler: Coroutine handling the analysis logic
        tags:    Tags for Swagger UI grouping
        wrapper: Optional decorator for error handling/logging (default enabled)
    """
    route_path = f"/analyze/{path}"
    router.get(route_path, tags=tags)(wrapper(handler))

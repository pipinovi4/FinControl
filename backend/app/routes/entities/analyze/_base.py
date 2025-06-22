from typing import Awaitable, Callable
from fastapi import APIRouter
from backend.app.utils.decorators import handle_route_exceptions
from backend.app.utils.middlewares.limiter import rate_limit

def generate_analyze_endpoints(
    router: APIRouter,
    *,
    path: str,  # e.g. "clients_growth"
    handler: Callable[..., Awaitable],
    tags: list[str],
    wrapper: Callable[[Callable[..., Awaitable]], Callable[..., Awaitable]] = handle_route_exceptions,
    name: str = __name__,
    rate_limit_rule: str | None = None
) -> None:
    """
    Attach a GET endpoint at `/<role>/analyze/<path>` to a router.

    Args:
        router:  APIRouter instance scoped to a specific role
        path:    URL subpath (relative to /analyze/) for the metric
        handler: Coroutine handling the analysis logic
        tags:    Tags for Swagger UI grouping
        wrapper: Optional decorator for error handling/logging (default enabled)
        name: Optional name for the route
        rate_limit_rule: A string representing the rate limit rule (e.g., "5/minute").
    """
    if rate_limit_rule:
        handler = rate_limit(rate_limit_rule)(handler)

    router.get(
        path=path,
        tags=tags,
        name=name,
        summary=f"{tags[0]} - {path.replace('_', ' ').title()}"
    )(wrapper(handler))

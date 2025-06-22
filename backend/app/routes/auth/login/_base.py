from typing import Awaitable, Callable
from fastapi import APIRouter
from backend.app.utils.decorators import handle_route_exceptions
from backend.app.utils.middlewares.limiter import rate_limit

def generate_login_endpoints(
    router: APIRouter,
    *,
    path: str,
    handler: Callable[..., Awaitable],
    tags: list[str],
    wrapper: Callable[[Callable[..., Awaitable]], Callable[..., Awaitable]] = handle_route_exceptions,
    name: str = __name__,
    rate_limit_rule: str | None = None,
) -> None:
    if rate_limit_rule:
        handler = rate_limit(rate_limit_rule)(handler)

    router.get(
        path=path,
        tags=tags,
        name=name,
        summary=f"{tags[0]} - {path.replace('_', ' ').title()}"
    )(wrapper(handler))
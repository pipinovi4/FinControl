from typing import Awaitable, Callable, TypeVar
from fastapi import APIRouter

from backend.app.schemas import AdminSchema, WorkerSchema, BrokerSchema, ClientSchema
from backend.app.schemas.auth import LoginRequest
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

    wrapped = wrapper(handler)
    wrapped._meta = {"input_schema": LoginRequest}

    router.get(
        path=path,
        tags=tags,
        name=name,
        summary=f"{tags[0]} - {path.replace('_', ' ').title()}"
    )(wrapped)
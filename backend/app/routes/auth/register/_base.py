from typing import Awaitable, Callable, TypeVar
from fastapi import APIRouter

from backend.app.schemas import AdminSchema, WorkerSchema, BrokerSchema, ClientSchema
from backend.app.utils.decorators import handle_route_exceptions
from backend.app.utils.middlewares.limiter import rate_limit


SchemaT = TypeVar("SchemaT", AdminSchema, WorkerSchema, BrokerSchema, ClientSchema)

def generate_register_endpoints(
    router: APIRouter,
    *,
    path: str,
    handler: Callable[..., Awaitable],
    tags: list[str],
    wrapper: Callable[[Callable[..., Awaitable]], Callable[..., Awaitable]] = handle_route_exceptions,
    schema: SchemaT,
    name: str = __name__,
    rate_limit_rule: str | None = None,
) -> None:
    if rate_limit_rule:
        handler = rate_limit(rate_limit_rule)(handler)

    wrapped = wrapper(handler)
    wrapped._meta = {"input_schema": schema.Create}

    router.post(
        path=path,
        tags=tags,
        name=name,
        summary=f"{tags[0]} - {path.replace('_', ' ').title()}",
        # response_model=schema.Create,
    )(wrapped)
from typing import Awaitable, Callable, TypeVar, Type
from pydantic import BaseModel
from fastapi import APIRouter

from app.utils.decorators import handle_route_exceptions
from app.utils.middlewares.limiter import rate_limit

InputSchemaT = TypeVar("InputSchemaT", bound=BaseModel)
OutputSchemaT = TypeVar("OutputSchemaT", bound=BaseModel)

def generate_login_endpoints(
    router: APIRouter,
    *,
    path: str,
    handler: Callable[..., Awaitable],
    tags: list[str],
    wrapper: Callable[[Callable[..., Awaitable]], Callable[..., Awaitable]] = handle_route_exceptions(default_status_code=500),
    input_model: Type[InputSchemaT],
    response_model: Type[OutputSchemaT],
    name: str = __name__,
    rate_limit_rule: str | None = None,
) -> None:
    # if rate_limit_rule:
    #     handler = rate_limit(rate_limit_rule)(handler)

    wrapped = wrapper(handler)
    wrapped._meta = {"input_schema": input_model}

    router.post(
        path=path,
        tags=tags,
        name=name,
        response_model=response_model,
        summary=f"{tags[0]} - {path.replace('_', ' ').title()}"
    )(wrapped)
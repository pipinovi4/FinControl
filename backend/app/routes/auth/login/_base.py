from typing import Awaitable, Callable, TypeVar, Type
from fastapi import APIRouter
from pydantic import BaseModel

from app.utils.decorators import handle_route_exceptions

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
    name: str,
) -> None:

    wrapped = wrapper(handler)
    wrapped._meta = {"input_schema": input_model}

    router.post(
        path,
        tags=tags,
        name=name,
        response_model=response_model,
        summary=f"Login — {tags[0]}"
    )(wrapped)

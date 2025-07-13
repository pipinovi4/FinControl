from inspect import signature
from typing import Awaitable, Callable, TypeVar, Type, List, Tuple, get_type_hints, Any
from fastapi import APIRouter
from pydantic import BaseModel

from backend.app.schemas.sessions import TokenPair
from backend.app.utils.decorators import handle_route_exceptions
# from backend.app.utils.middlewares.limiter import rate_limit
from backend.app.schemas import AdminSchema, WorkerSchema, BrokerSchema, ClientSchema

# Type variables for generic schemas and services
SchemaT = TypeVar("SchemaT", AdminSchema, WorkerSchema, BrokerSchema, ClientSchema)

InputSchemaT = TypeVar("InputSchemaT", bound=BaseModel)
OutputSchemaT = TypeVar("OutputSchemaT", bound=BaseModel)


def generate_register_endpoints(
    router: APIRouter,
    *,
    path: str,
    handler: Callable[..., Awaitable],
    tags: list[str],
    input_model: Type[InputSchemaT],
    response_model: Type[OutputSchemaT],
    schema_cls: Type[SchemaT],
    wrapper: Callable[[Callable[..., Awaitable]], Callable[..., Awaitable]] = handle_route_exceptions(default_status_code=500),
    name: str = __name__,
    rate_limit_rule: str | None = None,
) -> None:
    # if rate_limit_rule:
    #     handler = rate_limit(rate_limit_rule)(handler)

    # Attach schema metadata for possible route introspection
    handler._meta = {
        "input_schema": input_model,
        "output_schema": response_model,
    }

    wrapped = wrapper(handler)

    router.post(
        path=path,
        tags=tags,
        name=name,
        summary=f"{tags[0]} - {path.replace('_', ' ').title()}",
        response_model=response_model,
    )(wrapped)


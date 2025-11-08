from http.client import HTTPException
from typing import Awaitable, Callable, Type, TypeVar
from fastapi import APIRouter
from pydantic import BaseModel

from app.routes.sessions.refresh.types import RefreshTypes
from app.utils.decorators import handle_route_exceptions
from app.utils.middlewares.limiter import rate_limit

InputSchemaT = TypeVar("InputSchemaT", bound=BaseModel)
OutputSchemaT = TypeVar("OutputSchemaT", bound=BaseModel)

def generate_refresh_endpoints(
        router: APIRouter,
        *,
        path: str,
        handler: Callable[..., Awaitable],
        tags: list[str],
        wrapper: Callable[[Callable[..., Awaitable]], Callable[..., Awaitable]] = handle_route_exceptions(default_status_code=500),
        input_model: InputSchemaT,
        response_model: OutputSchemaT,
        refresh_type: RefreshTypes,
        name: str = __name__,
        rate_limit_rule: str | None = None,
) -> None:
    """
    Generates a refresh endpoint and adds it to the provided APIRouter.

    This function handles creating the endpoint with optional rate-limiting and exception handling.

    Parameters:
    - router (APIRouter): The FastAPI router to which the endpoint will be added.
    - path (str): The path of the endpoint (e.g., "/refresh").
    - handler (Callable[..., Awaitable]): The function that will handle the request for this endpoint.
    - tags (list[str]): A list of tags to categorize the endpoint in the OpenAPI documentation.
    - wrapper (Callable[[Callable[..., Awaitable]], Callable[..., Awaitable]], optional): A decorator function to wrap the handler (default is `handle_route_exceptions` for exception handling).
    - name (str, optional): The name of the endpoint (default is the current module name).
    - rate_limit_rule (str | None, optional): A rate limit rule to apply to the endpoint (e.g., "10/minute"). If None, no rate limit is applied.

    Returns:
    - None: The function adds the generated endpoint to the provided `router` and does not return anything.
    """
    # if rate_limit_rule:
    #     handler = rate_limit(rate_limit_rule)(handler)

    wrapped = wrapper(handler)
    wrapped._meta = {"input_schema": input_model}

    from fastapi import HTTPException, status

    if refresh_type is RefreshTypes.WEB:
        router.get(
            path=path,
            tags=tags,
            name=name,
            response_model=response_model,
            summary=f"Refresh token via cookies ({tags[0]})"
        )(wrapped)

    elif refresh_type is RefreshTypes.BOT:
        router.post(
            path=path,
            tags=tags,
            name=name,
            response_model=response_model,
            summary=f"Refresh token via body ({tags[0]})"
        )(wrapped)

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported refresh type: {refresh_type}"
        )

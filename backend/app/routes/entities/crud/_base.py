# routes/entities/_base.py
"""
Reusable helper that attaches a single HTTP route to a FastAPI `APIRouter`.

Keeps all FastAPI-specific glue (HTTP verb, path, tags) in **one place** so that
per-action router factories (`create_router_factory.py`, `read_router_factory.py`, …)
remain tiny and role-agnostic.
"""

from typing import Awaitable, Callable, Type
from fastapi import APIRouter

from backend.app.utils.decorators import handle_route_exceptions
from backend.app.utils.middlewares import rate_limit

# Thin wrapper around `router.<verb>()`                                    #
def generate_crud_endpoints(
    router: APIRouter,
    *,
    verb: str,
    path: str,
    handler: Callable[..., Awaitable],   # actual coroutine executed per request
    tags: list[str],
    wrapper: Callable[[Callable[..., Awaitable]], Callable[..., Awaitable]] = handle_route_exceptions,
    rate_limit_rule: str | None = None,  # Add rate limit rule
    name: str = __name__,
) -> None:
    """
     Attach `handler` to `router` with the given HTTP `verb` and `path`.

     Args:
         router:    Target `APIRouter` instance.
         verb:      HTTP method name in lowercase (e.g. `"post"`, `"get"`).
         path:      Sub-path relative to the router’s prefix (e.g. `"/admin"`).
         handler:   Async function that implements business logic.
         tags:      List of OpenAPI tags – used for grouping in Swagger UI.
         wrapper:
                Decorator applied to the `handler` function before attaching.
                Used for centralized error handling, logging, etc.
                Defaults to `handle_route_exceptions`.
         rate_limit_rule: Rate limit rule.
         name:      Name of route handler.

     Example:
         generate_crud_endpoints(
             router=my_router,
             verb="post",
             path="/admin",
             handler=create_admin,
             input_schema=AdminSchema.Create,
             tags=["Admin-CREATE"],
         )
     """
    # `getattr` maps the string verb to the corresponding decorator
    fastapi_decorator = getattr(router, verb)

    # Apply rate limit if provided
    if rate_limit_rule:
        handler = rate_limit(rate_limit_rule)(handler)

    # FastAPI automatically extracts the schema from the handler signature,
    # so we don’t need to pass `input_schema` to the decorator explicitly.
    # The presence of `input_schema` is still useful for static analysis and
    # for factories that might want to branch on “body vs. no-body”.
    fastapi_decorator(path, tags=tags, name=name, summary=f"{tags[0]} - {path.replace('_', ' ').title()}")(wrapper(handler))

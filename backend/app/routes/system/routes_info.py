from fastapi import APIRouter, Request
from fastapi.routing import APIRoute

router = APIRouter()

@router.get("/routes-info", tags=["System"])
def get_routes_info(request: Request):
    """
    Returns metadata about all registered HTTP endpoints.

    🔹 No circular import — uses request.app reference
    🔹 Useful for frontend introspection or debugging
    """
    app = request.app
    endpoints = []

    for route in app.routes:
        if isinstance(route, APIRoute):
            endpoints.append({
                "path": route.path,
                "methods": list(route.methods),
                "name": route.name,
                "summary": route.summary,
                "tags": route.tags,
                "endpoint": route.endpoint.__name__,
            })

    return {"endpoints": endpoints}

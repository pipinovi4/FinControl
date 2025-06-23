from .crud import create_crud_router
from .analyze import create_analyze_router # create_analyze_websocket_router

__all__ = [
    "create_crud_router",
    "create_analyze_router",
    # "create_analyze_websocket_router"
]
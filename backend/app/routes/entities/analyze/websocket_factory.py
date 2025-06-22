# backend/app/routes/entities/analyze/websocket_factory.py

from __future__ import annotations

from typing import Awaitable, Callable, Any, List
from fastapi import APIRouter, WebSocket, Depends, WebSocketException, status
from fastapi.websockets import WebSocketDisconnect

from backend.db.session import get_async_db
from backend.app.routes.entities.analyze.types import AnalyzeType
from backend.app.routes.entities.analyze.config import ROLE_REGISTRY
from backend.app.utils.protocols import BaseService
from backend.app.utils.wrappers import RoleServiceWrapper
from backend.app.permissions import PermissionRole
from backend.app.websockets import WebSocketConnection


def make_analyze_websocket_handler(
    *,
    service_cls: RoleServiceWrapper[BaseService],
    interface_cls: RoleServiceWrapper[BaseService],
    filter_cls: RoleServiceWrapper[BaseService],
    role: PermissionRole,
    metric: AnalyzeType,
) -> Callable[[WebSocket], Awaitable[None]]:
    """
    Returns a WebSocket handler for a given role and analysis metric.

    This handler:
    🔹 Resolves the service, interface, and filter classes for the role.
    🔹 Executes the metric logic using `run_<metric>` method from the service.
    🔹 Applies optional filters (can be extended via receive_json).
    🔹 Sends JSON response with the result back through WebSocket.
    """
    async def _handler(websocket: WebSocket, db=Depends(get_async_db)) -> None:
        connection = WebSocketConnection(websocket)
        await connection.connect()

        try:
            # Resolve service dependencies
            service = service_cls.resolve()
            interface = interface_cls.resolve()
            flt = filter_cls.resolve()

            # Build query and apply filters
            base_query = await service.get_query(db)
            flt_instance = flt(base_query)
            # (Optional) add support for dynamic filters via `receive_json`
            query = await flt_instance.apply()

            # Find and run appropriate method (e.g. run_clients_growth)
            method_name = f"run_{metric.value}"
            if not hasattr(service, method_name):
                raise WebSocketException(code=status.WS_1011_INTERNAL_ERROR)

            run_metric = getattr(service, method_name)
            raw_result = await run_metric(query)

            # Convert result to DTO (if supported)
            result = (
                await interface.to_dto(metric, raw_result)
                if hasattr(interface, "to_dto")
                else raw_result
            )

            # Send result to frontend
            await connection.send_json({"metric": metric.value, "data": result})
        except WebSocketDisconnect:
            # Graceful disconnect
            pass
        except Exception as e:
            # Any unexpected error during processing
            await connection.send_json({"error": str(e)})
        finally:
            await connection.close()

    _handler.__name__ = f"analyze_{role.value.lower()}_{metric.value}_ws"
    return _handler


def create_analyze_ws_routers() -> List[APIRouter]:
    """
    Generates all role-prefixed routers for analysis WebSocket endpoints.

    Each role gets its own router at:
        🔸 /<role>/ws/analyze/<metric>

    Example:
        /admin/ws/analyze/clients_growth
        /worker/ws/analyze/revenue_per_day
    """
    routers: List[APIRouter] = []

    for role, bundle in ROLE_REGISTRY.items():
        router = APIRouter(prefix=f"{bundle.prefix}/ws/analyze")

        for metric in AnalyzeType:
            ws_handler = make_analyze_websocket_handler(
                service_cls=bundle.service,
                interface_cls=bundle.interface,
                filter_cls=bundle.filter,
                role=role,
                metric=metric,
            )

            router.websocket(f"/{metric.value}")(ws_handler)

        routers.append(router)

    return routers

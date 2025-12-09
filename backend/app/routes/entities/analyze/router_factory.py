# routes/entities/analyze/factory.py
"""Factory that builds role‑scoped **/analyze** routers.

🔹 Each router lives under its role prefix (``/admin``, ``/worker`` …).
🔹 Every analysis metric (listed in ``AnalyzeType``) is exposed as
   ``GET /<role>/analyze/<metric>``.
🔹 The heavy lifting (filters → query → DTO) is done by a dynamic
   ``make_analyze_handler`` so we don’t duplicate code per role/metric.
"""

from __future__ import annotations

from typing import Awaitable, Callable, Any, List
from fastapi import APIRouter, HTTPException, Request, Depends

from db.session import get_async_db
from app.routes.entities.analyze._base import generate_analyze_endpoints
from app.routes.entities.analyze.types import AnalyzeType
from app.routes.entities.analyze.config import ROLE_REGISTRY
from app.permissions import PermissionRole
from app.utils.protocols import BaseService
from app.utils.wrappers import RoleServiceWrapper

def make_analyze_handler(
    *,
    service_cls: RoleServiceWrapper[BaseService],
    interface_cls: RoleServiceWrapper[BaseService],
    filter_cls: RoleServiceWrapper[BaseService],
    role: PermissionRole,
    metric: AnalyzeType,
) -> Callable[[Request], Awaitable[Any]]:
    """
    Returns an async FastAPI handler bound to one role + metric.
    """

    async def _handler(
        request: Request,
        db=Depends(get_async_db),
    ) -> Any:
        service = service_cls.resolve()
        interface = interface_cls.resolve()
        flt = filter_cls.resolve()

        try:
            base_query = await service.get_query(db)
        except AttributeError as exc:
            raise HTTPException(500, detail="Service lacks .get_query(db) method") from exc

        flt_instance = flt(base_query)

        for key, value in request.query_params.multi_items():
            if hasattr(flt_instance, key):
                await getattr(flt_instance, key)(value)
            else:
                raise HTTPException(400, detail=f"Unsupported filter '{key}' for role {role.value}")

        query = await flt_instance.apply()

        method_name = f"run_{metric.value}"
        if not hasattr(service, method_name):
            raise HTTPException(501, detail=f"Metric '{metric.value}' not implemented for role {role.value}")

        run_metric = getattr(service, method_name)
        raw_result = await run_metric(query)

        if hasattr(interface, "to_dto"):
            return await interface.to_dto(metric, raw_result)
        return raw_result

    _handler.__name__ = f"analyze_{role.value.lower()}_{metric.value}"
    return _handler

def create_analyze_routers() -> List[APIRouter]:
    routers = []

    for role, bundle in ROLE_REGISTRY.items():
        router = APIRouter(prefix=bundle.prefix + "/analyze")

        for metric in AnalyzeType:
            handler = make_analyze_handler(
                service_cls=bundle.service,
                interface_cls=bundle.interface,
                filter_cls=bundle.filter,
                role=role,
                metric=metric,
            )
            generate_analyze_endpoints(
                router=router,
                path=metric.value,
                handler=handler,
                tags=[role.value],
                rate_limit_rule="20/minute",
                name=handler.__name__,
            )

        routers.append(router)

    return routers

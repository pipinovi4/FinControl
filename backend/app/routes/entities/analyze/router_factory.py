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

from backend.app.db.session import get_db  # type: ignore  # ↲ adjust if your import differs
from backend.app.routes.entities.analyze._base import generate_analyze_endpoints
from backend.app.routes.entities.analyze.types import AnalyzeType
from backend.app.routes.entities.analyze.config import ROLE_REGISTRY
from backend.app.permissions import PermissionRole
from backend.app.utils.protocols import BaseService
from backend.app.utils.wrappers import RoleServiceWrapper

# ─────────────────────────────────────────────────────────────
# Dynamic handler factory
# ─────────────────────────────────────────────────────────────

def make_analyze_handler(
    *,
    service_cls: RoleServiceWrapper[BaseService],
    interface_cls: RoleServiceWrapper[BaseService],
    filter_cls: RoleServiceWrapper[BaseService],
    role: PermissionRole,
    metric: AnalyzeType,
) -> Callable[[Request], Awaitable[Any]]:
    """Return an async FastAPI handler bound to *one* role + metric.

    Flow:
        1. Read query params ⇒ map to FilterService.
        2. filters.apply() ⇒ SQLAlchemy query.
        3. Delegate to Service.run_<metric>().
        4. Map result via Interface.to_dto().
    """

    async def _handler(
        request: Request,
        db=Depends(get_db),
    ) -> Any:
        service = service_cls.resolve()
        interface = interface_cls.resolve()
        flt = filter_cls.resolve()

        try:
            base_query = db.query(service.model)  # type: ignore[attr-defined]
        except AttributeError as exc:
            raise HTTPException(500, detail="Service lacks .model attribute") from exc

        flt_instance = flt(base_query)  # type: ignore[call-arg]

        for key, value in request.query_params.multi_items():
            if hasattr(flt_instance, key):
                getattr(flt_instance, key)(value)
            else:
                raise HTTPException(400, detail=f"Unsupported filter '{key}' for role {role.value}")

        query = flt_instance.apply()

        method_name = f"run_{metric.value}"
        if not hasattr(service, method_name):
            raise HTTPException(501, detail=f"Metric '{metric.value}' not implemented for role {role.value}")

        raw_result = getattr(service, method_name)(query)  # type: ignore[attr-defined]

        if hasattr(interface, "to_dto"):
            return interface.to_dto(metric, raw_result)  # type: ignore[attr-defined]
        return raw_result

    _handler.__name__ = f"analyze_{role.value.lower()}_{metric.value}"
    return _handler


# ─────────────────────────────────────────────────────────────
# Router factory exposed to app
# ─────────────────────────────────────────────────────────────

def create_analyze_routers() -> List[APIRouter]:
    routers: List[APIRouter] = []

    for role, bundle in ROLE_REGISTRY.items():
        router = APIRouter(prefix=bundle.prefix, tags=[f"{role.value}-ANALYZE"])

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
                tags=[f"{role.value}-ANALYZE"],
            )

        routers.append(router)

    return routers

"""
roles.registry
==============

Central place where we bind every user-role to its own *service bundle*.
Each bundle contains:

    * URL prefix                – e.g. "/admin"
    * business-service          – CRUD / domain logic
    * interface service         – UI-specific helpers or DTO mappers
    * filter service            – role-specific query rules
    * util   service            – light, ad-hoc helpers
    * Pydantic schema class     – object returned to the client layer

**Why do we wrap classes with `RoleServiceWrapper`?**

`AdminService`, `BrokerService`, etc. all inherit from a “god-mode”
`UserService` that contains *privileged* methods.
`RoleServiceWrapper` is a runtime proxy that exposes **only** methods
declared directly on the concrete class, blocking everything inherited.
This guarantees that a route written for a restricted role can never
accidentally call a super-admin helper.

You can import a ready bundle like so:

    from app.utils.roles.registry import ROLE_REGISTRY, PermissionRole

    admin = ROLE_REGISTRY[PermissionRole.ADMIN]
    result = admin.service.get_summary(...)

Adding a new role → just append one tuple to `_RAW`.
"""

from __future__ import annotations

from typing import Dict, Type
from pydantic import BaseModel

from app.permissions import PermissionRole
from app.schemas.entities.filters import (
    WorkerFilterSchema, BrokerFilterSchema, AdminFilterSchema,
)
from app.services.entities import (
    AdminService, WorkerService, BrokerService,
    AdminInterfaceService, WorkerInterfaceService,
    BrokerInterfaceService, BrokerFilterService,
    AdminFilterService,  WorkerFilterService,
)
from app.utils.protocols import BaseService
from app.utils.wrappers import RoleServiceWrapper
from app.utils.types import RoleBundle
from app.routes.entities.analyze.types import RawTuple


_RAW: Dict[PermissionRole, RawTuple] = {
    PermissionRole.ADMIN: (
        "/admin",
        AdminService,  AdminInterfaceService,
        AdminFilterService,
        AdminFilterSchema,
    ),
    PermissionRole.WORKER: (
        "/worker",
        WorkerService, WorkerInterfaceService,
        WorkerFilterService,
        WorkerFilterSchema,
    ),
    PermissionRole.BROKER: (
        "/broker",
        BrokerService, BrokerInterfaceService,
        BrokerFilterService,
        BrokerFilterSchema,
    ),
}

# ──────────────────────────────────────────────────────────────────
# Registry: classes are wrapped → RoleBundle is created
# ──────────────────────────────────────────────────────────────────
def _build_bundle(
    prefix: str,
    svc_cls:   Type[BaseService],
    ui_cls:    Type[BaseService],
    flt_cls:   Type[BaseService],
    schema_cls: Type[BaseModel],
) -> RoleBundle:
    """Wrap every class in RoleServiceWrapper and pack into RoleBundle."""
    return RoleBundle(
        prefix=prefix,
        service=RoleServiceWrapper(svc_cls),
        interface=RoleServiceWrapper(ui_cls),
        filter=RoleServiceWrapper(flt_cls),
        schema=schema_cls.Out,
    )


ROLE_REGISTRY: Dict[PermissionRole, RoleBundle] = {
    role: _build_bundle(*raw_tuple)
    for role, raw_tuple in _RAW.items()
}

__all__ = [
    "ROLE_REGISTRY"
]
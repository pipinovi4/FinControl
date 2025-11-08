from dataclasses import dataclass
from typing import Type
from pydantic import BaseModel

from app.utils.protocols.base_service import BaseService
from app.utils.wrappers.role_service_wrapper import RoleServiceWrapper

# ───────────────────────────────────────────────────────────────
# Final assembled container per role — used in ROLE_REGISTRY
# ───────────────────────────────────────────────────────────────
@dataclass(frozen=True)
class RoleBundle:
    prefix:    str
    service:   RoleServiceWrapper[BaseService]
    interface: RoleServiceWrapper[BaseService]
    filter:    RoleServiceWrapper[BaseService]
    schema:    Type[BaseModel]

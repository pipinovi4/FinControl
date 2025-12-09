from typing import Type, Protocol
from pydantic import BaseModel

# ─────────────────────────────────────────────────────────────
# Interface (Protocol) for schema namespace containers
#
# Each user-role schema (e.g. AdminSchema, BrokerSchema, ...)
# is expected to group related Pydantic models under named
# attributes — one for each standard operation (CRUD).
#
# This protocol ensures consistent access and IDE support
# for dynamic schema selection (e.g. schema_cls.Create).
# ─────────────────────────────────────────────────────────────

class BaseSchemaNamespace(Protocol):
    Create: Type[BaseModel]   # Used for incoming POST payloads
    Out:    Type[BaseModel]   # Returned to application in responses
    Update: Type[BaseModel]   # Used for PATCH/PUT payloads
    Base:   Type[BaseModel]   # Shared attributes or filters

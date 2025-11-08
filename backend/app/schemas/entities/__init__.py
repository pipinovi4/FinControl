"""
Entity schemas package initializer.

This module re-exports the core Pydantic schemas for each user role/entity in the system.
Use it to import all entity-level schemas from a single access point.
"""

# Admin schema — full-access user with system-wide control
from app.schemas.entities.admin_schema import AdminSchema
from app.schemas.entities.credit_schema import CreditSchema

# User schema — base representation of any system user
from app.schemas.entities.user_schema import UserSchema

# Client schema — end user submitting applications
from app.schemas.entities.client_schema import ClientSchema

# Worker schema — internal employee managing client applications
from app.schemas.entities.worker_schema import WorkerSchema

# Broker schema — external partner referring and tracking clients
from app.schemas.entities.broker_schema import BrokerSchema

for cls in (
    WorkerSchema.Out,  WorkerSchema.Short,
    ClientSchema.Out,  ClientSchema.Short,
    BrokerSchema.Out,  BrokerSchema.Short, BrokerSchema.WebRegisterResponse,
    CreditSchema.Out, CreditSchema.Short  # ← оце додай
):
    cls.model_rebuild()

BrokerSchema.Out.model_rebuild()
BrokerSchema.WebRegisterResponse.model_rebuild()

CreditSchema.Out.model_rebuild()
CreditSchema.Short.model_rebuild()

# Public API of the entity schemas package
__all__ = [
    "AdminSchema",
    "ClientSchema",
    "WorkerSchema",
    "BrokerSchema",
    "UserSchema",
]

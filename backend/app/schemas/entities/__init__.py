"""
Entity schemas package initializer.

This module re-exports the core Pydantic schemas for each user role/entity in the system.
Use it to import all entity-level schemas from a single access point.
"""

# Admin schema — full-access user with system-wide control
from backend.app.schemas.entities.Admin import AdminSchema

# User schema — base representation of any system user
from backend.app.schemas.entities.User import UserSchema

# Client schema — end user submitting applications
from backend.app.schemas.entities.Client import ClientSchema

# Worker schema — internal employee managing client applications
from backend.app.schemas.entities.Worker import WorkerSchema

# Broker schema — external partner referring and tracking clients
from backend.app.schemas.entities.Broker import BrokerSchema

# Public API of the entity schemas package
__all__ = [
    "AdminSchema",
    "ClientSchema",
    "WorkerSchema",
    "BrokerSchema",
    "UserSchema",
]

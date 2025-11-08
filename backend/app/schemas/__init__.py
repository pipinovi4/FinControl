"""
Schemas package initializer.

This module re-exports all commonly used Pydantic schemas for easier access.
Use this when you want a centralized place to import entity schemas, mixins, and session-related models.
"""
# Base schema
from app.schemas.base import SchemaBase  # Base Pydantic schema with shared config (e.g. ORM mode)

# Entity schemas
from app.schemas.entities import (
    UserSchema,  # Pydantic schema for the User entity
    ClientSchema,  # Pydantic schema for the Client entity
    WorkerSchema,  # Pydantic schema for the Worker entity
    BrokerSchema,  # Pydantic schema for the Broker entity
    AdminSchema  # Pydantic schema for the Admin entity
)

# Mixin schemas (reusable blocks for auth, soft deletion, etc.)
from app.schemas.mixins import (
    AuthSchema,             # Mixin for email/password-based authentication
    DynamicLinkAuthSchema,  # Mixin for dynamic-link login authentication
    SoftDeleteSchema        # Mixin for soft-delete support
)

# Session-related schemas
from app.schemas.sessions.refresh_token import RefreshTokenSchema  # Schema for refresh tokens

# Public API of the schemas package
__all__ = [
    "SchemaBase",
    "RefreshTokenSchema",
    "UserSchema", "ClientSchema", "WorkerSchema", "BrokerSchema", "AdminSchema",
    "AuthSchema", "DynamicLinkAuthSchema", "SoftDeleteSchema"
]

# backend/app/schemas/entities/admin_schema.py

from typing import Optional, Type
from pydantic import BaseModel, Field

from backend.app.schemas.entities.user_schema import UserSchema
from backend.app.schemas.mixins import TimeStampAuthSchema, DynamicLinkAuthSchema


class AdminBase(UserSchema.Base, TimeStampAuthSchema, DynamicLinkAuthSchema):
    """
    Shared schema for the Admin entity.
    """
    display_name: Optional[str] = Field(
        ...,
        example="Jane Admin",
        description="Friendly display name used in dashboards or logs"
    )


class AdminCreate(UserSchema.Create, TimeStampAuthSchema, DynamicLinkAuthSchema):
    """
    Schema for creating a new Admin.
    """
    display_name: str = Field(
        default="Unnamed Admin",
        example="Jane Admin",
        description="Friendly display name for dashboard or logs"
    )
    is_super_admin: bool = Field(
        default=False,
        description="If true, grants full root access to admin features"
    )


class AdminUpdate(UserSchema.Update):
    """
    Schema for updating an existing Admin.
    """
    display_name: str = Field(
        ...,
        example="Jane A.",
        description="Updated friendly display name"
    )


class AdminOut(AdminBase):
    """
    Public schema for returning Admin data in API responses.
    """
    pass


class AdminSchema:
    Base:   Type[BaseModel] = AdminBase
    Create: Type[BaseModel] = AdminCreate
    Update: Type[BaseModel] = AdminUpdate
    Out:    Type[BaseModel] = AdminOut

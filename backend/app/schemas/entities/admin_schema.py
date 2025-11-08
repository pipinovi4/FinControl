# backend/app/schemas/entities/admin_schema.py

from typing import Optional, Type, Union
from pydantic import BaseModel, Field, EmailStr
from uuid import UUID

from app.permissions import PermissionRole
from app.schemas import SchemaBase
from app.schemas.entities.user_schema import UserSchema
from app.schemas.mixins import TimeStampAuthSchema, DynamicLinkAuthSchema


class AdminBase(UserSchema.Base, TimeStampAuthSchema, DynamicLinkAuthSchema):
    """
    Shared schema for the Admin entity.
    """
    display_name: Optional[str] = Field(
        None,
        example="Jane Admin",
        description="Friendly display name used in dashboards or logs"
    )


class AdminCreate(UserSchema.Create):
    """
    Schema for creating a new Admin.
    """
    display_name: Union[str, None] = Field(
        default=None,
        example="Jane A.",
        description="Updated friendly display name"
    )

class AdminUpdate(UserSchema.Update):
    """
    Schema for updating an existing Admin.
    """
    display_name: Optional[str] = Field(
        None,
        example="Jane A.",
        description="Updated friendly display name"
    )


class AdminOut(AdminBase):
    """
    Public schema for returning Admin data in API responses.
    """
    role: PermissionRole = Field(..., description="User role")

class AdminWebRegisterResponse(UserSchema.Base):
    id: UUID = Field(..., description="Unique broker ID")
    email: EmailStr = Field(..., description="Email used for login")
    display_name: str = Field(
        default="Unnamed Admin",
        example="Jane Admin",
        description="Friendly display name for dashboard or logs"
    )

class AdminSchema:
    Base:   Type[BaseModel] = AdminBase
    Create: Type[BaseModel] = AdminCreate
    Update: Type[BaseModel] = AdminUpdate
    Out:    Type[BaseModel] = AdminOut
    WebRegisterResponse: Type[BaseModel] = AdminWebRegisterResponse

# backend/app/schemas/entities/user_schema.py

from typing import Optional, Type
from pydantic import BaseModel, Field
from app.permissions.enums import PermissionRole
from app.schemas import SchemaBase
from app.schemas.mixins import UUIDSchema, TimeStampSchema, SoftDeleteSchema, AuthSchema


class UserBase(SchemaBase, AuthSchema, UUIDSchema, TimeStampSchema, SoftDeleteSchema):
    """
    Base schema shared across all user-related models.
    """
    role: PermissionRole = Field(..., example=PermissionRole.ADMIN.value)
    is_active: bool = Field(..., example=True)


class UserCreate(SchemaBase, AuthSchema.Create):
    """
    Schema for creating a new user.
    """


class UserOut(UserBase, AuthSchema.Out):
    """
    Schema for returning user data to clients.
    """
    pass


class UserUpdate(SchemaBase):
    """
    Schema for updating an existing user.
    """
    is_active: Optional[bool] = Field(None, example=True)


class UserSchema:
    Base: Type[BaseModel] = UserBase
    Create: Type[BaseModel] = UserCreate
    Update: Type[BaseModel] = UserUpdate
    Out: Type[BaseModel] = UserOut

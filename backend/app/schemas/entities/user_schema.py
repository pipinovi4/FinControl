# backend/app/schemas/entities/user_schema.py

from typing import Optional, Type
from pydantic import BaseModel, Field
from backend.app.permissions.enums import PermissionRole
from backend.app.schemas import SchemaBase
from backend.app.schemas.mixins import UUIDSchema, TimeStampSchema, SoftDeleteSchema, AuthSchema


class UserBase(SchemaBase, AuthSchema, UUIDSchema, TimeStampSchema, SoftDeleteSchema):
    """
    Base schema shared across all user-related models.
    """
    telegram_id: str = Field(..., example="123456789")
    telegram_username: str = Field(..., example="user")
    role: PermissionRole = Field(..., example=PermissionRole.ADMIN.value)
    is_active: bool = Field(..., example=True)


class UserCreate(SchemaBase, AuthSchema.Create):
    """
    Schema for creating a new user.
    """
    telegram_id: Optional[str]
    telegram_username: Optional[str]


class UserOut(UserBase, AuthSchema.Out):
    """
    Schema for returning user data to clients.
    """
    pass


class UserUpdate(SchemaBase):
    """
    Schema for updating an existing user.
    """
    telegram_username: Optional[str] = Field(None, example="user_updated")
    is_active: Optional[bool] = Field(None, example=True)


class UserSchema:
    Base: Type[BaseModel] = UserBase
    Create: Type[BaseModel] = UserCreate
    Update: Type[BaseModel] = UserUpdate
    Out: Type[BaseModel] = UserOut

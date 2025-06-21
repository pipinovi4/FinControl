# backend/app/schemas/filters/user_filter_schema.py

from typing import Optional
from pydantic import BaseModel, Field
from backend.app.permissions.enums import PermissionRole


class UserFilterSchema(BaseModel):
    """
    Filter schema for querying User entities.

    Includes:
    - Telegram identifiers
    - Role type
    - Active status
    """
    telegram_id: Optional[str] = Field(
        None,
        example="123456789",
        description="Filter by Telegram ID"
    )
    telegram_username: Optional[str] = Field(
        None,
        example="user",
        description="Filter by Telegram username"
    )
    role: Optional[PermissionRole] = Field(
        None,
        example=PermissionRole.ADMIN,
        description="Filter by assigned role"
    )
    is_active: Optional[bool] = Field(
        None,
        example=True,
        description="Filter by user activity status"
    )

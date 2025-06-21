# backend/app/schemas/entities/worker_schema.py

from typing import Optional, Type
from pydantic import BaseModel, EmailStr, Field

from backend.app.schemas.entities.user_schema import UserSchema
from backend.app.schemas.mixins import TimeStampAuthSchema, DynamicLinkAuthSchema


class WorkerBase(UserSchema.Base, TimeStampAuthSchema, DynamicLinkAuthSchema):
    """
    Shared schema for the Worker entity.
    """
    username: str = Field(..., example="john.smith", description="Internal login username for this worker")
    telegram_username: Optional[str] = Field(
        None, example="pipin", description="Optional Telegram username for contacting this worker"
    )


class WorkerCreate(UserSchema.Create, TimeStampAuthSchema, DynamicLinkAuthSchema):
    """
    Schema for creating a new Worker.
    """
    username: str = Field(..., example="john.smith", description="Unique internal username for login")


class WorkerUpdate(BaseModel):
    """
    Schema for updating Worker profile.
    """
    email: Optional[EmailStr] = Field(None, example="new@example.com")
    password: Optional[str] = Field(None, min_length=8, example="NewStr0ngP@ss")
    full_name: Optional[str] = Field(None, example="John Smith Jr.")
    username: Optional[str] = Field(None, example="john.smith2")
    telegram_username: Optional[str] = Field(None, example="newpipin")


class WorkerOut(WorkerBase):
    """
    Public schema for returning Worker data in API responses.
    """
    pass


class WorkerSchema:
    Base: Type[BaseModel] = WorkerBase
    Create: Type[BaseModel] = WorkerCreate
    Update: Type[BaseModel] = WorkerUpdate
    Out: Type[BaseModel] = WorkerOut

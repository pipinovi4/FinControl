from typing import Optional, Type, List, ForwardRef
from pydantic import BaseModel, Field

from backend.app.schemas.entities.user_schema import UserSchema
from backend.app.schemas.mixins import TimeStampAuthSchema, DynamicLinkAuthSchema

# Forward reference to avoid circular import
ClientOut = ForwardRef("ClientSchema.Out")


class WorkerBase(UserSchema.Base):
    """
    Shared base schema for the Worker entity.
    """
    username: str = Field(..., example="john.smith", description="Internal login username")


class WorkerCreate(UserSchema.Create, TimeStampAuthSchema, DynamicLinkAuthSchema):
    """
    Schema for creating a Worker.
    """
    username: str = Field(..., example="john.smith", description="Internal login username")


class WorkerUpdate(BaseModel):
    """
    Schema for updating a Worker.
    """
    username: Optional[str] = Field(None, example="john.smith.updated")
    telegram_username: Optional[str] = Field(None, example="newpipin")


class WorkerOut(WorkerBase, TimeStampAuthSchema, DynamicLinkAuthSchema):
    """
    Public-facing schema for Worker including metadata and relations.
    """
    clients: Optional[List[ClientOut]] = Field(
        default=None,
        description="List of assigned clients (optional)"
    )


class WorkerSchema:
    Base: Type[BaseModel] = WorkerBase
    Create: Type[BaseModel] = WorkerCreate
    Update: Type[BaseModel] = WorkerUpdate
    Out: Type[BaseModel] = WorkerOut

WorkerOut.model_rebuild()
from __future__ import annotations
from uuid import UUID
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

from backend.app.models.entities.credit import CreditStatus
from backend.app.schemas import SchemaBase


class CreditBase(BaseModel):
    amount: float = Field(..., description="Сума із заявки")
    approved_amount: Optional[float] = Field(None, description="Схвалена сума (ставить адмін)")
    monthly_payment: Optional[float] = Field(None, description="Місячний платіж (ставить адмін)")
    bank_name: Optional[str] = Field(None, max_length=120, description="Банк (ставить адмін)")
    first_payment_date: Optional[datetime] = Field(None, description="Перша дата платежу (ставить адмін)")
    status: CreditStatus = Field(..., description="Статус заявки")
    comment: Optional[str] = Field(None, description="Єдиний текстовий коментар")


class CreditCreate(BaseModel):
    client_id: UUID
    amount: float


class CreditUpdate(BaseModel):
    # для адміна: оновлення фінпараметрів і/або статусу
    amount: Optional[float] = None
    approved_amount: Optional[float] = None
    monthly_payment: Optional[float] = None
    bank_name: Optional[str] = None
    first_payment_date: Optional[datetime] = None
    status: Optional[CreditStatus] = None
    comment: Optional[str] = None


class CreditStatusUpdate(BaseModel):
    # для брокера: міняє лише статус
    status: CreditStatus


class CreditCommentIn(BaseModel):
    text: str = Field(..., min_length=1)  # довжина довільна (Postgres TEXT без ліміту)


class CreditOut(CreditBase):
    id: UUID
    client_id: UUID
    broker_id: Optional[UUID]
    worker_id: Optional[UUID]
    issued_at: datetime
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_deleted: bool

    class Config:
        from_attributes = True


class AdminPaginatedCreditsOut(BaseModel):
    credits: List[CreditOut]
    total: int


class BrokerPaginatedCreditsOut(BaseModel):
    credits: List[CreditOut]
    total: int


class CreditShort(SchemaBase):
    id: UUID
    client_id: UUID
    broker_id: Optional[UUID] = None
    worker_id: Optional[UUID] = None
    amount: float
    status: CreditStatus
    issued_at: datetime


# ───────────── WRAPPER ─────────────
class CreditSchema:
    Base = CreditBase
    Create = CreditCreate
    Update = CreditUpdate
    StatusUpdate = CreditStatusUpdate
    CommentIn = CreditCommentIn
    Out = CreditOut
    Short = CreditShort
    AdminPaginatedOut = AdminPaginatedCreditsOut
    BrokerPaginatedOut = BrokerPaginatedCreditsOut

from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

from backend.app.schemas import SchemaBase


# ─────────────── BASE ───────────────
class CreditBase(SchemaBase):
    amount: int = Field(..., description="Загальна сума кредиту")
    paid_amount: int = Field(..., description="Вже виплачена сума")
    status: str = Field(..., description="Статус кредиту", example="active")
    issued_at: datetime = Field(..., description="Дата видачі кредиту")
    last_payment_at: Optional[datetime] = Field(None, description="Дата останньої оплати")


# ─────────────── CREATE ───────────────
class CreditCreate(SchemaBase):
    client_id: UUID
    broker_id: UUID
    amount: float

# ─────────────── UPDATE ───────────────
class CreditUpdate(BaseModel):
    amount: Optional[int] = None
    paid_amount: Optional[int] = None
    status: Optional[str] = None
    last_payment_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }


# ─────────────── OUT ───────────────
class CreditOut(CreditBase):
    id: UUID
    client_id: UUID


# ─────────────── SHORT ───────────────
class CreditShort(BaseModel):
    id: UUID
    amount: int
    paid_amount: int
    status: str


# ─────────────── WRAPPER ───────────────
class CreditSchema:
    Base = CreditBase
    Create = CreditCreate
    Update = CreditUpdate
    Out = CreditOut
    Short = CreditShort

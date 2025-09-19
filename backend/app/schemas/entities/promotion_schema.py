from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import Field, computed_field
from uuid import UUID

from backend.app.schemas import SchemaBase
from backend.app.models.entities.promotion import PromotionEnum


# ───────────── BASE ─────────────
class PromotionBase(SchemaBase):
    promotion_type: PromotionEnum = Field(..., description="Тип промо (Helix/Union/General)")
    description: str = Field(..., min_length=1, max_length=4000, description="Текст промо")
    is_active: bool = Field(default=True, description="Активне промо чи ні")


# ───────────── CREATE / UPDATE ─────────────
class PromotionCreate(PromotionBase):
    pass


class PromotionUpdate(SchemaBase):
    promotion_type: Optional[PromotionEnum] = None
    description: Optional[str] = Field(None, min_length=1, max_length=4000)
    is_active: Optional[bool] = None


# ───────────── OUT (повний) ─────────────
class PromotionOut(PromotionBase):
    id: UUID
    created_at: datetime
    updated_at: datetime


# ───────────── OUT (компактний для “іконки”) ─────────────
class PromotionSummaryOut(SchemaBase):
    id: UUID
    promotion_type: PromotionEnum
    is_active: bool
    created_at: datetime

    # робимо невеликий прев’ю-текст із description
    description: str

    @computed_field  # type: ignore[misc]
    @property
    def snippet(self) -> str:
        txt = (self.description or "").strip()
        return (txt[:80] + "…") if len(txt) > 80 else txt


# ───────────── OUT (топ воркерів) ─────────────
class TopWorkerOut(SchemaBase):
    worker_id: UUID
    username: str
    credits_count: int

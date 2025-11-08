# services/entities/promotion_service.py
from __future__ import annotations

from typing import Optional, Sequence, TypeVar, Type, cast, List, Dict, Any, Tuple
from uuid import UUID
from datetime import datetime

from sqlalchemy import select, desc, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.entities.promotion import Promotion, PromotionEnum
from app.models.entities.worker import Worker
from app.models.entities.credit import Credit
from app.utils.decorators import handle_exceptions
from app.schemas.entities.promotion_schema import PromotionCreate, PromotionUpdate


PromotionT = TypeVar("PromotionT", bound=Promotion)


class PromotionService:
    """
    Async service for managing Promotion entities.
    """

    def __init__(self, db: AsyncSession, model: Type[PromotionT] = Promotion):
        self.db = db
        self.model = model

    # ───────────────────────────────────────────────
    # READ
    # ───────────────────────────────────────────────
    @handle_exceptions(raise_404=True)
    async def get_by_id(self, promo_id: UUID) -> PromotionT:
        """
        Retrieve a promotion by id (404 if not found).
        """
        stmt = select(self.model).where(self.model.id == promo_id)
        res = await self.db.execute(stmt)
        promo = res.scalar_one_or_none()
        return cast(PromotionT, promo)

    @handle_exceptions()
    async def get_all(
        self,
        *,
        is_active: Optional[bool] = None,
        ptype: Optional[PromotionEnum] = None,
        limit: Optional[int] = None,
    ) -> Sequence[PromotionT]:
        """
        List promotions with optional filters.
        """
        stmt = select(self.model).order_by(desc(self.model.created_at))
        if is_active is not None:
            stmt = stmt.where(self.model.is_active.is_(is_active))
        if ptype is not None:
            stmt = stmt.where(self.model.promotion_type == ptype)
        if limit:
            stmt = stmt.limit(limit)

        res = await self.db.execute(stmt)
        return cast(Sequence[PromotionT], res.scalars().all())

    @handle_exceptions()
    async def list_active_by_type(self, ptype: PromotionEnum) -> Sequence[PromotionT]:
        """
        All active promotions of a given type, newest first.
        """
        stmt = (
            select(self.model)
            .where(self.model.promotion_type == ptype, self.model.is_active.is_(True))
            .order_by(desc(self.model.created_at))
        )
        res = await self.db.execute(stmt)
        return cast(Sequence[PromotionT], res.scalars().all())

    # ───────────────────────────────────────────────
    # WRITE
    # ───────────────────────────────────────────────
    @handle_exceptions()
    async def create(self, payload: PromotionCreate) -> PromotionT:
        """
        Create a promotion.
        """
        promo = self.model(**payload.model_dump())
        self.db.add(promo)
        await self.db.commit()
        await self.db.refresh(promo)
        return cast(PromotionT, promo)

    @handle_exceptions(raise_404=True)
    async def update(self, promo_id: UUID, payload: PromotionUpdate) -> PromotionT:
        """
        Patch a promotion.
        """
        promo = await self.get_by_id(promo_id)
        for k, v in payload.model_dump(exclude_unset=True).items():
            setattr(promo, k, v)
        await self.db.commit()
        await self.db.refresh(promo)
        return cast(PromotionT, promo)

    @handle_exceptions(raise_404=True)
    async def deactivate(self, promo_id: UUID) -> None:
        """
        Soft-deactivate the promotion (is_active=False).
        """
        promo = await self.get_by_id(promo_id)
        promo.is_active = False
        await self.db.commit()

    @handle_exceptions(raise_404=True)
    async def activate(self, promo_id: UUID, *, deactivate_others_same_type: bool = False) -> PromotionT:
        """
        Activate a promotion. Optionally deactivate other active promos of the same type.
        """
        promo = await self.get_by_id(promo_id)
        promo.is_active = True

        if deactivate_others_same_type:
            stmt = (
                select(self.model.id)
                .where(
                    self.model.promotion_type == promo.promotion_type,
                    self.model.is_active.is_(True),
                    self.model.id != promo.id,
                )
            )
            ids = [row[0] for row in (await self.db.execute(stmt)).all()]
            if ids:
                # bulk update
                await self.db.execute(
                    self.model.__table__.update()
                    .where(self.model.id.in_(ids))
                    .values(is_active=False)
                )

        await self.db.commit()
        await self.db.refresh(promo)
        return cast(PromotionT, promo)

    # ───────────────────────────────────────────────
    # TOP-3 WORKERS BY CREDITS (для промо-виджету)
    # ───────────────────────────────────────────────
    @handle_exceptions()
    async def top_workers_by_credits(
        self,
        *,
        limit: int = 3,
        completed_statuses: Tuple[str, ...] = ("completed", "closed", "paid"),
        use_paid_sum: bool = False,  # True → сумуємо paid_amount; False → amount
    ) -> List[Dict[str, Any]]:
        """
        Aggregate: top workers by number of completed credits, then by total sum.
        """
        sum_col = Credit.paid_amount if use_paid_sum else Credit.amount

        stmt = (
            select(
                Worker.id.label("worker_id"),
                Worker.username,
                func.count(Credit.id).label("credits_count"),
                func.coalesce(func.sum(sum_col), 0).label("total_sum"),
            )
            .join(Credit, Credit.worker_id == Worker.id)
            .where(Credit.status.in_(completed_statuses))
            .group_by(Worker.id, Worker.username)
            .order_by(desc("credits_count"), desc("total_sum"))
            .limit(limit)
        )

        rows = (await self.db.execute(stmt)).all()
        return [
            {
                "worker_id": r.worker_id,
                "username": r.username,
                "credits_count": int(r.credits_count),
                "total_sum": float(r.total_sum),
            }
            for r in rows
        ]

    @staticmethod
    async def list(
        session: AsyncSession,
        *,
        limit: int = 20,
        ptype: str | None = None,
        is_active: bool | None = None,
        include_deleted: bool = False,
    ) -> list[Promotion]:
        stmt = select(Promotion).order_by(Promotion.created_at.desc()).limit(limit)
        if not include_deleted:
            stmt = stmt.where(Promotion.is_deleted.is_(False))
        if ptype:
            stmt = stmt.where(Promotion.promotion_type == ptype)
        if is_active is not None:
            stmt = stmt.where(Promotion.is_active.is_(is_active))
        rows = (await session.scalars(stmt)).all()
        return list(rows)

    @staticmethod
    async def soft_delete(session: AsyncSession, promotion_id: UUID) -> None:
        """
        Soft delete by marking is_deleted=True + deleted_at=now().
        Also deactivates the promotion.
        """
        await session.execute(
            update(Promotion)
            .where(Promotion.id == promotion_id, Promotion.is_deleted.is_(False))
            .values(is_deleted=True, deleted_at=datetime.utcnow(), is_active=False)
        )
        await session.commit()

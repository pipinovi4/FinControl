from __future__ import annotations

from datetime import datetime
from typing import Optional, List, Tuple, Sequence, TypeVar, Type, cast as tcast
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.decorators import handle_exceptions
from app.models.entities.credit import Credit, CreditStatus
from app.models.entities.application import Application
from app.schemas.entities.credit_schema import CreditCreate, CreditUpdate
from app.routes.entities.crud.dashboard.types import DeletedFilter

from .pagination import credit_list_paginated
from .helpers import ensure_broker_access, soft_delete_credit, restore_credit


CreditT = TypeVar("CreditT", bound=Credit)


class CreditService:
    """
    Async credit service.
    Fully Application-based.
    """

    def __init__(self, db: AsyncSession, model: Type[CreditT] = Credit):
        self.db = db
        self.model = model

    # ─────────────────────────────────────────────
    # READ
    # ─────────────────────────────────────────────
    @handle_exceptions(raise_404=True)
    async def get_by_id(self, credit_id: UUID) -> CreditT:
        stmt = select(self.model).where(self.model.id == credit_id)
        res = await self.db.execute(stmt)
        return tcast(CreditT, res.scalar_one_or_none())

    @handle_exceptions()
    async def list(
        self,
        *,
        status: Optional[CreditStatus] = None,
        broker_id: Optional[UUID] = None,
        application_id: Optional[UUID] = None,
        limit: Optional[int] = None,
    ) -> Sequence[CreditT]:

        stmt = select(self.model)
        if status:
            stmt = stmt.where(self.model.status == status)
        if broker_id:
            stmt = stmt.where(self.model.broker_id == broker_id)
        if application_id:
            stmt = stmt.where(self.model.application_id == application_id)

        stmt = stmt.order_by(self.model.issued_at.desc())
        if limit:
            stmt = stmt.limit(limit)

        res = await self.db.execute(stmt)
        return tcast(Sequence[CreditT], res.scalars().all())

    # ─────────────────────────────────────────────
    # PAGINATION
    # ─────────────────────────────────────────────
    @handle_exceptions()
    async def list_paginated(
        self,
        *,
        skip: int = 0,
        limit: int = 20,
        statuses: Optional[List[CreditStatus]] = None,
        broker_id: Optional[UUID] = None,
        application_id: Optional[UUID] = None,
        created_from: Optional[datetime] = None,
        created_to: Optional[datetime] = None,
        deleted: DeletedFilter = "active",
        search: Optional[str] = None,
    ) -> Tuple[List[CreditT], int]:

        return await credit_list_paginated(
            db=self.db,
            model=self.model,
            skip=skip,
            limit=limit,
            statuses=statuses,
            broker_id=broker_id,
            application_id=application_id,
            created_from=created_from,
            created_to=created_to,
            deleted=deleted,
            search=search,
        )

    # ─────────────────────────────────────────────
    # CREATE / UPDATE
    # ─────────────────────────────────────────────
    @handle_exceptions()
    async def create(self, payload: CreditCreate) -> CreditT:
        application = await self.db.get(Application, payload.application_id)
        if not application:
            raise ValueError("Application does not exist")

        if not application.broker_id:
            raise ValueError("Application must be assigned to a broker")

        credit = self.model(
            application_id=application.id,
            broker_id=application.broker_id,
            worker_id=application.worker_id,
            amount=payload.amount,
            status=CreditStatus.NEW,
        )

        self.db.add(credit)
        await self.db.commit()
        await self.db.refresh(credit)
        return tcast(CreditT, credit)

    @handle_exceptions(raise_404=True)
    async def update(self, credit_id: UUID, payload: CreditUpdate) -> CreditT:
        credit = await self.get_by_id(credit_id)
        data = payload.model_dump(exclude_unset=True)
        for k, v in data.items():
            setattr(credit, k, v)
        await self.db.commit()
        await self.db.refresh(credit)
        return credit

    @handle_exceptions()
    async def set_financials(
        self,
        credit_id: UUID,
        *,
        approved_amount: Optional[float] = None,
        monthly_payment: Optional[float] = None,
        bank_name: Optional[str] = None,
        first_payment_date: Optional[datetime] = None,
    ) -> CreditT:
        credit = await self.get_by_id(credit_id)

        if approved_amount is not None:
            credit.approved_amount = approved_amount
        if monthly_payment is not None:
            credit.monthly_payment = monthly_payment
        if bank_name is not None:
            credit.bank_name = bank_name
        if first_payment_date is not None:
            credit.first_payment_date = first_payment_date

        await self.db.commit()
        await self.db.refresh(credit)
        return credit

    # ─────────────────────────────────────────────
    # STATUS / COMMENTS
    # ─────────────────────────────────────────────
    @handle_exceptions()
    async def change_status(self, credit_id: UUID, new_status: CreditStatus) -> CreditT:
        credit = await self.get_by_id(credit_id)
        credit.status = new_status
        await self.db.commit()
        await self.db.refresh(credit)
        return credit

    @handle_exceptions()
    async def broker_update_status(self, credit_id: UUID, new_status: CreditStatus) -> CreditT:
        if new_status not in {
            CreditStatus.APPROVED,
            CreditStatus.TREATMENT,
            CreditStatus.REJECTED,
        }:
            raise ValueError("Broker can only set APPROVED, TREATMENT or REJECTED")

        return await self.change_status(credit_id, new_status)

    @handle_exceptions()
    async def add_comment(self, credit_id: UUID, comment_text: str) -> CreditT:
        credit = await self.get_by_id(credit_id)
        credit.comment = comment_text
        await self.db.commit()
        await self.db.refresh(credit)
        return credit

    @handle_exceptions()
    async def complete(self, credit_id: UUID) -> CreditT:
        credit = await self.get_by_id(credit_id)
        credit.status = CreditStatus.COMPLETED
        await self.db.commit()
        await self.db.refresh(credit)
        return credit

    # ─────────────────────────────────────────────
    # DELETE
    # ─────────────────────────────────────────────
    @staticmethod
    async def soft_delete(session: AsyncSession, credit_id: UUID) -> None:
        await soft_delete_credit(session, credit_id)

    @staticmethod
    async def restore(session: AsyncSession, credit_id: UUID) -> None:
        await restore_credit(session, credit_id)

    # ─────────────────────────────────────────────
    # BROKER ACCESS HELPERS
    # ─────────────────────────────────────────────
    @handle_exceptions(raise_404=True)
    async def get_for_broker(self, credit_id: UUID, broker_id: UUID):
        credit = await self.get_by_id(credit_id)
        ensure_broker_access(credit, broker_id)
        return credit

    @handle_exceptions()
    async def list_for_broker_paginated(
        self,
        broker_id: UUID,
        *,
        skip: int = 0,
        limit: int = 20,
        statuses: Optional[List[CreditStatus]] = None,
        application_id: Optional[UUID] = None,
        created_from: Optional[datetime] = None,
        created_to: Optional[datetime] = None,
    ):
        return await self.list_paginated(
            skip=skip,
            limit=limit,
            statuses=statuses,
            broker_id=broker_id,
            application_id=application_id,
            created_from=created_from,
            created_to=created_to,
        )

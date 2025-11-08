# backend/app/services/entities/credit/credit_service.py
from __future__ import annotations

import re
from datetime import datetime
from typing import Optional, Sequence, TypeVar, Type, cast as tcast, Tuple, List
from uuid import UUID

from fastapi import HTTPException, status

from sqlalchemy import (
    select,
    update,
    desc,
    func,
    and_,
    or_,
    cast as sa_cast,
    String,
)
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.decorators import handle_exceptions
from app.models.entities.client import Client
from app.models.entities.credit import Credit, CreditStatus
# Використовуй спільний тип DeletedFilter, щоб не дублювати Literal в різних місцях
from app.routes.entities.crud.dashboard.types import DeletedFilter


CreditT = TypeVar("CreditT", bound=Credit)


def _phone_norm(expr):
    """Нормалізатор телефону (видаляє все, крім цифр) — PostgreSQL functional expression."""
    return func.regexp_replace(expr, r"[^0-9]", "", "g")


def _looks_uuid(s: str) -> UUID | None:
    try:
        return UUID(s)
    except Exception:
        return None


def _search_clause_for_credit(search: str):
    """
    Підтримка кількох термів через пробіли/коми.
    Для кожного терму будуємо диз’юнкцію по:
      - id кредита (like + exact UUID)
      - client.email / client.full_name / client.phone_number (+ normalized phone like)
      - exact UUID клієнта
    Потім усі терми з’єднуємо AND-ом.
    """
    if not search:
        return None

    terms = [t.strip() for t in re.split(r"[\s,]+", search) if t.strip()]
    if not terms:
        return None

    and_groups = []
    for t in terms:
        like = f"%{t}%"
        disj = [
            sa_cast(Credit.id, String).ilike(like),
            Client.email.ilike(like),
            Client.full_name.ilike(like),
            Client.phone_number.ilike(like),
            _phone_norm(Client.phone_number).ilike(_phone_norm(like)),
        ]
        uid = _looks_uuid(t)
        if uid:
            disj.append(Credit.id == uid)   # exact match по id кредита
            disj.append(Client.id == uid)   # exact match по id клієнта
        and_groups.append(or_(*disj))

    return and_(*and_groups)


class CreditService:
    """
    Async service for managing Credit entities.

    Roles & permissions (на рівні сервісу):
      - Broker: може змінювати окремі статуси та додавати коментар.
      - Admin : може створювати кредити, оновлювати фінпараметри, змінювати будь-який статус.
    """

    def __init__(self, db: AsyncSession, model: Type[CreditT] = Credit):
        self.db = db
        self.model = model

    # ───────────────────────────────────────────────
    # READ
    # ───────────────────────────────────────────────
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
        client_id: Optional[UUID] = None,
        limit: Optional[int] = None,
    ) -> Sequence[CreditT]:
        stmt = select(self.model).order_by(desc(self.model.issued_at))
        if status:
            stmt = stmt.where(self.model.status == status)
        if broker_id:
            stmt = stmt.where(self.model.broker_id == broker_id)
        if client_id:
            stmt = stmt.where(self.model.client_id == client_id)
        if limit:
            stmt = stmt.limit(limit)

        res = await self.db.execute(stmt)
        return tcast(Sequence[CreditT], res.scalars().all())

    @handle_exceptions()
    async def list_paginated(
        self,
        *,
        skip: int = 0,
        limit: int = 20,
        statuses: Optional[List[CreditStatus]] = None,
        broker_id: Optional[UUID] = None,
        client_id: Optional[UUID] = None,
        created_from: Optional[datetime] = None,
        created_to: Optional[datetime] = None,
        deleted: DeletedFilter = "active",
        search: Optional[str] = None,
    ) -> Tuple[List[CreditT], int]:
        """
        Пагінація кредитів з фільтрами і пошуком,
        без cartesian product у SQL (один LEFT JOIN на Client).
        """
        where: List = []

        # deleted filter
        if deleted == "active":
            where.append(self.model.is_deleted.is_(False))
        elif deleted == "only":
            where.append(self.model.is_deleted.is_(True))
        # "all" — без умови

        if statuses:
            where.append(self.model.status.in_(statuses))
        if broker_id:
            where.append(self.model.broker_id == broker_id)
        if client_id:
            where.append(self.model.client_id == client_id)
        if created_from:
            where.append(self.model.issued_at >= created_from)
        if created_to:
            where.append(self.model.issued_at <= created_to)

        sc = _search_clause_for_credit(search or "")
        if sc is not None:
            where.append(sc)

        # ── базовий SELECT з єдиним JOIN на Client
        # для total рахуємо по підзапиту, аби не дублювати рядки
        base_ids = (
            select(self.model.id)
            .join(Client, Client.id == self.model.client_id, isouter=True)
        )
        if where:
            base_ids = base_ids.where(and_(*where))

        total = int(
            (await self.db.execute(select(func.count()).select_from(base_ids.subquery()))).scalar_one()
        )

        # сторінка даних
        data_stmt = (
            select(self.model)
            .join(Client, Client.id == self.model.client_id, isouter=True)
        )
        if where:
            data_stmt = data_stmt.where(and_(*where))
        data_stmt = (
            data_stmt
            .options(selectinload(self.model.client))   # якщо є relationship Credit.client
            .order_by(desc(self.model.issued_at))
            .offset(skip)
            .limit(limit)
        )

        rows = (await self.db.execute(data_stmt)).scalars().all()
        return tcast(List[CreditT], rows), total

    # ───────────────────────────────────────────────
    # CREATE / UPDATE (ADMIN)
    # ───────────────────────────────────────────────
    @handle_exceptions()
    async def create(self, payload) -> CreditT:
        """
        Створює кредит від імені Адміна.
        Автоматично підставляє broker_id з клієнта.
        """
        from app.schemas.entities.credit_schema import CreditCreate  # локальний імпорт, щоб уникати циклів
        if not isinstance(payload, CreditCreate):
            # якщо приходить plain dict (напряму з Pydantic), це не критично
            pass

        client = await self.db.get(Client, payload.client_id)
        if not client or not client.broker_id:
            raise ValueError("Client must exist and have broker_id before creating credit")

        credit = self.model(
            client_id=client.id,
            broker_id=client.broker_id,
            amount=payload.amount,
            status=CreditStatus.NEW,
        )
        self.db.add(credit)
        await self.db.commit()
        await self.db.refresh(credit)
        return tcast(CreditT, credit)

    @handle_exceptions(raise_404=True)
    async def update(self, credit_id: UUID, payload) -> CreditT:
        from app.schemas.entities.credit_schema import CreditUpdate
        credit = await self.get_by_id(credit_id)
        data = payload.model_dump(exclude_unset=True) if hasattr(payload, "model_dump") else dict(payload or {})
        for k, v in data.items():
            setattr(credit, k, v)
        await self.db.commit()
        await self.db.refresh(credit)
        return tcast(CreditT, credit)

    @handle_exceptions(raise_404=True)
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
        return tcast(CreditT, credit)

    # ───────────────────────────────────────────────
    # STATUS / COMMENTS
    # ───────────────────────────────────────────────
    @handle_exceptions(raise_404=True)
    async def change_status(self, credit_id: UUID, new_status: CreditStatus) -> CreditT:
        credit = await self.get_by_id(credit_id)
        credit.status = new_status
        await self.db.commit()
        await self.db.refresh(credit)
        return tcast(CreditT, credit)

    @handle_exceptions(raise_404=True)
    async def broker_update_status(self, credit_id: UUID, new_status: CreditStatus) -> CreditT:
        if new_status not in {CreditStatus.APPROVED, CreditStatus.TREATMENT, CreditStatus.REJECTED}:
            raise ValueError("Broker is allowed to set only APPROVED, TREATMENT or REJECTED")
        return await self.change_status(credit_id, new_status)

    @handle_exceptions(raise_404=True)
    async def add_comment(self, credit_id: UUID, comment_text: str) -> CreditT:
        credit = await self.get_by_id(credit_id)
        credit.comment = comment_text
        await self.db.commit()
        await self.db.refresh(credit)
        return tcast(CreditT, credit)

    @handle_exceptions(raise_404=True)
    async def complete(self, credit_id: UUID) -> CreditT:
        credit = await self.get_by_id(credit_id)
        credit.status = CreditStatus.COMPLETED
        await self.db.commit()
        await self.db.refresh(credit)
        return tcast(CreditT, credit)

    # ───────────────────────────────────────────────
    # DELETE (soft)
    # ───────────────────────────────────────────────
    @staticmethod
    async def soft_delete(session: AsyncSession, credit_id: UUID) -> None:
        await session.execute(
            update(Credit)
            .where(Credit.id == credit_id, Credit.is_deleted.is_(False))
            .values(is_deleted=True)
        )
        await session.commit()

    @staticmethod
    async def restore(session: AsyncSession, credit_id: UUID) -> None:
        await session.execute(
            update(Credit)
            .where(Credit.id == credit_id, Credit.is_deleted.is_(True))
            .values(is_deleted=False)
        )
        await session.commit()

    # ───────────────────────────────────────────────
    # HELPERS (scoped access for broker)
    # ───────────────────────────────────────────────
    @handle_exceptions(raise_404=True)
    async def get_for_broker(self, credit_id: UUID, broker_id: UUID) -> CreditT:
        credit = await self.get_by_id(credit_id)
        if credit.broker_id is None or credit.broker_id != broker_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied to this credit")
        return credit

    @handle_exceptions()
    async def list_for_broker_paginated(
        self,
        broker_id: UUID,
        *,
        skip: int = 0,
        limit: int = 20,
        statuses: Optional[List[CreditStatus]] = None,
        client_id: Optional[UUID] = None,
        created_from: Optional[datetime] = None,
        created_to: Optional[datetime] = None,
    ) -> Tuple[List[CreditT], int]:
        return await self.list_paginated(
            skip=skip,
            limit=limit,
            statuses=statuses,
            broker_id=broker_id,
            client_id=client_id,
            created_from=created_from,
            created_to=created_to,
        )

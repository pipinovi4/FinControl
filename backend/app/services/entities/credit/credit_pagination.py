from __future__ import annotations

from datetime import datetime
from typing import Optional, List, Tuple, Type, cast as tcast

from sqlalchemy import select, and_, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.entities.credit import Credit, CreditStatus
from app.models.entities.application import Application
from app.routes.entities.crud.dashboard.types import DeletedFilter

from .credit_queries import search_clause_for_credit


async def credit_list_paginated(
    *,
    db: AsyncSession,
    model: Type[Credit],
    skip: int,
    limit: int,
    statuses: Optional[List[CreditStatus]],
    broker_id: Optional[str],
    application_id: Optional[str],
    created_from: Optional[datetime],
    created_to: Optional[datetime],
    deleted: DeletedFilter,
    search: Optional[str],
) -> Tuple[List[Credit], int]:

    where = []

    # deletion
    if deleted == "active":
        where.append(model.is_deleted.is_(False))
    elif deleted == "only":
        where.append(model.is_deleted.is_(True))

    if statuses:
        where.append(model.status.in_(statuses))

    if broker_id:
        where.append(model.broker_id == broker_id)

    if application_id:
        where.append(model.application_id == application_id)

    if created_from:
        where.append(model.issued_at >= created_from)
    if created_to:
        where.append(model.issued_at <= created_to)

    sc = search_clause_for_credit(search or "")
    if sc is not None:
        where.append(sc)

    base_ids = (
        select(model.id)
        .join(Application, Application.id == model.application_id, isouter=True)
    )

    if where:
        base_ids = base_ids.where(and_(*where))

    total = int(
        (
            await db.execute(
                select(func.count()).select_from(base_ids.subquery())
            )
        ).scalar_one()
    )

    data_stmt = (
        select(model)
        .join(Application, Application.id == model.application_id, isouter=True)
    )

    if where:
        data_stmt = data_stmt.where(and_(*where))

    data_stmt = (
        data_stmt
        .options(selectinload(model.application))
        .order_by(model.issued_at.desc())
        .offset(skip)
        .limit(limit)
    )

    rows = (await db.execute(data_stmt)).scalars().all()
    return tcast(List[Credit], rows), total

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update
from uuid import UUID

from app.models.entities.credit import Credit


def ensure_broker_access(credit: Credit, broker_id: UUID):
    if credit.broker_id != broker_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )


async def soft_delete_credit(session: AsyncSession, credit_id: UUID):
    await session.execute(
        update(Credit)
        .where(Credit.id == credit_id, Credit.is_deleted.is_(False))
        .values(is_deleted=True)
    )
    await session.commit()


async def restore_credit(session: AsyncSession, credit_id: UUID):
    await session.execute(
        update(Credit)
        .where(Credit.id == credit_id, Credit.is_deleted.is_(True))
        .values(is_deleted=False)
    )
    await session.commit()

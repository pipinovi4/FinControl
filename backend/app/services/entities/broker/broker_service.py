from sqlalchemy import select, update, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence, TypeVar, cast
from uuid import UUID

from app.models.entities import Broker, Application
from app.permissions import PermissionRole
from app.services.auth import PasswordService
from app.services.entities import UserService
from app.utils.decorators import handle_exceptions
from app.schemas.entities.broker_schema import BrokerSchema

BrokerT = TypeVar("BrokerT", bound=Broker)


class BrokerService(UserService):
    """
    Async CRUD & assignment service for Broker,
    rewritten for APPLICATION-BASED architecture.
    """

    def __init__(self, db: AsyncSession):
        super().__init__(db)
        self.db = db

    # ---------------------------------------------------------
    # GETTERS
    # ---------------------------------------------------------
    @handle_exceptions(raise_404=True)
    async def get_by_id(self, broker_id: UUID) -> BrokerT:
        stmt = (
            select(Broker)
            .where(Broker.id == broker_id, Broker.is_deleted == False)
            .options(
                selectinload(Broker.applications),
                selectinload(Broker.credits),
            )
        )
        result = await self.db.execute(stmt)
        return cast(BrokerT, result.scalar_one_or_none())

    @handle_exceptions()
    async def get_by_email(self, email: str) -> BrokerT | None:
        stmt = select(Broker).where(Broker.email == email)
        result = await self.db.execute(stmt)
        return cast(BrokerT, result.scalar_one_or_none())

    @handle_exceptions()
    async def get_all_brokers(self) -> Sequence[BrokerT]:
        stmt = select(Broker).where(Broker.role == PermissionRole.BROKER)
        result = await self.db.execute(stmt)
        return cast(Sequence[BrokerT], result.scalars().all())

    # ---------------------------------------------------------
    # CREATE / UPDATE / DELETE
    # ---------------------------------------------------------
    @handle_exceptions()
    async def create(self, broker_data: BrokerSchema.Create) -> BrokerT:
        data = broker_data.model_dump()
        data["password_hash"] = PasswordService.hash(data.pop("password"))

        broker = Broker(**data)
        self.db.add(broker)
        await self.db.commit()
        await self.db.refresh(broker)
        return cast(BrokerT, broker)

    @handle_exceptions()
    async def update(self, broker_id: UUID, updates: BrokerSchema.Update) -> BrokerT:
        broker = await self.get_by_id(broker_id)

        for key, value in updates.model_dump(exclude_unset=True).items():
            setattr(broker, key, value)

        await self.db.commit()
        await self.db.refresh(broker)
        return cast(BrokerT, broker)

    @handle_exceptions()
    async def delete(self, broker_id: UUID) -> BrokerT:
        broker = await self.get_by_id(broker_id)
        await self.db.delete(broker)
        await self.db.commit()
        return cast(BrokerT, broker)

    # ---------------------------------------------------------
    # APPLICATIONS – MAIN CHANGE
    # ---------------------------------------------------------
    @handle_exceptions()
    async def get_broker_applications(self, broker_id: UUID) -> Sequence[Application]:
        stmt = select(Application).where(
            Application.broker_id == broker_id,
            Application.is_deleted == False,
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    @handle_exceptions()
    async def remove_application_from_broker(self, application_id: UUID) -> Application | None:
        stmt = select(Application).where(Application.id == application_id)
        result = await self.db.execute(stmt)
        app = result.scalar_one_or_none()

        if app:
            app.broker_id = None
            await self.db.commit()
            await self.db.refresh(app)

        return app

    @handle_exceptions()
    async def reassign_application_to_broker(self, application_id: UUID, new_broker_id: UUID) -> Application | None:
        stmt = select(Application).where(Application.id == application_id)
        result = await self.db.execute(stmt)
        app = result.scalar_one_or_none()

        if app:
            app.broker_id = new_broker_id
            await self.db.commit()
            await self.db.refresh(app)

        return app

    # ---------------------------------------------------------
    # AGGREGATES
    # ---------------------------------------------------------
    @handle_exceptions(default_return=0)
    async def get_broker_applications_count(self, broker_id: UUID) -> int:
        stmt = select(func.count()).select_from(Application).where(
            Application.broker_id == broker_id,
            Application.is_deleted == False,
        )
        return (await self.db.execute(stmt)).scalar_one()

    @handle_exceptions(default_return=False)
    async def has_application(self, broker_id: UUID, application_id: UUID) -> bool:
        stmt = select(Application).where(
            Application.id == application_id,
            Application.broker_id == broker_id,
            Application.is_deleted == False,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none() is not None

    @handle_exceptions()
    async def bulk_assign_applications(self, broker_id: UUID, application_ids: list[UUID]) -> None:
        stmt = (
            update(Application)
            .where(Application.id.in_(application_ids))
            .values(broker_id=broker_id)
        )
        await self.db.execute(stmt)
        await self.db.commit()

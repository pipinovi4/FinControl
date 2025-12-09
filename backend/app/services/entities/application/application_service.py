# backend/app/services/entities/application/application_service.py

from typing import Sequence, TypeVar, Type, cast
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.orm.attributes import flag_modified

from app.models.entities.application import Application
from app.services.entities.user import UserService
from app.utils.decorators import handle_exceptions


ApplicationT = TypeVar("ApplicationT", bound=Application)


class ApplicationService(UserService):

    def __init__(self, db: AsyncSession, model: Type[ApplicationT] = Application):
        super().__init__(db)
        self.model = model

    # -------------------------------------------------------
    # BASIC CRUD
    # -------------------------------------------------------

    @handle_exceptions(raise_404=True)
    async def get_by_id(self, application_id: UUID) -> ApplicationT:
        stmt = (
            select(self.model)
            .where(self.model.id == application_id)
            .options(
                selectinload(Application.worker),
                selectinload(Application.broker),
                selectinload(Application.credits),
            )
        )
        result = await self.db.execute(stmt)
        return cast(ApplicationT, result.scalar_one())

    @handle_exceptions()
    async def get_all(self, include_deleted=False) -> Sequence[ApplicationT]:
        stmt = select(self.model)
        if not include_deleted:
            stmt = stmt.where(self.model.is_deleted == False)

        result = await self.db.execute(stmt)
        return cast(Sequence[ApplicationT], result.scalars().all())

    @handle_exceptions()
    async def create(self, telegram_id: UUID, data: dict) -> ApplicationT:
        app = self.model(telegram_id=telegram_id, data=data)
        self.db.add(app)
        await self.db.commit()
        await self.db.refresh(app)
        return cast(ApplicationT, app)

    @handle_exceptions()
    async def update_data(self, application_id: UUID, new_data: dict) -> ApplicationT:
        app = await self.get_by_id(application_id)

        # 1. Делаем защищённое merge чтобы не затирать нормальные поля
        app.data = {**app.data, **new_data}

        # 2. Помечаем JSONB как изменённый (иначе PG может не записать)
        flag_modified(app, "data")

        await self.db.commit()
        await self.db.refresh(app)
        return app
    @handle_exceptions()
    async def assign_worker(self, application_id: UUID, worker_id: UUID):
        app = await self.get_by_id(application_id)
        app.worker_id = worker_id
        await self.db.commit()
        return app

    @handle_exceptions()
    async def assign_broker(self, application_id: UUID, broker_id: UUID):
        app = await self.get_by_id(application_id)
        app.broker_id = broker_id
        await self.db.commit()
        return app

    @handle_exceptions()
    async def soft_delete(self, application_id: UUID):
        app = await self.get_by_id(application_id)
        app.is_deleted = True
        await self.db.commit()
        return app

    @handle_exceptions()
    async def restore(self, application_id: UUID):
        app = await self.get_by_id(application_id)
        app.is_deleted = False
        await self.db.commit()
        return app

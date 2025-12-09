from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select, update
from uuid import UUID
from typing import Sequence, cast, TypeVar

from app.models import Worker, Application
from app.services.auth import PasswordService
from app.services.entities import UserService
from app.utils.decorators import handle_exceptions
from app.schemas.entities.worker_schema import WorkerSchema

WorkerT = TypeVar("WorkerT", bound=Worker)


class WorkerService(UserService):
    """
    Async service for CRUD + assignment operations for Worker,
    rewritten for APPLICATION-BASED architecture.

    Methods:
        - get_by_id
        - get_by_username
        - get_by_email
        - get_applications
        - assign_application
        - unassign_application
        - bulk_assign_applications
        - create
        - update
        - delete
    """

    def __init__(self, db: AsyncSession):
        super().__init__(db)
        self.db = db

    # ---------------------------------------------------------
    # GETTERS
    # ---------------------------------------------------------
    @handle_exceptions(raise_404=True)
    async def get_by_id(self, worker_id: UUID) -> WorkerT | None:
        stmt = (
            select(Worker)
            .where(Worker.id == worker_id)
            .options(
                selectinload(Worker.applications),
                selectinload(Worker.credits),
            )
        )
        result = await self.db.execute(stmt)
        return cast(WorkerT, result.scalar_one_or_none())

    @handle_exceptions()
    async def get_by_username(self, username: str) -> WorkerT | None:
        stmt = (
            select(Worker)
            .where(Worker.username == username)
            .options(
                selectinload(Worker.applications),
                selectinload(Worker.credits),
            )
        )
        result = await self.db.execute(stmt)
        return cast(WorkerT, result.scalar_one_or_none())

    @handle_exceptions()
    async def get_by_email(self, email: str) -> WorkerT | None:
        stmt = (
            select(Worker)
            .where(Worker.email == email)
            .options(
                selectinload(Worker.applications),
                selectinload(Worker.credits),
            )
        )
        result = await self.db.execute(stmt)
        return cast(WorkerT, result.scalar_one_or_none())

    # ---------------------------------------------------------
    # APPLICATIONS
    # ---------------------------------------------------------
    @handle_exceptions()
    async def get_applications(self, worker_id: UUID) -> Sequence[Application]:
        stmt = select(Application).where(Application.worker_id == worker_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    @handle_exceptions()
    async def assign_application(self, worker_id: UUID, application_id: UUID) -> None:
        stmt = (
            update(Application)
            .where(Application.id == application_id)
            .values(worker_id=worker_id)
        )
        await self.db.execute(stmt)
        await self.db.commit()

    @handle_exceptions()
    async def unassign_application(self, worker_id: UUID, application_id: UUID) -> None:
        stmt = select(Application).where(Application.id == application_id)
        result = await self.db.execute(stmt)
        app = result.scalar_one_or_none()

        if app and app.worker_id == worker_id:
            stmt = (
                update(Application)
                .where(Application.id == application_id)
                .values(worker_id=None, taken_at_worker=None)
            )
            await self.db.execute(stmt)
            await self.db.commit()

    @handle_exceptions()
    async def bulk_assign_applications(self, worker_id: UUID, application_ids: list[UUID]) -> None:
        stmt = (
            update(Application)
            .where(Application.id.in_(application_ids))
            .values(worker_id=worker_id)
        )
        await self.db.execute(stmt)
        await self.db.commit()

    # ---------------------------------------------------------
    # CREATE / UPDATE / DELETE
    # ---------------------------------------------------------
    @handle_exceptions()
    async def create(self, worker_data: WorkerSchema.Create) -> WorkerT:
        data = worker_data.model_dump()
        data["password_hash"] = PasswordService.hash(data.pop("password"))

        worker = Worker(**data)
        self.db.add(worker)
        await self.db.commit()
        await self.db.refresh(worker)
        return cast(WorkerT, worker)

    @handle_exceptions()
    async def update(self, worker_id: UUID, worker_data: WorkerSchema.Update) -> WorkerT:
        worker = await self.get_by_id(worker_id)

        for key, value in worker_data.model_dump(exclude_unset=True).items():
            setattr(worker, key, value)

        await self.db.commit()
        await self.db.refresh(worker)
        return cast(WorkerT, worker)

    @handle_exceptions()
    async def delete(self, worker_id: UUID) -> WorkerT:
        worker = await self.get_by_id(worker_id)
        await self.db.delete(worker)
        await self.db.commit()
        return cast(WorkerT, worker)

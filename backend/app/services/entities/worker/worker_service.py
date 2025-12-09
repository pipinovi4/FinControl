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
    Async service for handling CRUD and assignment operations related to Worker users,
    updated for Application-based architecture.

    Methods:
        - get_by_id(worker_id)
        - get_by_username(username)
        - get_by_email(email)
        - get_applications(worker_id)
        - update_username(worker_id, new_username)
        - assign_application(worker_id, application_id)
        - unassign_application(worker_id, application_id)
        - bulk_assign_applications(worker_id, application_ids)
        - create(worker_data)
    """

    def __init__(self, db: AsyncSession):
        super().__init__(db)
        self.db = db

    # -------------------------------------------------------------
    # BASIC GETTERS
    # -------------------------------------------------------------
    @handle_exceptions(raise_404=True)
    async def get_by_id(self, worker_id: UUID) -> WorkerT | None:
        """
        Fetch Worker by UUID including related Applications and Credits.
        """
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
        """
        Fetch Worker by username.
        """
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
        """
        Fetch Worker by email.
        """
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

    # -------------------------------------------------------------
    # APPLICATIONS
    # -------------------------------------------------------------
    @handle_exceptions()
    async def get_applications(self, worker_id: UUID) -> Sequence[Application]:
        """
        Return all applications assigned to a Worker.
        """
        stmt = select(Application).where(Application.worker_id == worker_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    # -------------------------------------------------------------
    # UPDATE WORKER
    # -------------------------------------------------------------
    @handle_exceptions()
    async def update_username(self, worker_id: UUID, new_username: str) -> None:
        stmt = (
            update(Worker)
            .where(Worker.id == worker_id)
            .values(username=new_username)
        )
        await self.db.execute(stmt)
        await self.db.commit()

    # -------------------------------------------------------------
    # ASSIGN / UNASSIGN APPLICATIONS
    # -------------------------------------------------------------
    @handle_exceptions()
    async def assign_application(self, worker_id: UUID, application_id: UUID) -> None:
        """
        Assign an application to a worker.
        """
        stmt = (
            update(Application)
            .where(Application.id == application_id)
            .values(worker_id=worker_id)
        )
        await self.db.execute(stmt)
        await self.db.commit()

    @handle_exceptions()
    async def unassign_application(self, worker_id: UUID, application_id: UUID) -> None:
        """
        Unassign an application ONLY if it currently belongs to this worker.
        """
        stmt = select(Application).where(Application.id == application_id)
        res = await self.db.execute(stmt)
        app = res.scalar_one_or_none()

        if app and app.worker_id == worker_id:
            stmt = (
                update(Application)
                .where(Application.id == application_id)
                .values(worker_id=None)
            )
            await self.db.execute(stmt)
            await self.db.commit()

    @handle_exceptions()
    async def bulk_assign_applications(self, worker_id: UUID, application_ids: list[UUID]) -> None:
        """
        Assign many applications to a worker at once.
        """
        stmt = (
            update(Application)
            .where(Application.id.in_(application_ids))
            .values(worker_id=worker_id)
        )
        await self.db.execute(stmt)
        await self.db.commit()

    # -------------------------------------------------------------
    # CREATE WORKER
    # -------------------------------------------------------------
    @handle_exceptions()
    async def create(self, worker_data: WorkerSchema.Create) -> WorkerT:
        """
        Create a new Worker with hashed password.
        """
        data = worker_data.model_dump()
        data["password_hash"] = PasswordService.hash(data.pop("password"))

        worker = Worker(**data)
        self.db.add(worker)
        await self.db.commit()
        await self.db.refresh(worker)
        return cast(WorkerT, worker)

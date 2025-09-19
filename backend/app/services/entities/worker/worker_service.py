from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select, update
from uuid import UUID
from typing import Sequence, cast, TypeVar

from backend.app.models import Worker, Client
from backend.app.services.auth import PasswordService
from backend.app.services.entities import UserService
from backend.app.utils.decorators import handle_exceptions
from backend.app.schemas.entities.worker_schema import WorkerSchema

WorkerT = TypeVar("WorkerT", bound=Worker)


class WorkerService(UserService):
    """
    Async service for handling all CRUD and assignment operations related to Worker users.

    Methods:
        - get_by_id(worker_id): Get Worker by UUID.
        - get_by_username(username): Get Worker by username.
        - get_clients(worker_id): Return all clients assigned to a Worker.
        - update_username(worker_id, new_username): Update Worker.username field.
        - assign_client(worker_id, client_id): Assign a specific client to a worker.
        - unassign_client(worker_id, client_id): Unassign a client from a worker.
        - bulk_assign_clients(worker_id, client_ids): Assign multiple clients to a worker.
        - create(worker_data): Create new Worker instance in DB.
        - update(worker_id, worker_data): Update an existing Worker with new data.
        - delete(worker_id): Hard-delete a Worker from the DB.
    """

    def __init__(self, db: AsyncSession):
        super().__init__(db)
        self.db = db

    @handle_exceptions(raise_404=True)
    async def get_by_id(self, worker_id: UUID) -> WorkerT | None:
        """
        Fetch a worker by UUID.
        Raises 404 if not found.
        """
        stmt = select(Worker).where(Worker.id == worker_id)
        stmt = stmt.options(
            selectinload(Worker.clients),
            selectinload(Worker.credits)
        )
        result = await self.db.execute(stmt)
        return cast(WorkerT, result.scalar_one_or_none())

    @handle_exceptions()
    async def get_by_username(self, username: str) -> WorkerT | None:
        """
        Fetch a worker by their system username.
        """
        stmt = select(Worker).where(Worker.username == username)
        stmt = stmt.options(
            selectinload(Worker.clients),
            selectinload(Worker.credits)
        )
        result = await self.db.execute(stmt)
        return cast(WorkerT, result.scalar_one_or_none())

    @handle_exceptions()
    async def get_by_email(self, email: str) -> WorkerT | None:
        """
        Fetch a worker by their email.
        """
        stmt = select(Worker).where(Worker.email == email)
        stmt = stmt.options(
            selectinload(Worker.clients),
            selectinload(Worker.credits)
        )
        result = await self.db.execute(stmt)
        return cast(WorkerT, result.scalar_one_or_none())

    @handle_exceptions()
    async def get_clients(self, worker_id: UUID) -> Sequence[Client]:
        """
        Retrieve all clients assigned to the given worker.
        """
        stmt = select(Client).where(Client.worker_id == worker_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    @handle_exceptions()
    async def update_username(self, worker_id: UUID, new_username: str) -> None:
        """
        Update the username of a worker.
        """
        stmt = update(Worker).where(Worker.id == worker_id).values(username=new_username)
        await self.db.execute(stmt)
        await self.db.commit()


    @handle_exceptions()
    async def assign_client(self, worker_id: UUID, client_id: UUID) -> None:
        """
        Assign a client to a specific worker.
        """
        stmt = update(Client).where(Client.id == client_id).values(worker_id=worker_id)
        await self.db.execute(stmt)
        await self.db.commit()

    @handle_exceptions()
    async def unassign_client(self, worker_id: UUID, client_id: UUID) -> None:
        """
        Unassign a client from a worker if they are currently linked.
        """
        stmt = select(Client).where(Client.id == client_id)
        result = await self.db.execute(stmt)
        client = result.scalar_one_or_none()
        if client and client.worker_id == worker_id:
            stmt = update(Client).where(Client.id == client_id).values(worker_id=None)
            await self.db.execute(stmt)
            await self.db.commit()

    @handle_exceptions()
    async def bulk_assign_clients(self, worker_id: UUID, client_ids: list[UUID]) -> None:
        """
        Assign multiple clients to a worker in a single batch update.
        """
        stmt = update(Client).where(Client.id.in_(client_ids)).values(worker_id=worker_id)
        await self.db.execute(stmt)
        await self.db.commit()

    @handle_exceptions()
    async def create(self, worker_data: WorkerSchema.Create) -> WorkerT:
        """
        Create a new Worker user. Hashes the password before saving.
        """
        updated_worker_data = worker_data.model_dump()
        updated_worker_data["password_hash"] = PasswordService.hash(updated_worker_data.pop("password"))
        worker = Worker(**updated_worker_data)
        self.db.add(worker)
        await self.db.commit()
        await self.db.refresh(worker)
        return cast(WorkerT, worker)

    @handle_exceptions()
    async def update(self, worker_id: UUID, worker_data: WorkerSchema.Update) -> WorkerT:
        """
        Update an existing worker using the provided schema data.
        Only non-null fields are applied.
        """
        worker = await self.get_by_id(worker_id)
        for key, value in worker_data.model_dump(exclude_unset=True).items():
            setattr(worker, key, value)
        await self.db.commit()
        await self.db.refresh(worker)
        return cast(WorkerT, worker)

    @handle_exceptions()
    async def delete(self, worker_id: UUID) -> WorkerT:
        """
        Hard delete a worker from the database.
        """
        worker = await self.get_by_id(worker_id)
        await self.db.delete(worker)
        await self.db.commit()
        return cast(WorkerT, worker)

"""
WorkerService handles operations related to Worker users.

Methods:
    get_worker_by_id(worker_id): Get worker by UUID, raise 404 if not found.
    get_by_username(username): Get worker by internal username.
    get_clients(worker_id): Get all clients assigned to a worker.
    update_username(worker_id, new_username): Change worker's username.
    update_telegram_username(worker_id, telegram_username): Update Telegram tag.
    assign_client(worker_id, client_id): Assign a client to worker.
    unassign_client(worker_id, client_id): Remove client from worker.
    bulk_assign_clients(worker_id, client_ids): Assign multiple clients.
    create_worker(worker_data): Create a new worker.
    update_worker(worker_id, worker_data): Update existing worker fields.
    delete_worker(worker_id): Hard delete worker from DB.
"""

from sqlalchemy.orm import Session
from uuid import UUID
from typing import Sequence, cast, TypeVar

from backend.app.models import Worker, Client
from backend.app.services.entities import UserService
from backend.app.utils.decorators import handle_exceptions

WorkerT = TypeVar("WorkerT", bound=Worker)


class WorkerService(UserService):
    def __init__(self, db: Session):
        super().__init__(db)
        self.db = db

    # --- GETTERS ---

    @handle_exceptions(raise_404=True)
    def get_worker_by_id(self, worker_id: UUID) -> WorkerT | None:
        return cast(WorkerT, self.db.query(Worker).filter(Worker.id == worker_id).first())

    @handle_exceptions()
    def get_by_username(self, username: str) -> WorkerT | None:
        return cast(WorkerT, self.db.query(Worker).filter(Worker.username == username).first())

    @handle_exceptions(default_return=[])
    def get_clients(self, worker_id: UUID) -> Sequence[Client]:
        worker = self.get_worker_by_id(worker_id)
        return cast(Sequence[Client], worker.clients if worker else [])

    # --- UPDATES ---

    @handle_exceptions()
    def update_username(self, worker_id: UUID, new_username: str) -> None:
        self.db.query(Worker).filter(Worker.id == worker_id).update({"username": new_username})
        self.db.commit()

    @handle_exceptions()
    def update_telegram_username(self, worker_id: UUID, telegram_username: str) -> None:
        self.db.query(Worker).filter(Worker.id == worker_id).update({"telegram_username": telegram_username})
        self.db.commit()

    # --- CLIENT MANAGEMENT ---

    @handle_exceptions()
    def assign_client(self, worker_id: UUID, client_id: UUID) -> None:
        self.db.query(Client).filter(Client.id == client_id).update({"worker_id": worker_id})
        self.db.commit()

    @handle_exceptions()
    def unassign_client(self, worker_id: UUID, client_id: UUID) -> None:
        client = self.db.query(Client).filter(Client.id == client_id).first()
        if client and client.worker_id == worker_id:
            self.db.query(Client).filter(Client.id == client_id).update({"worker_id": None})
            self.db.commit()

    # --- BULK ---

    @handle_exceptions()
    def bulk_assign_clients(self, worker_id: UUID, client_ids: list[UUID]) -> None:
        self.db.query(Client).filter(Client.id.in_(client_ids)).update(
            {"worker_id": worker_id}, synchronize_session=False
        )
        self.db.commit()

    # --- CRUD ---

    @handle_exceptions()
    def create_worker(self, worker_data: dict) -> WorkerT:
        worker = Worker(**worker_data)
        self.db.add(worker)
        self.db.commit()
        self.db.refresh(worker)
        return cast(WorkerT, worker)

    @handle_exceptions()
    def update_worker(self, worker_id: UUID, worker_data: dict) -> WorkerT:
        worker = self.get_worker_by_id(worker_id)
        for key, value in worker_data.items():
            setattr(worker, key, value)
        self.db.commit()
        self.db.refresh(worker)
        return cast(WorkerT, worker)

    @handle_exceptions()
    def delete_worker(self, worker_id: UUID) -> WorkerT:
        worker = self.get_worker_by_id(worker_id)
        self.db.delete(worker)
        self.db.commit()
        return cast(WorkerT, worker)

from sqlalchemy.orm import Session
from uuid import UUID
from typing import Sequence, cast, TypeVar

from backend.app.models import Worker, Client
from backend.app.services.entities import UserService
from backend.app.utils.decorators import handle_exceptions
from backend.app.schemas.entities.Worker import WorkerSchema  # Імпорт схем

WorkerT = TypeVar("WorkerT", bound=Worker)


class WorkerService(UserService):
    def __init__(self, db: Session):
        super().__init__(db)
        self.db = db

    @handle_exceptions(raise_404=True)
    def get_by_id(self, worker_id: UUID) -> WorkerT | None:
        return cast(WorkerT, self.db.query(Worker).filter(Worker.id == worker_id).first())

    @handle_exceptions()
    def get_by_username(self, username: str) -> WorkerT | None:
        return cast(WorkerT, self.db.query(Worker).filter(Worker.username == username).first())

    @handle_exceptions(default_return=[])
    def get_clients(self, worker_id: UUID) -> Sequence[Client]:
        worker = self.get_worker_by_id(worker_id)
        return cast(Sequence[Client], worker.clients if worker else [])

    @handle_exceptions()
    def update_username(self, worker_id: UUID, new_username: str) -> None:
        self.db.query(Worker).filter(Worker.id == worker_id).update({"username": new_username})
        self.db.commit()

    @handle_exceptions()
    def update_telegram_username(self, worker_id: UUID, telegram_username: str) -> None:
        self.db.query(Worker).filter(Worker.id == worker_id).update({"telegram_username": telegram_username})
        self.db.commit()

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

    @handle_exceptions()
    def bulk_assign_clients(self, worker_id: UUID, client_ids: list[UUID]) -> None:
        self.db.query(Client).filter(Client.id.in_(client_ids)).update(
            {"worker_id": worker_id}, synchronize_session=False
        )
        self.db.commit()

    @handle_exceptions()
    def create(self, worker_data: WorkerSchema.Create) -> WorkerT:
        worker = Worker(**worker_data.model_dump())
        self.db.add(worker)
        self.db.commit()
        self.db.refresh(worker)
        return cast(WorkerT, worker)

    @handle_exceptions()
    def update(self, worker_id: UUID, worker_data: WorkerSchema.Update) -> WorkerT:
        worker = self.get_worker_by_id(worker_id)
        for key, value in worker_data.model_dump(exclude_unset=True).items():
            setattr(worker, key, value)
        self.db.commit()
        self.db.refresh(worker)
        return cast(WorkerT, worker)

    @handle_exceptions()
    def delete(self, worker_id: UUID) -> WorkerT:
        worker = self.get_worker_by_id(worker_id)
        self.db.delete(worker)
        self.db.commit()
        return cast(WorkerT, worker)

from sqlalchemy.orm import Session
from typing import Sequence, TypeVar, cast
from uuid import UUID

from backend.app.models.entities import Broker, Client
from backend.app.permissions import PermissionRole
from backend.app.utils.decorators import handle_exceptions
from backend.app.schemas.entities.Broker import BrokerSchema  # імпорт схеми

BrokerT = TypeVar("BrokerT", bound=Broker)


class BrokerService:
    def __init__(self, db: Session):
        self.db = db

    @handle_exceptions(raise_404=True)
    def get_broker_by_id(self, broker_id: UUID) -> BrokerT:
        return cast(BrokerT, self.db.query(Broker).filter_by(id=broker_id, is_deleted=False).first())

    @handle_exceptions(default_return=[])
    def get_all_brokers(self) -> Sequence[BrokerT]:
        return cast(Sequence[BrokerT], self.db.query(Broker).filter_by(role=PermissionRole.BROKER).all())

    @handle_exceptions()
    def create_broker(self, broker_data: BrokerSchema.Create) -> Broker:
        broker = Broker(**broker_data.model_dump())
        self.db.add(broker)
        self.db.commit()
        self.db.refresh(broker)
        return broker

    @handle_exceptions()
    def update_broker(self, broker_id: UUID, updates: BrokerSchema.Update) -> Broker:
        broker = self.get_broker_by_id(broker_id)
        for key, value in updates.model_dump(exclude_unset=True).items():
            setattr(broker, key, value)
        self.db.commit()
        self.db.refresh(broker)
        return broker

    @handle_exceptions()
    def delete_broker(self, broker_id: UUID) -> Broker:
        broker = self.get_broker_by_id(broker_id)
        self.db.delete(broker)
        self.db.commit()
        return broker

    @handle_exceptions(default_return=[])
    def get_broker_clients(self, broker_id: UUID) -> Sequence[Client]:
        return self.db.query(Client).filter(Client.broker_id == broker_id, Client.is_deleted == False).all()

    @handle_exceptions()
    def remove_client_from_broker(self, client_id: UUID) -> Client:
        client = self.db.query(Client).filter_by(id=client_id).first()
        if client:
            client.broker_id = None
            self.db.commit()
            self.db.refresh(client)
        return client

    @handle_exceptions()
    def reassign_client_to_broker(self, client_id: UUID, new_broker_id: UUID) -> Client:
        client = self.db.query(Client).filter_by(id=client_id).first()
        if client:
            client.broker_id = new_broker_id
            self.db.commit()
            self.db.refresh(client)
        return client

    @handle_exceptions(default_return=0)
    def get_broker_clients_count(self, broker_id: UUID) -> int:
        return self.db.query(Client).filter(Client.broker_id == broker_id, Client.is_deleted == False).count()

    @handle_exceptions(default_return=False)
    def has_client(self, broker_id: UUID, client_id: UUID) -> bool:
        return self.db.query(Client).filter(
            Client.id == client_id,
            Client.broker_id == broker_id,
            Client.is_deleted == False
        ).first() is not None

    @handle_exceptions()
    def bulk_assign_clients(self, broker_id: UUID, client_ids: list[UUID]) -> None:
        self.db.query(Client).filter(Client.id.in_(client_ids)).update(
            {"broker_id": broker_id}, synchronize_session=False
        )
        self.db.commit()

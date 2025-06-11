from sqlalchemy.orm import Session
from typing import Sequence, TypeVar, cast
from uuid import UUID

from backend.app.models.entities import Broker, Client
from backend.app.permissions import PermissionRole
from backend.app.utils.decorators import handle_exceptions

BrokerT = TypeVar("BrokerT", bound=Broker)


class BrokerService:
    """
    Service for interacting with Broker entities.
    Provides methods for retrieving, updating, deleting and assigning clients.
    """

    def __init__(self, db: Session):
        self.db = db

    # --- GETTERS ---

    @handle_exceptions(raise_404=True)
    def get_broker_by_id(self, broker_id: UUID) -> BrokerT:
        """Retrieve a broker by UUID."""
        return cast(BrokerT, self.db.query(Broker).filter_by(id=broker_id, is_deleted=False).first())

    @handle_exceptions(default_return=[])
    def get_all_brokers(self) -> Sequence[BrokerT]:
        """Return all brokers."""
        return cast(Sequence[BrokerT], self.db.query(Broker).filter_by(role=PermissionRole.BROKER).all())

    # --- SETTERS ---

    @handle_exceptions()
    def create_broker(self, broker_data: dict) -> Broker:
        """Create a new broker."""
        broker = Broker(**broker_data)
        self.db.add(broker)
        self.db.commit()
        self.db.refresh(broker)
        return broker

    @handle_exceptions()
    def update_broker(self, broker_id: UUID, updates: dict) -> Broker:
        """Update broker's data."""
        broker = self.get_broker_by_id(broker_id)
        for key, value in updates.items():
            setattr(broker, key, value)
        self.db.commit()
        self.db.refresh(broker)
        return broker

    @handle_exceptions()
    def delete_broker(self, broker_id: UUID) -> Broker:
        """Permanently delete a broker."""
        broker = self.get_broker_by_id(broker_id)
        self.db.delete(broker)
        self.db.commit()
        return broker

    # --- CLIENT RELATIONS ---

    @handle_exceptions(default_return=[])
    def get_broker_clients(self, broker_id: UUID) -> Sequence[Client]:
        """
        Retrieve all clients assigned to the broker.
        """
        return self.db.query(Client).filter(Client.broker_id == broker_id, Client.is_deleted == False).all()

    @handle_exceptions()
    def remove_client_from_broker(self, client_id: UUID) -> Client:
        """
        Unassign a client from their broker (set broker_id to NULL).
        """
        client = self.db.query(Client).filter_by(id=client_id).first()
        if client:
            client.broker_id = None
            self.db.commit()
            self.db.refresh(client)
        return client

    @handle_exceptions()
    def reassign_client_to_broker(self, client_id: UUID, new_broker_id: UUID) -> Client:
        """
        Reassign a specific client to a different broker.
        """
        client = self.db.query(Client).filter_by(id=client_id).first()
        if client:
            client.broker_id = new_broker_id
            self.db.commit()
            self.db.refresh(client)
        return client

    @handle_exceptions(default_return=0)
    def get_broker_clients_count(self, broker_id: UUID) -> int:
        """
        Get total number of clients assigned to the broker.
        """
        return self.db.query(Client).filter(Client.broker_id == broker_id, Client.is_deleted == False).count()

    @handle_exceptions(default_return=False)
    def has_client(self, broker_id: UUID, client_id: UUID) -> bool:
        """
        Check whether a specific client is assigned to this broker.
        """
        return self.db.query(Client).filter(
            Client.id == client_id,
            Client.broker_id == broker_id,
            Client.is_deleted == False
        ).first() is not None

    # --- BULK ---

    @handle_exceptions()
    def bulk_assign_clients(self, broker_id: UUID, client_ids: list[UUID]) -> None:
        """Assign multiple clients to the given broker."""
        self.db.query(Client).filter(Client.id.in_(client_ids)).update(
            {"broker_id": broker_id}, synchronize_session=False
        )
        self.db.commit()

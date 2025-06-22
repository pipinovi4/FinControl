from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence, TypeVar, cast
from uuid import UUID

from backend.app.models.entities import Broker, Client
from backend.app.permissions import PermissionRole
from backend.app.services.entities import UserService
from backend.app.utils.decorators import handle_exceptions
from backend.app.schemas.entities.broker_schema import BrokerSchema

BrokerT = TypeVar("BrokerT", bound=Broker)


class BrokerService(UserService):
    """
    BrokerService handles all async CRUD operations for Broker users.

    Inherits:
        UserService – Provides shared user logic (e.g. deletion, querying)

    Public Methods:
        - get_by_id(broker_id): Fetch a specific Broker by UUID.
        - get_all_brokers(): Retrieve a list of all Brokers.
        - create(broker_data): Create a new Broker user.
        - update(broker_id, updates): Apply updates to an existing Broker.
        - delete(broker_id): Permanently delete Broker from database.
        - get_broker_clients(broker_id): List all clients linked to the broker.
        - remove_client_from_broker(client_id): Detach client from broker.
        - reassign_client_to_broker(client_id, new_broker_id): Move client to new broker.
        - get_broker_clients_count(broker_id): Get number of assigned clients.
        - has_client(broker_id, client_id): Check if broker has the specified client.
        - bulk_assign_clients(broker_id, client_ids): Assign multiple clients to broker.
    """

    def __init__(self, db: AsyncSession):
        super().__init__(db)
        self.db = db

    @handle_exceptions(raise_404=True)
    async def get_by_id(self, broker_id: UUID) -> BrokerT:
        result = await self.db.execute(
            select(Broker).where(Broker.id == broker_id, Broker.is_deleted == False)
        )
        return cast(BrokerT, result.scalar_one_or_none())

    @handle_exceptions(default_return=[])
    async def get_all_brokers(self) -> Sequence[BrokerT]:
        result = await self.db.execute(
            select(Broker).where(Broker.role == PermissionRole.BROKER)
        )
        return cast(Sequence[BrokerT], result.scalars().all())

    @handle_exceptions()
    async def create(self, broker_data: BrokerSchema.Create) -> Broker:
        broker = Broker(**broker_data.model_dump())
        self.db.add(broker)
        await self.db.commit()
        await self.db.refresh(broker)
        return broker

    @handle_exceptions()
    async def update(self, broker_id: UUID, updates: BrokerSchema.Update) -> Broker:
        broker = await self.get_by_id(broker_id)
        for key, value in updates.model_dump(exclude_unset=True).items():
            setattr(broker, key, value)
        await self.db.commit()
        await self.db.refresh(broker)
        return broker

    @handle_exceptions()
    async def delete(self, broker_id: UUID) -> Broker:
        broker = await self.get_by_id(broker_id)
        await self.db.delete(broker)
        await self.db.commit()
        return broker

    @handle_exceptions(default_return=[])
    async def get_broker_clients(self, broker_id: UUID) -> Sequence[Client]:
        result = await self.db.execute(
            select(Client).where(Client.broker_id == broker_id, Client.is_deleted == False)
        )
        return result.scalars().all()

    @handle_exceptions()
    async def remove_client_from_broker(self, client_id: UUID) -> Client:
        result = await self.db.execute(
            select(Client).where(Client.id == client_id)
        )
        client = result.scalar_one_or_none()
        if client:
            client.broker_id = None
            await self.db.commit()
            await self.db.refresh(client)
        return client

    @handle_exceptions()
    async def reassign_client_to_broker(self, client_id: UUID, new_broker_id: UUID) -> Client:
        result = await self.db.execute(
            select(Client).where(Client.id == client_id)
        )
        client = result.scalar_one_or_none()
        if client:
            client.broker_id = new_broker_id
            await self.db.commit()
            await self.db.refresh(client)
        return client

    @handle_exceptions(default_return=0)
    async def get_broker_clients_count(self, broker_id: UUID) -> int:
        result = await self.db.execute(
            select(Client).where(Client.broker_id == broker_id, Client.is_deleted == False)
        )
        return len(result.scalars().all())

    @handle_exceptions(default_return=False)
    async def has_client(self, broker_id: UUID, client_id: UUID) -> bool:
        result = await self.db.execute(
            select(Client).where(
                Client.id == client_id,
                Client.broker_id == broker_id,
                Client.is_deleted == False
            )
        )
        return result.scalar_one_or_none() is not None

    @handle_exceptions()
    async def bulk_assign_clients(self, broker_id: UUID, client_ids: list[UUID]) -> None:
        await self.db.execute(
            update(Client).where(Client.id.in_(client_ids)).values(broker_id=broker_id)
        )
        await self.db.commit()

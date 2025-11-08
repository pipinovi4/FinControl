from typing import Sequence, cast, TypeVar, Type
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models import Client
from app.services.auth import PasswordService
from app.services.entities import UserService
from app.utils.decorators import handle_exceptions
from app.schemas.entities.client_schema import ClientSchema

ClientT = TypeVar("ClientT", bound=Client)


class ClientService(UserService):
    """
    Async service for managing Client entities.

    Provides methods to retrieve, create, update, and delete clients.
    Inherits from the generic UserService.
    """

    def __init__(self, db: AsyncSession, client_model: Type[ClientT] = Client):
        """
        Initialize the service with a database session and client model.

        :param db: Async SQLAlchemy session.
        :param client_model: The ORM model to use (defaults to Client).
        """
        super().__init__(db)
        self.client_model = client_model

    @handle_exceptions(raise_404=True)
    async def get_by_id(self, client_id: UUID) -> ClientT | None:
        """
        Retrieve a client by its UUID.

        :param client_id: UUID of the client.
        :return: Client instance or None.
        """
        stmt = select(self.client_model).where(self.client_model.id == client_id, self.client_model.is_deleted == False)
        stmt = stmt.options(
            selectinload(Client.worker), selectinload(Client.broker), selectinload(Client.credits)
        )
        result = await self.db.execute(stmt)
        return cast(ClientT | None, result.scalar_one_or_none())

    @handle_exceptions()
    async def get_by_email(self, email: str) -> ClientT | None:
        """
        Fetch a client by their email.
        """
        stmt = select(Client).where(Client.email == email)
        stmt = stmt.options(
            selectinload(Client.worker), selectinload(Client.broker), selectinload(Client.credits)
        )
        result = await self.db.execute(stmt)
        return cast(ClientT, result.scalar_one_or_none())

    @handle_exceptions()
    async def get_all_clients(self, is_deleted: bool | None = None) -> Sequence[ClientT]:
        """
        Retrieve all clients, optionally filtering by deletion status.

        :param is_deleted: If specified, filters clients by deletion status.
        :return: List of Client instances.
        """
        stmt = select(self.client_model)
        if is_deleted is not None:
            stmt = stmt.where(self.client_model.is_deleted == is_deleted)
        result = await self.db.execute(stmt)
        return cast(Sequence[ClientT], result.scalars().all())

    @handle_exceptions()
    async def get_client_field(self, client_id: UUID, field_name: str) -> str | None:
        """
        Retrieve a specific field value from a client.

        :param client_id: UUID of the client.
        :param field_name: Name of the field.
        :return: Field value as string, or None.
        """
        client = await self.get_by_id(client_id)
        return getattr(client, field_name, None) if client else None

    @handle_exceptions()
    async def update_client_field(self, client_id: UUID, field_name: str, value: str) -> None:
        """
        Update a specific field for a client.

        :param client_id: UUID of the client.
        :param field_name: Field name to update.
        :param value: New value for the field.
        """
        client = await self.get_by_id(client_id)
        if client:
            setattr(client, field_name, value)
            await self.db.commit()

    @handle_exceptions()
    async def update_client_contact_info(self, client_id: UUID, full_name: str, phone_number: str, email: str) -> None:
        """
        Update contact information for a client.

        :param client_id: UUID of the client.
        :param full_name: New full name.
        :param phone_number: New phone number.
        :param email: New email address.
        """
        client = await self.get_by_id(client_id)
        if client:
            client.full_name = full_name
            client.phone_number = phone_number
            client.email = email
            await self.db.commit()

    @handle_exceptions()
    async def update_client_employment_info(self, client_id: UUID, workplace: str, position: str, income: str) -> None:
        """
        Update employment-related fields for a client.

        :param client_id: UUID of the client.
        :param workplace: New workplace name.
        :param position: New position.
        :param income: New income value.
        """
        client = await self.get_by_id(client_id)
        if client:
            client.workplace = workplace
            client.position = position
            client.income = income
            await self.db.commit()

    @handle_exceptions()
    async def create(self, client_data: ClientSchema.Create) -> ClientT:
        """
        Create a new Client user. Hashes the password before saving.
        """
        updated_client_data = client_data.model_dump()
        updated_client_data["password_hash"] = PasswordService.hash(updated_client_data.pop("password"))
        client = Client(**updated_client_data)
        self.db.add(client)
        await self.db.commit()
        await self.db.refresh(client)
        return cast(ClientT, client)

    @handle_exceptions()
    async def update(self, client_id: UUID, client_data: ClientSchema.Update) -> ClientT:
        """
        Update an existing client's fields.

        :param client_id: UUID of the client.
        :param client_data: Schema with updated client data.
        :return: Updated Client instance.
        """
        client = await self.get_by_id(client_id)
        for key, value in client_data.model_dump(exclude_unset=True).items():
            setattr(client, key, value)
        await self.db.commit()
        await self.db.refresh(client)
        return client

    @handle_exceptions()
    async def delete(self, client_id: UUID) -> ClientT:
        """
        Permanently delete a client from the database.

        :param client_id: UUID of the client.
        :return: Deleted Client instance.
        """
        client = await self.get_by_id(client_id)
        await self.db.delete(client)
        await self.db.commit()
        return client

from typing import Sequence, cast, TypeVar, Type
from sqlalchemy.orm import Session
from uuid import UUID

from backend.app.models import Client
from backend.app.services.entities import UserService
from backend.app.utils.decorators import handle_exceptions
from backend.app.schemas.entities.Client import ClientSchema

ClientT = TypeVar("ClientT", bound=Client)


class ClientServices(UserService):
    def __init__(self, db: Session, client_model: Type[ClientT] = Client):
        super().__init__(db)
        self.client_model = client_model

    @handle_exceptions(raise_404=True)
    def get_client_by_id(self, client_id: UUID) -> ClientT | None:
        return cast(ClientT | None,
                    self.db.query(self.client_model).filter_by(id=client_id, is_deleted=False).first())

    @handle_exceptions(default_return=[])
    def get_all_clients(self, is_deleted: bool | None = None) -> Sequence[ClientT]:
        query = self.db.query(self.client_model)
        if is_deleted is not None:
            query = query.filter_by(is_deleted=is_deleted)
        return cast(Sequence[ClientT], query.all())

    @handle_exceptions()
    def get_client_field(self, client_id: UUID, field_name: str) -> str | None:
        client = self.get_client_by_id(client_id)
        return getattr(client, field_name, None) if client else None

    @handle_exceptions()
    def update_client_field(self, client_id: UUID, field_name: str, value: str) -> None:
        client = self.get_client_by_id(client_id)
        if client:
            setattr(client, field_name, value)
            self.db.commit()

    @handle_exceptions()
    def update_client_contact_info(self, client_id: UUID, full_name: str, phone_number: str, email: str) -> None:
        client = self.get_client_by_id(client_id)
        if client:
            client.full_name = full_name
            client.phone_number = phone_number
            client.email = email
            self.db.commit()

    @handle_exceptions()
    def update_client_employment_info(self, client_id: UUID, workplace: str, position: str, income: str) -> None:
        client = self.get_client_by_id(client_id)
        if client:
            client.workplace = workplace
            client.position = position
            client.income = income
            self.db.commit()

    @handle_exceptions()
    def create_client(self, client_data: ClientSchema.Create) -> ClientT:
        client = Client(**client_data.model_dump())
        self.db.add(client)
        self.db.commit()
        self.db.refresh(client)
        return client

    @handle_exceptions()
    def update_client(self, client_id: UUID, client_data: ClientSchema.Update) -> ClientT:
        client = self.get_client_by_id(client_id)
        for key, value in client_data.model_dump(exclude_unset=True).items():
            setattr(client, key, value)
        self.db.commit()
        self.db.refresh(client)
        return client

    @handle_exceptions()
    def delete_client(self, client_id: UUID) -> ClientT:
        client = self.get_client_by_id(client_id)
        self.db.delete(client)
        self.db.commit()
        return client

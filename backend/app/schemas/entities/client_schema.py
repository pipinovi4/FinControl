# backend/app/schemas/entities/client_schema.py
from __future__ import annotations

from typing import Optional, List, Dict, Type, TYPE_CHECKING
from uuid import UUID
from pydantic import BaseModel, Field, EmailStr

from backend.app.schemas import SchemaBase
from backend.app.schemas.entities.credit_schema import CreditShort
from backend.app.schemas.entities.user_schema import UserSchema

if TYPE_CHECKING:
    from backend.app.schemas.entities.worker_schema import WorkerShort # noqa 401
    from backend.app.schemas.entities.broker_schema import BrokerShort # noqa 401
    from backend.app.schemas.entities.credit_schema import CreditShort # noqa 401


class ClientBase(UserSchema.Base):
    """
    Shared schema for the Client entity.
    """
    worker_id: Optional[UUID] = Field(None, description="UUID of the assigned worker")
    worker: Optional["WorkerShort"] = Field(None, description="Nested Worker (if assigned)")

    broker_id: Optional[UUID] = Field(None, description="UUID of the assigned broker")
    broker: Optional["BrokerShort"] = Field(None, description="Nested Broker (if assigned)")

    credits: Optional[List["CreditShort"]] = Field(
        None, description="List of client's credit records"
    )

    full_name: str = Field(..., example="Ivan Ivanov")
    phone_number: str = Field(..., example="+380931234567")
    email: str = Field(..., example="client@example.com")

    amount: Optional[str] = Field(None, example="10000")
    snils: Optional[str] = Field(None, example="123-456-789 00")
    inn: Optional[str] = Field(None, example="1234567890")
    reg_address: Optional[str] = Field(None, example="123 Main St")
    fact_address: Optional[str] = Field(None, example="123 Main St")
    reg_date: Optional[str] = Field(None, example="01.01.2020")
    family_status: Optional[str] = Field(None, example="Married")
    workplace: Optional[str] = Field(None, example="ACME Corp")
    org_legal_address: Optional[str] = Field(None, example="456 Elm St")
    org_fact_address: Optional[str] = Field(None, example="456 Elm St")
    position: Optional[str] = Field(None, example="Engineer")
    income: Optional[str] = Field(None, example="5000")
    income_proof: Optional[str] = Field(None, example="2-NDFL")
    employment_date: Optional[str] = Field(None, example="01.01.2020")
    org_activity: Optional[str] = Field(None, example="IT")
    assets: Optional[str] = Field(None, example="Yes")
    extra_income: Optional[str] = Field(None, example="Freelance")
    contact_person: Optional[str] = Field(None, example="Olga Petrova, +380631234567, sister")
    active_credit: int = Field(0, ge=0, example=100000)
    report_files: Optional[List[Dict]] = Field(None, description="Uploaded report file metadata")


class ClientCreate(UserSchema.Create):
    """
    Schema for registering a new Client.
    """
    worker_id: Optional[UUID] = Field(None)
    broker_id: Optional[UUID] = Field(None)
    full_name: str = Field(..., example="Ivan Ivanov")
    phone_number: str = Field(..., example="+380931234567")
    email: EmailStr = Field(..., example="client@example.com")
    amount: Optional[str] = Field(None, example="10000")
    snils: Optional[str] = Field(None, example="123-456-789 00")
    inn: Optional[str] = Field(None, example="1234567890")
    reg_address: Optional[str] = Field(None, example="123 Main St")
    fact_address: Optional[str] = Field(None, example="123 Main St")
    reg_date: Optional[str] = Field(None, example="01.01.2020")
    family_status: Optional[str] = Field(None, example="Married")
    workplace: Optional[str] = Field(None, example="ACME Corp")
    org_legal_address: Optional[str] = Field(None, example="456 Elm St")
    org_fact_address: Optional[str] = Field(None, example="456 Elm St")
    position: Optional[str] = Field(None, example="Engineer")
    income: Optional[str] = Field(None, example="5000")
    income_proof: Optional[str] = Field(None, example="2-NDFL")
    employment_date: Optional[str] = Field(None, example="01.01.2020")
    org_activity: Optional[str] = Field(None, example="IT")
    assets: Optional[str] = Field(None, example="Yes")
    extra_income: Optional[str] = Field(None, example="Freelance")
    contact_person: Optional[str] = Field(None, example="Olga Petrova, +380631234567, sister")
    report_files: Optional[List[Dict]] = Field(None)


class ClientUpdate(SchemaBase):
    """
    Schema for updating a Client.
    """
    worker_id: Optional[UUID] = Field(None)
    broker_id: Optional[UUID] = Field(None)
    full_name: Optional[str] = Field(None, example="Ivan Ivanov")
    phone_number: Optional[str] = Field(None, example="+380931234567")
    email: Optional[EmailStr] = Field(None, example="client@example.com")
    amount: Optional[str] = Field(None, example="10000")
    snils: Optional[str] = Field(None, example="123-456-789 00")
    inn: Optional[str] = Field(None, example="1234567890")
    reg_address: Optional[str] = Field(None, example="123 Main St")
    fact_address: Optional[str] = Field(None, example="123 Main St")
    reg_date: Optional[str] = Field(None, example="01.01.2020")
    family_status: Optional[str] = Field(None, example="Married")
    workplace: Optional[str] = Field(None, example="ACME Corp")
    org_legal_address: Optional[str] = Field(None, example="456 Elm St")
    org_fact_address: Optional[str] = Field(None, example="456 Elm St")
    position: Optional[str] = Field(None, example="Engineer")
    income: Optional[str] = Field(None, example="5000")
    income_proof: Optional[str] = Field(None, example="2-NDFL")
    employment_date: Optional[str] = Field(None, example="01.01.2020")
    org_activity: Optional[str] = Field(None, example="IT")
    assets: Optional[str] = Field(None, example="Yes")
    extra_income: Optional[str] = Field(None, example="Freelance")
    contact_person: Optional[str] = Field(None, example="Olga Petrova, +380631234567, sister")
    report_files: Optional[List[Dict]] = Field(None)


class ClientOut(ClientBase):
    """
    Public-facing schema for returning Client data.
    """
    pass

class ClientShort(BaseModel):
    id: UUID
    full_name: str
    phone_number: str
    email: str

class ClientSchema:
    Base:   Type[BaseModel] = ClientBase
    Create: Type[BaseModel] = ClientCreate
    Update: Type[BaseModel] = ClientUpdate
    Out:    Type[BaseModel] = ClientOut
    Short:  Type[BaseModel] = ClientShort


from importlib import import_module

_client_mod = import_module("backend.app.schemas.entities.broker_schema")
globals()["BrokerShort"] = _client_mod.BrokerSchema.Short
_client_mod = import_module("backend.app.schemas.entities.worker_schema")
globals()["WorkerShort"] = _client_mod.WorkerSchema.Short
_client_mod = import_module("backend.app.schemas.entities.credit_schema")
globals()["CreditShort"] = _client_mod.CreditSchema.Short
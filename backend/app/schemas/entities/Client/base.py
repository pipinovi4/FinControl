from typing import Optional, List, Dict
from uuid import UUID
from pydantic import Field
from backend.app.schemas.entities.User import UserSchema
from backend.app.schemas.entities.Worker import WorkerSchema
from backend.app.schemas.entities.Broker import BrokerSchema


class ClientBase(UserSchema.Base):
    """
    Shared schema for the Client entity.

    Inherits:
      - UserSchema.Base           (id, created_at, updated_at, full_name, telegram info)

    Adds client-specific profile fields.
    """
    worker_id: Optional[UUID] = Field(
        None,
        description="UUID of the assigned worker (if any)"
    )

    worker: Optional[WorkerSchema.Base]= Field(
        None,
        description="Full nested Worker schema if assigned"
    )

    broker_id: Optional[UUID] = Field(
        None,
        description="UUID of the assigned broker (if any)"
    )

    broker: Optional[BrokerSchema.Base]= Field(
        None,
        description="Full nested Broker schema if assigned"
    )

    # Contact & identity
    full_name: str = Field(..., example="Ivan Ivanov", description="Client’s full legal name")
    phone_number: str = Field(..., example="+380931234567", description="Contact phone number")
    email: str = Field(..., example="client@example.com", description="Contact email address")
    # Questionnaire
    amount: Optional[str] = Field(None, example="10000", description="Requested loan amount")
    snils: Optional[str] = Field(None, example="123-456-789 00", description="Social security number (SNILS)")
    inn: Optional[str] = Field(None, example="1234567890", description="Taxpayer ID (INN)")
    reg_address: Optional[str] = Field(None, example="123 Main St", description="Registered residential address")
    fact_address: Optional[str] = Field(None, example="123 Main St", description="Actual residential address")
    reg_date: Optional[str] = Field(None, example="01.01.2020", description="Registration date (dd.mm.yyyy)")
    family_status: Optional[str] = Field(None, example="Married", description="Marital status")
    workplace: Optional[str] = Field(None, example="ACME Corp", description="Employer name")
    org_legal_address: Optional[str] = Field(None, example="456 Elm St", description="Employer legal address")
    org_fact_address: Optional[str] = Field(None, example="456 Elm St", description="Employer actual address")
    position: Optional[str] = Field(None, example="Engineer", description="Job position")
    income: Optional[str] = Field(None, example="5000", description="Monthly net income")
    income_proof: Optional[str] = Field(None, example="2-NDFL", description="Income proof method")
    employment_date: Optional[str] = Field(None, example="01.01.2020", description="Employment start date")
    org_activity: Optional[str] = Field(None, example="IT", description="Industry/sector of employer")
    assets: Optional[str] = Field(None, example="Yes", description="Presence of assets")
    extra_income: Optional[str] = Field(None, example="Freelance", description="Additional income sources")
    contact_person: Optional[str] = Field(
        None,
        example="Olga Petrova, +7631234567, sister",
        description="Emergency contact (name, phone, relation)"
    )
    report_files: Optional[List[Dict]] = Field(
        None,
        description="List of uploaded report file metadata (e.g. JSONB payloads)"
    )

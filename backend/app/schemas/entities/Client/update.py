from typing import Optional, List, Dict
from uuid import UUID
from pydantic import Field, EmailStr

from backend.app.schemas.entities import UserSchema


class ClientUpdate(UserSchema.Update):
    """
    Schema for updating an existing client.

    All fields optional; only provided ones will be updated.
    """
    worker_id: Optional[UUID] = Field(None, description="UUID of the assigned worker")
    broker_id: Optional[UUID] = Field(None, description="UUID of the assigned broker")
    full_name: Optional[str] = Field(None, example="Ivan Ivanov", description="Client’s full legal name")
    phone_number: Optional[str] = Field(None, example="+380931234567", description="Contact phone number")
    email: Optional[EmailStr] = Field(None, example="client@example.com", description="Contact email address")
    amount: Optional[str] = Field(None, example="10000", description="Requested loan amount")
    snils: Optional[str] = Field(None, example="123-456-789 00", description="Social security number")
    inn: Optional[str] = Field(None, example="1234567890", description="Taxpayer ID")
    reg_address: Optional[str] = Field(None, example="123 Main St", description="Registered residential address")
    fact_address: Optional[str] = Field(None, example="123 Main St", description="Actual residential address")
    reg_date: Optional[str] = Field(None, example="01.01.2020", description="Registration date")
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
        example="Olga Petrova, +380631234567, sister",
        description="Emergency contact (name, phone, relation)"
    )
    report_files: Optional[List[Dict]] = Field(
        None,
        description="List of uploaded report file metadata"
    )

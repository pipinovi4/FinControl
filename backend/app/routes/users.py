from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import uuid4
from pydantic import BaseModel, EmailStr

from backend.db.session import get_db
from backend.app.models.entities.admin import Admin
from backend.app.models.entities.client import Client
from backend.app.models.entities.broker import Broker
from backend.app.models.entities.worker import Worker
from backend.app.permissions.enums import PermissionRole
from backend.app.schemas.entities.Client import ClientSchema
from backend.app.schemas.entities.Admin import AdminSchema
from backend.app.schemas.entities.Worker import WorkerSchema
from backend.app.schemas.entities.Broker import BrokerSchema

router = APIRouter(prefix="/users", tags=["Users"])


# --- SCHEMAS --- #
class AdminCreate(BaseModel):
    email: EmailStr
    telegram_id: str
    telegram_username: str
    is_active: bool


class BrokerCreate(BaseModel):
    email: EmailStr
    telegram_id: str
    telegram_username: str
    is_active: bool
    company_name: str
    region: list[str]


class WorkerCreate(BaseModel):
    email: EmailStr
    telegram_id: str
    telegram_username: str
    is_active: bool
    username: str


class ClientCreate(BaseModel):
    email: EmailStr
    telegram_id: str
    telegram_username: str
    is_active: bool
    full_name: str
    phone_number: str


# --- ROUTES --- #

@router.post("/admin", summary="Create Admin")
def create_admin(user: AdminSchema.Create, db: Session = Depends(get_db)):
    admin = Admin(
        id=uuid4(),
        telegram_id=user.telegram_id,
        telegram_username=user.telegram_username,
        role=PermissionRole.ADMIN,
        is_active=user.is_active,
        display_name=user.display_name,
        is_super_admin=user.is_super_admin,
        password_hash=user.password_hash,
        email=str(user.email),
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return {"msg": "Admin created!", "user": admin}


@router.post("/broker", summary="Create Broker")
def create_broker(user: BrokerSchema.Create, db: Session = Depends(get_db)):
    print(user.__dict__)
    broker = Broker(
        id=uuid4(),
        telegram_id=user.telegram_id,
        telegram_username=user.telegram_username,
        role=PermissionRole.BROKER,
        is_active=user.is_active,
        company_name=user.company_name,
        region=user.region,
        email=str(user.email),
        password_hash=user.password,
    )
    db.add(broker)
    db.commit()
    db.refresh(broker)
    return {"msg": "Broker created!", "user": broker}


@router.post("/worker", summary="Create Worker")
def create_worker(user: WorkerSchema.Create, db: Session = Depends(get_db)):
    worker = Worker(
        id=uuid4(),
        telegram_username=user.telegram_username,
        role=PermissionRole.WORKER,
        username=user.username,
        password_hash=user.password,
        telegram_id=user.telegram_id,
        email=str(user.email),
        is_active=user.is_active,
    )
    db.add(worker)
    db.commit()
    db.refresh(worker)
    return {"msg": "Worker created!", "user": worker}


@router.post("/client", summary="Create Client")
def create_client(user: ClientSchema.Create, db: Session = Depends(get_db)):
    print(user.model_dump())
    client = Client(
        id=uuid4(),
        telegram_id=user.telegram_id,
        telegram_username=user.telegram_username,
        role=PermissionRole.CLIENT,
        is_active=user.is_active,
        full_name=user.full_name,
        phone_number=user.phone_number,
        email=str(user.email),
        amount=user.amount,
        snils=user.snils,
        inn=user.inn,
        reg_address=user.reg_address,
        fact_address=user.fact_address,
        reg_date=user.reg_date,
        family_status=user.family_status,
        workplace=user.workplace,
        org_legal_address=user.org_legal_address,
        org_fact_address=user.org_fact_address,
        position=user.position,
        income=user.income,
        income_proof=user.income_proof,
        employment_date=user.employment_date,
        org_activity=user.org_activity,
        assets=user.assets,
        extra_income=user.extra_income,
        contact_person=user.contact_person,
        # якщо report_files обробляється окремо, можна зберегти тут user.report_files
    )
    db.add(client)
    db.commit()
    db.refresh(client)
    return {"msg": "Client created!", "user": client}

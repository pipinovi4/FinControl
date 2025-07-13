import uuid
from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UUID, String, Text, Integer
from sqlalchemy.dialects.postgresql import JSONB

from backend.app.models.entities.user import User
from backend.app.permissions.enums import PermissionRole
from backend.app.models.entities.credit import Credit
from backend.app.models.entities.earning import Earning

class Client(User):
    """
    SQLAlchemy model representing a client entity.

    A client is a user who applies for credit and is optionally associated with
    a broker and/or a worker. This model stores full identification, employment,
    and financial details required for credit assessment and processing.

    Inherits:
    - User: Provides base fields like ID, timestamps, and common authentication.
    """

    __tablename__ = 'clients'

    # Inherited primary key mapped to users table (joined-table inheritance)
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('users.id', ondelete='CASCADE'),
        primary_key=True
    )

    # Reference to the assigned worker (optional, may be null)
    worker_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('users.id', ondelete='SET NULL'),
        nullable=True
    )
    worker: Mapped["Worker"] = relationship(
        "Worker",
        foreign_keys=[worker_id],
        back_populates="clients"
    )

    # Timestamp when the worker took this client into processing
    taken_at_worker: Mapped[datetime] = mapped_column(nullable=True)

    # Reference to the assigned broker (optional, may be null)
    broker_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('users.id', ondelete='SET NULL'),
        nullable=True
    )
    broker: Mapped["Broker"] = relationship(
        "Broker",
        foreign_keys=[broker_id],
        back_populates="clients"
    )

    # Timestamp when the broker registered or forwarded this client
    taken_at_broker: Mapped[datetime] = mapped_column(nullable=True)

    # One-to-many relationship with client's credit history
    credits: Mapped[list["Credit"]] = relationship(
        "Credit", back_populates="client", cascade="all, delete-orphan"
    )

    # ========================
    # 📌 Personal Information
    # ========================
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    # =========================
    # 📌 Financial Questionnaire
    # =========================
    amount: Mapped[str] = mapped_column(String(50), nullable=True)
    snils: Mapped[str] = mapped_column(String(20), nullable=True)
    inn: Mapped[str] = mapped_column(String(20), nullable=True)

    # =========================
    # 📌 Address Information
    # =========================
    reg_address: Mapped[str] = mapped_column(Text, nullable=True)
    fact_address: Mapped[str] = mapped_column(Text, nullable=True)
    reg_date: Mapped[str] = mapped_column(String(20), nullable=True)

    # =========================
    # 📌 Family & Employment
    # =========================
    family_status: Mapped[str] = mapped_column(String(50), nullable=True)
    workplace: Mapped[str] = mapped_column(String(255), nullable=True)
    position: Mapped[str] = mapped_column(String(100), nullable=True)
    employment_date: Mapped[str] = mapped_column(String(20), nullable=True)
    income: Mapped[str] = mapped_column(String(100), nullable=True)
    income_proof: Mapped[str] = mapped_column(String(100), nullable=True)
    org_legal_address: Mapped[str] = mapped_column(Text, nullable=True)
    org_fact_address: Mapped[str] = mapped_column(Text, nullable=True)
    org_activity: Mapped[str] = mapped_column(String(100), nullable=True)

    # =========================
    # 📌 Additional Information
    # =========================
    assets: Mapped[str] = mapped_column(String(255), nullable=True)
    extra_income: Mapped[str] = mapped_column(String(255), nullable=True)
    contact_person: Mapped[str] = mapped_column(Text, nullable=True)

    # =========================
    # 📌 Credit Summary
    # =========================
    active_credit: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    report_files: Mapped[list[dict]] = mapped_column(JSONB, nullable=True)

    # Enables polymorphic identity for the Client role
    __mapper_args__ = {
        "inherit_condition": (id == User.id),
        "polymorphic_identity": PermissionRole.CLIENT,
    }

    def __repr__(self):
        """Developer-friendly string representation for debugging."""
        return f"<Client id={self.id} full_name={self.full_name} worker={self.worker}>"

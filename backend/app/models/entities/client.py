import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Text, Integer, CheckConstraint, DateTime
from sqlalchemy.dialects.postgresql import JSONB, UUID as PGUUID

from app.models.entities.user import User
from app.permissions.enums import PermissionRole

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

    # ⬇️ Головні інваріанти на рівні БД
    __table_args__ = (
        # числове поле не може бути від’ємним
        CheckConstraint('active_credit >= 0', name='ck_clients_active_credit_nonneg'),

        # не дозволяємо порожнє (тільки пробіли) ім’я
        CheckConstraint("char_length(btrim(full_name)) > 0", name='ck_clients_full_name_not_blank'),

        # базова E.164-перевірка для телефону (+XXXXXXXX...), 8–15 цифр
        CheckConstraint(r"phone_number ~ '^\+?[1-9]\d{7,14}$'", name='ck_clients_phone_e164'),

        # дуже базова валідація email (не ідеальна, але тримає формат)
        CheckConstraint(r"email ~ '^[^@\s]+@[^@\s]+\.[^@\s]+$'", name='ck_clients_email_basic'),

        # якщо є timestamp «взяв у роботу», має існувати worker_id
        CheckConstraint("(taken_at_worker IS NULL) OR (worker_id IS NOT NULL)",
                        name='ck_clients_worker_ts_consistency'),

        # якщо є timestamp від брокера, має існувати broker_id
        CheckConstraint("(taken_at_broker IS NULL) OR (broker_id IS NOT NULL)",
                        name='ck_clients_broker_ts_consistency'),
    )

    # Inherited primary key mapped to users table (joined-table inheritance)
    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey('users.id', ondelete='CASCADE'),
        primary_key=True
    )

    # Reference to the assigned worker (optional, may be null)
    worker_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey('workers.id', ondelete='SET NULL'),
        nullable=True,
        index=True,
    )
    worker: Mapped["Worker"] = relationship(
        "Worker",
        foreign_keys=[worker_id],
        back_populates="clients"
    )

    # Timestamp when the worker took this client into processing
    taken_at_worker: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    # Reference to the assigned broker (optional, may be null)
    broker_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey('brokers.id', ondelete='SET NULL'),
        nullable=True,
        index=True,
    )
    broker: Mapped["Broker"] = relationship(
        "Broker",
        foreign_keys=[broker_id],
        back_populates="clients"
    )

    # Timestamp when the broker registered or forwarded this client
    taken_at_broker: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    # One-to-many relationship with client's credit history
    credits: Mapped[list["Credit"]] = relationship(
        "Credit",
        back_populates="client",
        foreign_keys="Credit.client_id",
        cascade="all",
        passive_deletes=True,
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
    report_files: Mapped[Optional[list[dict]]] = mapped_column(
        JSONB,
        nullable=True,
        default=None
    )
    # Enables polymorphic identity for the Client role
    __mapper_args__ = {
        "inherit_condition": (id == User.id),
        "polymorphic_identity": PermissionRole.CLIENT,
    }

    def __repr__(self):
        """Developer-friendly string representation for debugging."""
        return f"<Client id={self.id} full_name={self.full_name} worker={self.worker}>"

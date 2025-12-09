from __future__ import annotations
from datetime import datetime
from enum import StrEnum
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, Numeric, Enum, DateTime, String, Text, text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

from db.session import Base
from app.models.mixins.soft_delete import SoftDeleteMixin


class CreditStatus(StrEnum):
    NEW = "new"              # Заявка створена, ще не оброблена
    APPROVED = "approved"    # Схвалено брокером (адмін перевіряє та заносить фінпараметри)
    REJECTED = "rejected"    # Відхилено (лікувати клієнта)
    TREATMENT = "treatment"  # В роботі з клієнтом (лікування)
    COMPLETED = "completed"  # Заявка завершена


class Credit(Base, SoftDeleteMixin):
    __tablename__ = "credits"

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,                         # Python-side (зручно в коді)
        server_default=text("gen_random_uuid()"),  # DB-side (надійно й уніфіковано)
        nullable=False,
    )
    application_id: Mapped[UUID] = mapped_column(ForeignKey("applications.id", ondelete="CASCADE"), nullable=False)
    broker_id: Mapped[UUID] = mapped_column(ForeignKey("brokers.id", ondelete="SET NULL"), nullable=True)
    worker_id: Mapped[UUID] = mapped_column(ForeignKey("workers.id", ondelete="SET NULL"), nullable=True)

    # сума із заявки (створює адмін)
    amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)

    # фінпараметри, які заповнює ТІЛЬКИ адмін після схвалення брокером
    approved_amount: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    monthly_payment: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    bank_name: Mapped[str | None] = mapped_column(String(120), nullable=True)
    first_payment_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    status: Mapped[CreditStatus] = mapped_column(
        Enum(CreditStatus, name="credit_status"),
        default=CreditStatus.NEW,
        nullable=False,
        index=True,
    )

    # issued_at: зберігаємо naive UTC (для стабільної роботи з Pydantic)
    issued_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        default=datetime.utcnow,
        nullable=False,
        index=True,
    )

    # єдиний довільно довгий коментар (брокер/адмін можуть переписувати)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    application = relationship("Application", back_populates="credits")
    broker = relationship("Broker", back_populates="credits")
    worker = relationship("Worker", back_populates="credits")

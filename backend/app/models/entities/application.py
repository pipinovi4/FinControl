import uuid
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, CheckConstraint, DateTime
from sqlalchemy.dialects.postgresql import JSONB, UUID as PGUUID

from app.models import UUIDMixin, SoftDeleteMixin
from db.session import Base


class Application(Base, UUIDMixin, SoftDeleteMixin):
    """
    Single credit application submitted by a Telegram user.
    Stores canonical JSON data from Wizard.
    """

    __tablename__ = "applications"

    __table_args__ = (
        CheckConstraint(
            "(taken_at_worker IS NULL) OR (worker_id IS NOT NULL)",
            name="ck_application_worker_ts"
        ),
        CheckConstraint(
            "(taken_at_broker IS NULL) OR (broker_id IS NOT NULL)",
            name="ck_application_broker_ts"
        ),
    )

    telegram_id: Mapped[int] = mapped_column(
        index=True,
        nullable=False
    )

    # ---------------------------------------------------------
    # Worker assignment
    # ---------------------------------------------------------
    worker_id: Mapped[uuid.UUID | None] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("workers.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    worker: Mapped["Worker"] = relationship(
        "Worker",
        foreign_keys=[worker_id],
        back_populates="applications"
    )

    taken_at_worker: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # ---------------------------------------------------------
    # Broker assignment
    # ---------------------------------------------------------
    broker_id: Mapped[uuid.UUID | None] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("brokers.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    broker: Mapped["Broker"] = relationship(
        "Broker",
        foreign_keys=[broker_id],
        back_populates="applications"
    )

    taken_at_broker: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # ---------------------------------------------------------
    # Main application data sent from Wizard (canonical)
    # ---------------------------------------------------------
    data: Mapped[dict] = mapped_column(JSONB, nullable=False)

    # ---------------------------------------------------------
    # Credit history (if needed)
    # ---------------------------------------------------------
    credits: Mapped[list["Credit"]] = relationship(
        "Credit",
        back_populates="application",
        foreign_keys="Credit.application_id",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self):
        return f"<Application id={self.id} telegram={self.telegram_id}>"

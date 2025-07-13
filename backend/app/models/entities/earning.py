from sqlalchemy import Date, Numeric

from backend.db.session import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from uuid import UUID
from datetime import date
from uuid import uuid4

class Earning(Base):
    __tablename__ = "earnings"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4
    )
    worker_id: Mapped[UUID] = mapped_column(
        ForeignKey("workers.id")
    )
    client_id: Mapped[UUID] = mapped_column(
        ForeignKey("clients.id")
    )

    date: Mapped[date] = mapped_column(Date, nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    worker: Mapped["Worker"] = relationship("Worker", back_populates="earnings")

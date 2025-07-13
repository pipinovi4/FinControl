# models/entities/credit.py

import uuid
from datetime import datetime, timedelta
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID, ForeignKey, Integer, String, DateTime
from backend.db.session import Base

class Credit(Base):
    __tablename__ = 'credits'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    client_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('clients.id', ondelete='CASCADE'),
        nullable=False
    )

    client: Mapped["Client"] = relationship("Client", back_populates="credits")

    broker_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('brokers.id', ondelete='CASCADE'),
        nullable=False
    )

    broker: Mapped["Broker"] = relationship("Broker", back_populates="credits")

    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    paid_amount: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active")
    issued_at: Mapped[datetime] = mapped_column(DateTime, nullable=False,     default=datetime.utcnow())
    last_payment_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    def __repr__(self):
        return (
            f"<Credit id={self.id} client_id={self.client_id} "
            f"total={self.total_amount} paid={self.paid_amount} status={self.status}>"
        )

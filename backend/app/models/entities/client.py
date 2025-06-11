import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UUID, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from backend.app.models.entities import User, Worker, Broker


class Client(User):
    """
    SQLAlchemy model for clients in the system.

    Inherits:
    - User: Base class with UUID primary key, timestamps, Telegram info, and role.

    Represents an individual applying for credit, assigned to a specific worker.
    Contains full personal, employment, and financial profile.
    """

    __tablename__ = 'clients'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('users.id', ondelete='CASCADE'),
        primary_key=True
    )
    # ForeignKey to base User table, following joined-table inheritance strategy

    worker_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('users.id', ondelete='SET NULL'),
        nullable=True
    )
    # Reference to the user who manages this client (must be of role Worker)

    worker: Mapped[Worker] = relationship(
        "Worker",
        foreign_keys=[worker_id],
        back_populates="clients"
    )
    # ORM relationship to the assigned worker (reverse via User.clients)

    broker_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('users.id', ondelete='SET NULL'),
        nullable=True
    )

    broker: Mapped[Broker] = relationship(
        "Broker",
        foreign_keys=[broker_id],
        back_populates="clients"
    )
    # ORM relationship to the assigned broker (reverse via User.clients)

    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    # Full legal name (e.g., from passport)

    phone_number: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    # Client's phone number (used for contact & deduplication)

    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    # Email for communication and document delivery

    # --- Additional questionnaire fields ---
    amount: Mapped[str] = mapped_column(String(50), nullable=True)
    # Requested loan amount

    snils: Mapped[str] = mapped_column(String(20), nullable=True)
    # Social security number (SNILS)

    inn: Mapped[str] = mapped_column(String(20), nullable=True)
    # Taxpayer identification number (INN)

    reg_address: Mapped[str] = mapped_column(Text, nullable=True)
    fact_address: Mapped[str] = mapped_column(Text, nullable=True)
    # Registered and actual residential addresses

    reg_date: Mapped[str] = mapped_column(String(20), nullable=True)
    # Date of registration (in format dd.mm.yyyy)

    family_status: Mapped[str] = mapped_column(String(50), nullable=True)
    # Marital status

    workplace: Mapped[str] = mapped_column(String(255), nullable=True)
    # Name of employer

    org_legal_address: Mapped[str] = mapped_column(Text, nullable=True)
    org_fact_address: Mapped[str] = mapped_column(Text, nullable=True)
    # Legal and actual addresses of employer

    position: Mapped[str] = mapped_column(String(100), nullable=True)
    # Job position

    income: Mapped[str] = mapped_column(String(100), nullable=True)
    # Monthly net income

    income_proof: Mapped[str] = mapped_column(String(100), nullable=True)
    # Method of income confirmation (e.g., 2-NDFL, statement)

    employment_date: Mapped[str] = mapped_column(String(20), nullable=True)
    # Employment start date (dd.mm.yyyy)

    org_activity: Mapped[str] = mapped_column(String(100), nullable=True)
    # Industry or sector of the employer

    assets: Mapped[str] = mapped_column(String(10), nullable=True)
    # Presence of assets (Yes/No)

    extra_income: Mapped[str] = mapped_column(String(255), nullable=True)
    # Any additional sources of income

    contact_person: Mapped[str] = mapped_column(Text, nullable=True)
    # Emergency contact (name, phone, relation)

    report_files: Mapped[list[dict]] = mapped_column(JSONB, nullable=True)
    # List of uploaded credit history report file IDs (can be JSON if Postgres)

    __mapper_args__ = {
        "polymorphic_identity": "client",
        "inherit_condition": (id == User.id),
    }
    # Enables SQLAlchemy polymorphic loading based on 'role' column in User

    def __repr__(self):
        """
        Developer-friendly string representation of a client object.
        """
        return f"<Client id={self.id} worker={self.worker}>"

import enum
import uuid
from sqlalchemy import String, Boolean, Enum as SQLEnum, text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column
from uuid import uuid4

from backend.db.session import Base
from app.models.mixins import TimeStampMixin, SoftDeleteMixin


class PromotionEnum(enum.Enum):
    HELIX = "HELIX"
    UNION = "UNION"
    GENERAL = "GENERAL"


class Promotion(Base, TimeStampMixin, SoftDeleteMixin):
    __tablename__ = "promotions"

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,                         # Python-side (зручно в коді)
        server_default=text("gen_random_uuid()"),  # DB-side (надійно й уніфіковано)
        nullable=False,
    )

    promotion_type: Mapped[PromotionEnum] = mapped_column(
        SQLEnum(
            PromotionEnum,
            name="promotion_enum",
            native_enum=True,
            create_type=True,
            validate_strings=True,
        ),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

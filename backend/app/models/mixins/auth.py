from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

class AuthMixin:
    """
    Mixin for email-password authentication.
    """
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

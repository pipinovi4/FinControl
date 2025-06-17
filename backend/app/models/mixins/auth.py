from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

class AuthMixin:
    """
    Mixin for traditional JWT-compatible email/password authentication.

    Fields:
    - email: used as primary login identifier
    - password_hash: securely stored password (e.g., bcrypt)

    Notes:
    - This mixin supports login via email & password.
    - JWT sessions are generated dynamically from these credentials — no need to store JWT in DB.
    - Use `AuthService` + `JWTService` for login/token logic.
    """
    __abstract__ = True

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

from typing import Optional
from passlib.context import CryptContext
from sqlalchemy.orm.session import Session

from backend.app.models.entities import Admin

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordService:
    """
    Service for handling password hashing, verification, and authentication of Admin users.

    Attributes:
        db (Session): SQLAlchemy session for database operations.
    """

    def __init__(self, db: Session):
        """
        Initialize PasswordService with a database session.

        Args:
            db (Session): SQLAlchemy session instance.
        """
        self.db = db

    @classmethod
    def hash(cls, password: str) -> str:
        """
        Hash a plaintext password using bcrypt.

        Args:
            password (str): The plaintext password to hash.

        Returns:
            str: The resulting bcrypt hash.
        """
        return pwd_ctx.hash(password)

    @staticmethod
    def verify(plain: str, hashed: str) -> bool:
        """
        Verify a plaintext password against a stored bcrypt hash.

        Args:
            plain (str): The plaintext password to verify.
            hashed (str): The bcrypt hash to compare against.

        Returns:
            bool: True if the plaintext matches the hash, False otherwise.
        """
        return pwd_ctx.verify(plain, hashed)

    def authenticate(self, email: str, password: str) -> Optional[Admin]:
        """
        Authenticate an Admin by email and password.

        This method looks up the Admin by email, verifies the provided password
        against the stored password_hash, and returns the Admin instance on success.

        Args:
            email (str): The Admin's login email.
            password (str): The plaintext password to authenticate.

        Returns:
            Optional[Admin]: The authenticated Admin instance if credentials are valid; otherwise, None.
        """
        admin = (
            self.db.query(Admin)
            .filter_by(email=email, is_deleted=False)
            .first()
        )
        if admin and self.verify(password, str(admin.password_hash)):
            return admin
        return None

from backend.app.services.auth.token_manager import TokenManager
from backend.app.services.smtp_service import SMTPService
from backend.app.services.entities.user.user_service import UserService
from backend.app.core.settings import settings

from sqlalchemy.orm import Session
from pydantic import EmailStr
from uuid import UUID
import secrets


class ResetPasswordService:
    """
    Handles password reset flow:
        1. Generates and emails a password reset token.
        2. Validates token and sets new password.

    Dependencies:
        - SMTPService: used to send reset link via email
        - TokenManager: encodes/decodes JWT with 'reset' type
        - UserService: fetches and updates user by email or ID
    """

    def __init__(self, db: Session):
        self.db = db
        self.smtp = SMTPService()
        self.user_service = UserService(db)

    def request_reset(self, email: EmailStr) -> None:
        """
        Generates a password reset token and sends it to the provided email.

        Args:
            email (EmailStr): User's registered email.

        Returns:
            None. Silently fails if no user is found.
        """
        user = self.user_service.get_user_by_email(email)
        if not user:
            return

        token = self._generate_token(user.id)
        self._send_reset_email(email, token)

    def reset_password(self, token: str, new_password: str) -> bool:
        """
        Validates the reset token and updates the password.

        Args:
            token (str): Reset token received via email.
            new_password (str): New password to be saved.

        Returns:
            bool: True if password was reset, False otherwise.
        """
        user_id = self._verify_token(token=token)
        if not user_id:
            return False

        self.user_service.update_password(user_id, new_password)
        return True

    # --------- helpers (private) ------------

    @staticmethod
    def _generate_token(user_id: UUID) -> str:
        """
        Generates a reset JWT for the given user ID.

        Args:
            user_id (UUID): User's unique identifier.

        Returns:
            str: Encoded JWT.
        """
        return TokenManager.encode(
            payload={"sub": str(user_id)},
            token_type="reset",
            ttl_minutes=settings.PASSWORD_RESET_TOKEN_TTL
        )

    @staticmethod
    def _verify_token(token: str) -> UUID | None:
        """
        Decodes and verifies the reset token.

        Args:
            token (str): JWT to decode.

        Returns:
            UUID | None: User ID if valid, otherwise None.

        Raises:
            ValueError: If token is invalid or not a reset token.
        """
        try:
            payload = TokenManager.decode(token, expected_type="reset")
            return UUID(payload["sub"])
        except ValueError:
            return None

    def _send_reset_email(self, email: EmailStr, token: str) -> None:
        """
        Sends the reset token via email.

        Args:
            email (EmailStr): Recipient's email.
            token (str): JWT token to include in the email.

        Returns:
            None
        """
        self.smtp.send_password_reset_email(to_email=email, reset_token=token)

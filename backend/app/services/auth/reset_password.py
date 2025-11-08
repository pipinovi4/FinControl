from app.services.auth.token_manager import TokenManager
from app.services.smtp_service import SMTPService
from app.services.entities.user.user_service import UserService
from app.core.settings import settings

from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr
from uuid import UUID

from app.utils.decorators import handle_route_exceptions


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

    def __init__(self, db: AsyncSession):
        self.db = db
        self.smtp = SMTPService()
        self.user_service = UserService(db)

    @handle_route_exceptions()
    async def request_reset(self, email: EmailStr) -> None:
        """
        Generates a password reset token and sends it to the provided email.
        Silently fails if no user is found.

        Args:
            email (EmailStr): User's registered email.
        """
        user = await self.user_service.get_user_by_email(email)
        if not user:
            return

        token = self._generate_token(user.id)
        await self._send_reset_email(email, token)

    @handle_route_exceptions()
    async def reset_password(self, token: str, new_password: str) -> bool:
        """
        Validates the reset token and updates the password.

        Args:
            token (str): Reset token received via email.
            new_password (str): New password to be saved.

        Returns:
            bool: True if password was reset, False otherwise.
        """
        user_id = self._verify_token(token)
        if not user_id:
            return False

        await self.user_service.update_password(user_id, new_password)
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
        """
        try:
            payload = TokenManager.decode(token, expected_type="reset")
            return UUID(payload["sub"])
        except ValueError:
            return None

    async def _send_reset_email(self, email: EmailStr, token: str) -> None:
        """
        Sends the reset token via email.

        Args:
            email (EmailStr): Recipient's email.
            token (str): JWT token to include in the email.
        """
        await self.smtp.send_password_reset_email(to_email=email, reset_token=token)

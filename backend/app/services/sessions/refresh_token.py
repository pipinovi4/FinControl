# backend/app/services/entities/refresh_token_service.py

from datetime import datetime, UTC, timedelta
from uuid import UUID
from hashlib import sha256
from sqlalchemy.orm import Session
import secrets

from backend.app.models.sessions.refresh_token import RefreshToken
from backend.app.utils.decorators import handle_exceptions

class RefreshTokenService:
    """
    Service layer for managing refresh token operations:
    creation, revocation, verification, and rotation.
    """

    def __init__(self, db: Session):
        self.db = db

    # ---- helpers -------------------------------------------------
    @staticmethod
    def _hash(raw: str) -> str:
        """
        Hashes the raw refresh token using SHA-256.
        """
        return sha256(raw.encode()).hexdigest()

    # ---- public --------------------------------------------------

    @handle_exceptions()
    def create(
        self,
        user_id: UUID,
        raw_token: str,
        ip: str | None,
        ua: str | None,
        ttl_days: int = 30,
    ):
        """
        Create a new refresh token in the database.
        """
        token_row = RefreshToken(
            user_id=user_id,
            token_hash=self._hash(raw_token),
            created_from_ip=ip,
            user_agent=ua,
            expires_at=datetime.now(UTC) + timedelta(days=ttl_days),
            is_active=True,
        )
        self.db.add(token_row)
        self.db.commit()
        self.db.refresh(token_row)

    @handle_exceptions()
    def revoke(self, token_hash: str) -> None:
        """
        Soft-revoke a refresh token by hash.
        """
        self.db.query(RefreshToken).filter_by(token_hash=token_hash).update(
            {"is_active": False}
        )
        self.db.commit()

    @handle_exceptions(default_return=None)
    def verify(self, raw_token: str) -> RefreshToken | None:
        """
        Check that a given raw token is active and not expired,
        returning the ORM instance or None.
        """
        hashed = self._hash(raw_token)
        return (
            self.db.query(RefreshToken)
            .filter(
                RefreshToken.token_hash == hashed,
                RefreshToken.is_active.is_(True),
                RefreshToken.expires_at > datetime.now(UTC),
            )
            .first()
        )

    @handle_exceptions()
    def rotate(
        self,
        stored_token: RefreshToken,
        ip: str | None,
        ua: str | None,
        ttl_days: int = 30,
    ) -> str:
        """
        Revoke the old token and issue a new one.
        """
        stored_token.is_active = False
        self.db.add(stored_token)

        raw_token = secrets.token_urlsafe(48)
        hashed = self._hash(raw_token)

        new_token = RefreshToken(
            user_id=stored_token.user_id,
            token_hash=hashed,
            created_from_ip=ip,
            user_agent=ua,
            expires_at=datetime.now(UTC) + timedelta(days=ttl_days),
            is_active=True,
        )
        self.db.add(new_token)
        self.db.commit()

        return raw_token

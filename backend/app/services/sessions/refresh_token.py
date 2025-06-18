# backend/app/services/entities/refresh_token_service.py
from datetime import datetime, UTC, timedelta
from uuid import UUID
from hashlib import sha256
from sqlalchemy.orm import Session

from backend.app.models.sessions.refresh_token import RefreshToken


class RefreshTokenService:
    def __init__(self, db: Session):
        self.db = db

    # ---- helpers -------------------------------------------------
    @staticmethod
    def _hash(raw: str) -> str:
        return sha256(raw.encode()).hexdigest()

    # ---- public --------------------------------------------------
    def create(
        self,
        user_id: UUID,
        raw_token: str,
        ip: str | None,
        ua: str | None,
        ttl_days: int = 30,
    ):
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

    def revoke(self, token_hash: str) -> None:
        """
        Soft-revoke a refresh token by hash.
        """
        self.db.query(RefreshToken).filter_by(token_hash=token_hash).update(
            {"is_active": False}
        )
        self.db.commit()

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

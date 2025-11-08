# backend/app/services/auth/invite_service.py
from __future__ import annotations

from datetime import datetime, UTC, timedelta
from hashlib import sha256
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.entities.registration_invite import RegistrationInvite
from app.permissions import PermissionRole

class InviteService:
    """
    Сервіс керування інвайт-лінками для реєстрації.

    Містить:
    • create_invite   – генерує та повертає raw-токен
    • peek_invite     – читає, але не позначає 'used'
    • consume_invite  – позначає 'used' (приймає або raw_token, або модель)
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_invite(
            self,
            *,
            role: PermissionRole,
            expires_at: Optional[datetime] = None,  # ← datetime, not int
            hours_valid: int = 24,  # fallback if expires_at is missing
    ) -> str:
        # If the caller didn’t pass a datetime – calculate it from hours_valid
        if expires_at is None:
            expires_at = datetime.now(UTC) + timedelta(hours=hours_valid)

        # Safety-check: must be in the future
        if expires_at <= datetime.now(UTC):
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail="expires_at must be in the future",
            )

        raw, token_hash = RegistrationInvite.make_token()
        invite = RegistrationInvite(
            token_hash=token_hash,
            role=role,
            expires_at=expires_at,
        )
        self.db.add(invite)
        await self.db.commit()
        return raw

    # ─────────────────────────────────────────────────────────────
    async def _get_invite(self, raw_token: str) -> Optional[RegistrationInvite]:
        token_hash = sha256(raw_token.encode()).hexdigest()
        return await self.db.scalar(
            select(RegistrationInvite)
            .where(RegistrationInvite.token_hash == token_hash)
            .with_for_update()
        )

    async def peek_invite(self, raw_token: str) -> RegistrationInvite:
        """
        Перевіряє валідність токена, НЕ змінює invite.

        Використовуй у GET-роуті, щоб фронт міг дізнатися роль.
        """
        invite = await self._get_invite(raw_token)
        if (
            not invite
            or invite.is_used
            or invite.expires_at < datetime.now(UTC)
        ):
            raise HTTPException(status.HTTP_410_GONE, detail="Невалідна чи протермінована ссилка")
        return invite

    async def consume_invite(
        self,
        invite_or_token: RegistrationInvite | str,
    ) -> RegistrationInvite:
        """
        Позначає інвайт використаним.

        • Якщо переданий raw_token — дістає модель і маркує.
        • Якщо передана модель — маркує напряму.
        """
        if isinstance(invite_or_token, str):
            invite = await self.peek_invite(invite_or_token)  # повторна перевірка
        else:
            invite = invite_or_token

        # Маркуємо використаним
        invite.is_used = True
        await self.db.commit()
        return invite

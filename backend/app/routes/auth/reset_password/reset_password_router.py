from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.schemas.auth import ResetPasswordRequest, ResetPasswordConfirm
from backend.app.utils.decorators import handle_route_exceptions
from backend.app.services.auth import ResetPasswordService
from backend.app.utils.middlewares import rate_limit
from backend.db.session import get_async_db

router = APIRouter(tags=["Reset Password"])


@router.post("/request", status_code=status.HTTP_202_ACCEPTED)
@rate_limit("2/minute")
@handle_route_exceptions()
async def request_reset(
    data: ResetPasswordRequest,
    db: AsyncSession = Depends(get_async_db)
):
    service = ResetPasswordService(db)
    await service.request_reset(data.email)
    return {"detail": "If that email exists, a reset link has been sent."}


@router.post("/confirm", status_code=status.HTTP_200_OK)
@handle_route_exceptions()
async def reset_password(
    data: ResetPasswordConfirm,
    db: AsyncSession = Depends(get_async_db)
):
    service = ResetPasswordService(db)
    success = await service.reset_password(data.token, data.new_password)

    if not success:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid or expired token")

    return {"detail": "Password successfully updated."}

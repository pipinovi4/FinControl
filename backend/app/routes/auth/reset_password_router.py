from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.schemas.auth import ResetPasswordRequest, ResetPasswordConfirm
from backend.app.utils.decorators import handle_route_exceptions
from backend.app.services.auth import ResetPasswordService
from backend.db.session import get_db

reset_password_router = APIRouter(tags=["Reset Password"])


@reset_password_router.post(
    "/reset-password-request",
    status_code=status.HTTP_200_OK,
    summary="Send password reset link to user's email",
)
@handle_route_exceptions
def request_reset(
    data: ResetPasswordRequest,
    db: Session = Depends(get_db),
):
    email = data.email
    if not email:
        raise HTTPException(status_code=404, detail="User with this email does not exist")

    ResetPasswordService(db).request_reset(email)
    return {"msg": "A reset link has been sent to the specified email."}


@reset_password_router.post(
    "/resend-reset-link",
    status_code=status.HTTP_200_OK,
    summary="Resend password reset link to user's email",
)
@handle_route_exceptions
def resend_reset_link(
    data: ResetPasswordRequest,
    db: Session = Depends(get_db),
):
    email = data.email
    if not email:
        raise HTTPException(status_code=404, detail="User with this email does not exist")

    ResetPasswordService(db).request_reset(email)
    return {"msg": "A new reset link has been resent to the specified email."}


@reset_password_router.post(
    "/reset-password",
    status_code=status.HTTP_200_OK,
    summary="Reset password using provided token and new password",
)
@handle_route_exceptions
def reset_password(
    data: ResetPasswordConfirm,
    db: Session = Depends(get_db),
):
    if not data.token:
        raise HTTPException(status_code=404, detail="User with this token does not exist")

    if not data.new_password:
        raise HTTPException(status_code=404, detail="New password cannot be empty")

    success = ResetPasswordService(db).reset_password(data.token, data.new_password)
    if not success:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    return {"msg": "Password updated successfully"}

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.schemas.auth import ResetPasswordRequest, ResetPasswordConfirm
from backend.app.utils.decorators import handle_route_exceptions
from backend.app.services.auth import ResetPasswordService
from backend.db.session import get_db

reset_password_router = APIRouter(tags=["Reset Password"])


@reset_password_router.post("/request", status_code=status.HTTP_202_ACCEPTED)
@handle_route_exceptions()
def request_reset(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    ResetPasswordService(db).request_reset(data.email)
    return {"detail": "If that email exists, a reset link has been sent."}

@reset_password_router.post("/confirm", status_code=status.HTTP_200_OK)
@handle_route_exceptions()
def reset_password(data: ResetPasswordConfirm, db: Session = Depends(get_db)):
    if not ResetPasswordService(db).reset_password(data.token, data.new_password):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid or expired token")
    return {"detail": "Password successfully updated."}

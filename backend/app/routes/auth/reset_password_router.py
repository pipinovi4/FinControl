from fastapi import APIRouter, Depends, HTTPException, status, Body
from pydantic import BaseModel
from pydantic import EmailStr
from sqlalchemy.orm import Session

from backend.app.utils.decorators import handle_route_exceptions
from backend.app.services.auth import ResetPasswordService
from backend.db.session import get_db

reset_password_router = APIRouter(tags=["Reset Password"])


# TODO move ResetPasswordRequest/ResetPasswordConfirm to schemas domain
class ResetPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordConfirm(BaseModel):
    token: str
    new_password: str

@reset_password_router.post("/reset-password-request")
@handle_route_exceptions
def request_reset(
    data: ResetPasswordRequest,
    db: Session = Depends(get_db),
):
    email = data.email
    if not email:
        raise HTTPException(status_code=404, detail="User with this email does not exist")

    reset_password_cls = ResetPasswordService(db)

    reset_password_cls.request_reset(email)

    return {"msg": "A reset link has been sent on specified email."}

@reset_password_router.post(f"/reset-password")
@handle_route_exceptions
def reset_password(data: ResetPasswordConfirm, db: Session = Depends(get_db)):
    token = data.token
    if not token:
        raise HTTPException(status_code=404, detail="User with this token does not exist")

    new_password = data.new_password
    if not new_password:
        raise HTTPException(status_code=404, detail="New password cannot be empty")

    reset_password_cls = ResetPasswordService(db)
    success = reset_password_cls.reset_password(data.token, data.new_password)
    if not success:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    return {"msg": "Password updated successfully"}

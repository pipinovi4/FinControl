from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from uuid import uuid4
from backend.db.session import get_db  # функція, яка дає db: Session
from backend.app.models.entities.user import User  # твоя User модель

router = APIRouter(prefix="/users", tags=["Users"])


# Pydantic схема
class UserCreate(BaseModel):
    email: EmailStr
    telegram_id: str
    telegram_username: str
    role: str
    is_active: bool


@router.post("/", summary="Create user")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Перевірка чи вже існує користувач з такою email
    existing = db.query(User).filter_by(email=user.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )

    # Створення об'єкта User
    new_user = User(
        id=uuid4(),  # Якщо не autogen
        telegram_id=user.telegram_id,
        telegram_username=user.telegram_username,
        role=user.role,
        is_active=user.is_active
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "msg": "User created!",
        "user": {
            "id": new_user.id,
            "telegram_id": new_user.telegram_id,
            "telegram_username": new_user.telegram_username,
            "role": new_user.role,
            "is_active": new_user.is_active
        }
    }

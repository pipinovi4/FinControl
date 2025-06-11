# backend/app/routes/users.py
from fastapi import APIRouter
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/users", tags=["Users"])

# Тестова схема для створення юзера
class UserCreate(BaseModel):
    email: EmailStr
    telegram_id: str
    telegram_username: str
    role: str
    is_active: bool

@router.post("/", summary="Create user (demo route)")
async def create_user(user: UserCreate):
    # Тут замість БД — просто вивід у консоль для тесту
    print("New user data:", user)
    return {"msg": "User created!", "user": user}

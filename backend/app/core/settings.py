# backend/app/core/settings.py

from pydantic import BaseSettings

class Settings(BaseSettings):
    # JWT
    JWT_SECRET: str
    JWT_ALGO: str = "HS256"
    ACCESS_EXPIRE_MINUTES: int = 30
    REFRESH_EXPIRE_DAYS: int = 30

    # DB
    DATABASE_URL: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
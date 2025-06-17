from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import computed_field
from dotenv import load_dotenv

# підвантажуємо .env поряд із коренем проєкту
ENV_PATH = Path(__file__).resolve().parent.parent.parent.parent / ".env"
load_dotenv(ENV_PATH, override=True)


class Settings(BaseSettings):
    # --- DB ---
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    # --- JWT ---
    JWT_SECRET: str
    JWT_ALGO: str
    ACCESS_EXPIRE_MINUTES: int
    REFRESH_EXPIRE_DAYS: int

    # --- computed ---
    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    class Config:
        env_file = ".env"          # fallback, якщо load_dotenv не спрацює
        extra = "ignore"           # про всяк випадок


settings = Settings()

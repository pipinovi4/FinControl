from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from typing import AsyncGenerator

from backend.app.config import SQLALCHEMY_DATABASE_URI
from backend.app.core.settings import settings

# ─────────────────────────────────────────────────────────────
# ASYNC SQLAlchemy setup
# ─────────────────────────────────────────────────────────────

# Create the async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,  # Set to False in production
    future=True
)

# Async sessionmaker
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

# Base class for all ORM models
Base = declarative_base()

# FastAPI dependency for providing async DB session
async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Yield an async SQLAlchemy session for use with FastAPI dependencies.
    Closes session automatically after use.
    """
    async with AsyncSessionLocal() as session:
        yield session

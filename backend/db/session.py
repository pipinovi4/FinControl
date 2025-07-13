from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from typing import AsyncGenerator
from backend.app.config import SQLALCHEMY_DATABASE_URI

# Create async SQLAlchemy engine
engine = create_async_engine(SQLALCHEMY_DATABASE_URI, echo=True)

# Create async sessionmaker
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

# Declarative base for models
Base = declarative_base()

# Async dependency for FastAPI
async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

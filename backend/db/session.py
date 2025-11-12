from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from typing import AsyncGenerator
from app.config import (
    SQLALCHEMY_DATABASE_URI,
    SQLALCHEMY_POOL_PRE_PING,
    SQLALCHEMY_POOL_SIZE,
    SQLALCHEMY_MAX_OVERFLOW,
    SQLALCHEMY_POOL_TIMEOUT,
)

# 🔧 Створюємо async SQLAlchemy engine з pool параметрами
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URI,
    echo=True,
    pool_pre_ping=(SQLALCHEMY_POOL_PRE_PING.lower() == "true"),
    pool_size=SQLALCHEMY_POOL_SIZE,
    max_overflow=SQLALCHEMY_MAX_OVERFLOW,
    pool_timeout=SQLALCHEMY_POOL_TIMEOUT,
)

# 🧠 Create async sessionmaker
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

# 📦 Declarative base for models
Base = declarative_base()

# 📡 Async dependency for FastAPI
async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

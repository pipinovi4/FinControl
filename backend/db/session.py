from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from typing import AsyncGenerator
from app.config import (
    SQLALCHEMY_DATABASE_URI,
    SQLALCHEMY_POOL_PRE_PING,
    SQLALCHEMY_POOL_RECYCLE,
    SQLALCHEMY_POOL_SIZE,
    SQLALCHEMY_MAX_OVERFLOW,
    SQLALCHEMY_POOL_TIMEOUT,
)

# 🔧 Create async SQLAlchemy engine with pool settings
engine = create_async_engine(
    f"{SQLALCHEMY_DATABASE_URI}?pool_pre_ping=true&pool_recycle={SQLALCHEMY_POOL_RECYCLE}",
    echo=True,
    pool_size=SQLALCHEMY_POOL_SIZE,
    max_overflow=SQLALCHEMY_MAX_OVERFLOW,
    pool_timeout=SQLALCHEMY_POOL_TIMEOUT,
    pool_pre_ping=True,
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

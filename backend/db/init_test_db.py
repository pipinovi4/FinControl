from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import Base
from app.core.settings import settings

DB_URL = settings.DB_URL

engine_test = create_async_engine(DB_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(bind=engine_test, expire_on_commit=False)

async def init_test_db():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

async def override_test_db():
    async with AsyncSessionLocal() as session:
        yield session

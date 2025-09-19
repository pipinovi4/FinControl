import pytest
from httpx import AsyncClient
from httpx import ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import AsyncGenerator

from backend.main import application
from backend.db.session import get_async_db
from backend.db.init_test_db import override_test_db


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="session")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    application.dependency_overrides[get_async_db] = override_test_db

    transport = ASGITransport(app=application)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="function")
async def test_db_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in override_test_db():
        try:
            yield session
        finally:
            await session.close()
        break

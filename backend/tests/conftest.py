import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from backend.main import application  # FastAPI instance
from backend.db.session import get_db
from backend.db.init_test_db import override_test_db  # твоя тестова БД (див нижче)

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture(scope="session")
async def async_client() -> AsyncClient:
    application.dependency_overrides[get_db] = override_test_db
    async with AsyncClient(app=application, base_url="http://test") as client:
        yield client

@pytest.fixture(scope="function")
async def test_db_session() -> AsyncSession:
    async for session in override_test_db():
        yield session

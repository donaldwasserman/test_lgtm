import os
import tempfile

_TMP_DIR = tempfile.mkdtemp(prefix="geoevents-tests-")
os.environ["DATABASE_URL"] = f"sqlite+aiosqlite:///{_TMP_DIR}/test.db"
os.environ["SECRET_KEY"] = "test-secret-key"
os.environ["DEBUG"] = "false"

import pytest
from httpx import ASGITransport, AsyncClient

from app.db import base
from app.db.session import AsyncSessionLocal, engine, get_db
from app.main import app


async def override_get_db():
    async with AsyncSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
async def reset_db():
    async with engine.begin() as conn:
        await conn.run_sync(base.Base.metadata.drop_all)
        await conn.run_sync(base.Base.metadata.create_all)
    yield
    await engine.dispose()


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


@pytest.fixture
def user_payload():
    return {
        "email": "alice@example.com",
        "username": "alice",
        "password": "secret123",
        "full_name": "Alice Example",
    }


@pytest.fixture
async def register_and_login(client):
    async def _register_and_login(payload):
        register = await client.post("/api/auth/register", json=payload)
        assert register.status_code == 200, register.text
        login = await client.post(
            "/api/auth/login",
            data={"username": payload["username"], "password": payload["password"]},
        )
        assert login.status_code == 200, login.text
        return login.json()["access_token"]

    return _register_and_login
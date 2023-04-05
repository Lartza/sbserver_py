import asyncio
from os import environ
from typing import AsyncIterator
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
import pytest
from httpx import AsyncClient

from ..main import app, get_db
from .. import models

env = environ.get('APPLICATION_ENV')

if env == 'test':
    async_engine = create_async_engine(
        "sqlite+aiosqlite:///./test.db", connect_args={"check_same_thread": False}
    )
    TestingSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=async_engine)

    async def init():
        async with async_engine.begin() as conn:
            await conn.run_sync(models.Base.metadata.drop_all)
            await conn.run_sync(models.Base.metadata.create_all)

    asyncio.run(init())
else:
    raise Exception('Not a test environment, protecting database')


async def override_get_db() -> AsyncIterator[AsyncSession]:
    async with TestingSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def anyio_backend():
    return 'asyncio'


@pytest.mark.anyio
async def test_read_vipusers():
    async with async_engine.begin() as conn:
        stmt = insert(models.Vipusers).values(userID='test')
        await conn.execute(stmt)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get('/vipusers')
    assert response.status_code == 200
    assert response.json() == {'items': [{'userID': 'test'}], 'page': 1, 'pages': 1, 'size': 50, 'total': 1}

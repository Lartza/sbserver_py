from os import environ
import pytest
from httpx import AsyncClient

from ..main import app, engine, database
from .. import tables

env = environ.get('APPLICATION_ENV')

if env == 'test':
    tables.metadata.drop_all(engine)
    tables.metadata.create_all(engine)
else:
    raise Exception('Not a test environment, protecting database')


@pytest.fixture
def anyio_backend():
    return 'asyncio'


@pytest.mark.anyio
async def test_read_vipusers():
    query = tables.vipusers.insert().values(userID='test')
    await database.execute(query)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get('/vipusers')
    assert response.status_code == 200
    assert response.json() == {'items': [{'userID': 'test'}], 'total': 1, 'page': 1, 'size': 50}

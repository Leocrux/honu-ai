import pytest_asyncio
from beanie import init_beanie
from httpx import AsyncClient
from mongomock_motor import AsyncMongoMockClient

from app.api import router as ServiceProviderRouter
from app.main import app
from app.models import ServiceProviderModel
from tests.datafile import testdata


@pytest_asyncio.fixture
async def test_app():
    app.include_router(
        ServiceProviderRouter, tags=["ServiceProvider"], prefix="/service_provider"
    )
    mongoclient = AsyncMongoMockClient()
    await init_beanie(
        document_models=[ServiceProviderModel],
        database=mongoclient.get_database(name="honu-ai-db"),
    )
    collection = mongoclient["honu-ai-db"]["service_provider_collection"]

    for data in testdata:
        result = await collection.insert_one(data)
        assert result.inserted_id
    ac = AsyncClient(app=app, base_url="http://localhost:8080", follow_redirects=True)
    yield ac

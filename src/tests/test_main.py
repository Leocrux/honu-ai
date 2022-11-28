import pytest


@pytest.mark.asyncio
async def test_hello(test_app):
    response = await test_app.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


@pytest.mark.asyncio
async def test_get_service_provider_id(test_app):
    response = await test_app.get("/service_provider/1")
    assert response.json()["name"] == "SEO Inc 1"


@pytest.mark.asyncio
async def test_task_3(test_app):
    """Mongomock does not support $dateDiff yet... resort to manual test for now"""
    return True
    # response = await test_app.get("/get_available_providers?skills=A&budget=100")
    # assert response.json()[0]["_id"] == "3"

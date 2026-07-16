import pytest
from httpx import AsyncClient, ASGITransport
from backend.app.main import app


@pytest.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_health_endpoint(async_client):
    response = await async_client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "version" in data
    assert "environment" in data


@pytest.mark.asyncio
async def test_chat_endpoint_no_pipeline(async_client):
    response = await async_client.post(
        "/api/v1/chat",
        json={"message": "Hello", "session_id": None},
    )
    assert response.status_code in (200, 503)


@pytest.mark.asyncio
async def test_chat_endpoint_empty_message(async_client):
    response = await async_client.post(
        "/api/v1/chat",
        json={"message": "", "session_id": None},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_appointment_endpoint_validation(async_client):
    response = await async_client.post(
        "/api/v1/appointments",
        json={
            "patient_name": "",
            "contact_number": "",
            "preferred_date": "2020-01-01",
            "preferred_time": "invalid",
            "requested_service": "",
            "reason": "",
        },
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_docs_available(async_client):
    response = await async_client.get("/docs")
    assert response.status_code in (200, 307)


@pytest.mark.asyncio
async def test_openapi_json(async_client):
    response = await async_client.get("/openapi.json")
    assert response.status_code == 200

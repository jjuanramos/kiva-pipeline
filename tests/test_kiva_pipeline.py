import pytest
from httpx import AsyncClient

from kiva_pipeline.app import app


client = AsyncClient(app=app, base_url="http://127.0.0.1:8000")


@pytest.mark.asyncio
async def test_root():
    response = await client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello world!"
    }


@pytest.mark.asyncio
async def test_get_kiva_item_empty():
    response = await client.get("/get_kiva_item/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "You need to provide an id such as /get_kiva_item/50000"
    }


@pytest.mark.asyncio
async def test_get_kiva_item_response_given_str_returns_error():
    response = await client.get("/get_kiva_item/'s'")

    assert response.status_code == 422
    assert "detail" in response.json()
    assert response.json()\
        .get('detail')[0].get("msg") == "value is not a valid integer"


@pytest.mark.asyncio
async def test_get_kiva_item_response_given_int():
    response = await client.get("http://127.0.0.1:8000/get_kiva_item/50000")

    assert response.status_code == 200
    assert type(response.json()) == dict
    assert "detail" not in response.json()
    assert "data" in response.json()


@pytest.mark.asyncio
async def test_get_kiva_batch_response_given_str():
    response = await client.get("http://127.0.0.1:8000/get_kiva_batch/'s'")

    assert response.status_code == 422
    assert type(response.json()) == dict
    assert "detail" in response.json()
    assert response.json()\
        .get('detail')[0].get("msg") == "value is not a valid integer"


@pytest.mark.asyncio
async def test_get_kiva_batch_response_given_int():
    response = await client.get("http://127.0.0.1:8000/get_kiva_batch/5")

    assert response.status_code == 200
    assert type(response.json()) == dict
    assert "detail" not in response.json()
    assert "data" in response.json()
    assert len(
        response.json()
        .get("data")
        .get("lend")
        .get("loans")
        .get("values")
    ) == 5


@pytest.mark.asyncio
async def test_get_kiva_batch_response_given_empty():
    response = await client.get("http://127.0.0.1:8000/get_kiva_batch")

    assert response.status_code == 200
    assert type(response.json()) == dict
    assert "message" in response.json()


@pytest.mark.asyncio
async def test_get_kiva_batch_response_given_int_greater_than_twenty():
    response = await client.get("http://127.0.0.1:8000/get_kiva_batch/30")

    assert response.status_code == 200
    assert type(response.json()) == dict
    assert "detail" not in response.json()
    assert "data" in response.json()
    assert len(
        response.json()
        .get("data")
        .get("lend")
        .get("loans")
        .get("values")
        ) == 20

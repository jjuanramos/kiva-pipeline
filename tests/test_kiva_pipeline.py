import requests


def test_basic_response():
    response = requests.get("http://127.0.0.1:8000/")

    assert response.status_code == 200


def test_get_kiva_item_empty():
    response = requests.get("http://127.0.0.1:8000/get_kiva_item/")

    assert type(response.json()) == dict
    assert "message" in response.json()


def test_get_kiva_item_response_given_str():
    response = requests.get("http://127.0.0.1:8000/get_kiva_item/'s'")

    assert type(response.json()) == dict
    assert "detail" in response.json()
    assert response.json()\
        .get('detail')[0].get("msg") == "value is not a valid integer"


def test_get_kiva_item_response_given_int():
    response = requests.get("http://127.0.0.1:8000/get_kiva_item/50000")

    assert type(response.json()) == dict
    assert "detail" not in response.json()
    assert "data" in response.json()


def test_get_kiva_batch_response_given_str():
    response = requests.get("http://127.0.0.1:8000/get_kiva_batch/'s'")

    assert type(response.json()) == dict
    assert "detail" in response.json()
    assert response.json()\
        .get('detail')[0].get("msg") == "value is not a valid integer"


def test_get_kiva_batch_response_given_int():
    response = requests.get("http://127.0.0.1:8000/get_kiva_batch/5")

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


def test_get_kiva_batch_response_given_empty():
    response = requests.get("http://127.0.0.1:8000/get_kiva_batch")

    assert type(response.json()) == dict
    assert "message" in response.json()


def test_get_kiva_batch_response_given_int_greater_than_twenty():
    response = requests.get("http://127.0.0.1:8000/get_kiva_batch/30")

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

import pytest
from api.courier_client import CourierClient
from api.order_client import OrderClient
from helpers.data_generator import generate_courier_data, generate_order_data
from data.config import BASE_URL


@pytest.fixture(scope="function")
def courier():
    client = CourierClient(BASE_URL)
    courier_data = generate_courier_data()

    create_resp = client.create_courier(
        courier_data["login"], courier_data["password"], courier_data["firstName"]
    )
    assert create_resp.status_code == 201

    login_resp = client.login_courier(courier_data["login"], courier_data["password"])
    assert login_resp.status_code == 200
    courier_id = login_resp.json()["id"]

    courier_data["id"] = courier_id
    yield courier_data

    client.delete_courier(courier_id)


@pytest.fixture(scope="function")
def order_client():
    return OrderClient(BASE_URL)


@pytest.fixture(scope="function")
def order_id(order_client):
    payload = generate_order_data()
    resp = order_client.create_order(payload)
    assert resp.status_code == 201
    track = resp.json()["track"]
    get_resp = order_client.get_order_by_track(track)
    assert get_resp.status_code == 200
    return get_resp.json()["order"]["id"]

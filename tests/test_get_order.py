import pytest
import allure
from api.order_client import OrderClient
from helpers.data_generator import generate_order_data
from data.config import BaseUrl, ErrorOrder


@allure.feature("get order")
class TestGetOrder:
    @allure.story("get orders")
    @allure.title("Получения списка всех заказаов")
    def test_get_orders(self):
        client = OrderClient(BaseUrl.BASE_URL)
        response = client.get_orders()
        assert response.status_code == 200
        response_json = response.json()
        assert "orders" in response_json
        assert isinstance(response_json["orders"], list)

    @allure.title("Успешное получения заказа по номеру (track)")
    def test_get_order_by_track_success(self):
        client = OrderClient(BaseUrl.BASE_URL)
        payload = generate_order_data()
        track = client.create_order(payload).json()["track"]

        response = client.get_order_by_track(track)

        assert response.status_code == 200
        order = response.json()["order"]
        assert order["track"] == track
        assert "id" in order
        assert "firstName" in order

    @allure.title("Ошибка: запрос без номера заказа (track)")
    def test_get_order_without_track(self):
        client = OrderClient(BaseUrl.BASE_URL)
        response = client._send_request("GET", BaseUrl.ORDER_TRACK)

        assert response.status_code == 400
        assert ErrorOrder.MISSING_COURIER_OR_ORDER_ID in response.json()["message"]

    @allure.title("Ошибка: запрос с несущесвующим номером заказа")
    def test_get_order_with_invalid_track(self):
        client = OrderClient(BaseUrl.BASE_URL)
        response = client.get_order_by_track(999999999)

        assert response.status_code == 404
        assert ErrorOrder.NOT_FOUND_ORDER in response.json()["message"]

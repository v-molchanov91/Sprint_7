import pytest
import allure
from api.order_client import OrderClient
from api.courier_client import CourierClient
from helpers.data_generator import generate_courier_data, generate_order_data
from data.config import BaseUrl, ErrorOrder


@allure.feature("Order API")
@allure.story("Принятие заказа (Назначение курьера)")
class TestAcceptOrder:

    @allure.title("Успешное принятие заказа возвращает {{ok: true}}")
    def test_accept_order_success(self, courier, order_id):
        client = OrderClient(BaseUrl.BASE_URL)
        response = client.accept_order(order_id, courier["id"])

        assert response.status_code == 200
        assert response.json() == {"ok": True}

    @allure.title("Ошибка: не передан id курьера")
    def test_accept_order_without_courier_id_fails(self, order_id):
        client = OrderClient(BaseUrl.BASE_URL)
        response = client._send_request(
            "PUT", f"{BaseUrl.ACCEPT_ORDER}/{order_id}", params={}
        )

        assert response.status_code == 400
        assert ErrorOrder.MISSING_COURIER_OR_ORDER_ID in response.json()["message"]

    @allure.title("Ошибка: передан несуществующий id курьера")
    def test_accept_order_with_invalid_courier_id_fails(self, order_id):
        client = OrderClient(BaseUrl.BASE_URL)
        invalid_courier_id = 999999999
        response = client.accept_order(order_id, invalid_courier_id)

        assert response.status_code == 404
        assert ErrorOrder.COURIER_NOT_FOUND in response.json()["message"]

    @allure.title("Ошибка: не передан id заказа")
    def test_accept_order_without_order_id_fails(self):
        client = OrderClient(BaseUrl.BASE_URL)

        response = client._send_request(
            "PUT", BaseUrl.ACCEPT_ORDER, params={"courierId": 123}
        )

        assert response.status_code == 404

    @allure.title("Ошибка: неверный id заказа")
    def test_accept_order_with_invalid_order_id_fails(self, courier):
        client = OrderClient(BaseUrl.BASE_URL)
        invalid_order_id = 999999999
        response = client.accept_order(invalid_order_id, courier["id"])

        assert response.status_code == 404
        assert ErrorOrder.ORDER_NOT_FOUND in response.json()["message"]

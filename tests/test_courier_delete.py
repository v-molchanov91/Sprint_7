import pytest
import allure
from api.courier_client import CourierClient
from data.config import BASE_URL, ErrorCourier, COURIER
from helpers.data_generator import generate_courier_data


@allure.feature("API Courier")
@allure.story("Удаление курьера")
class TestDeleteCourier:
    @allure.title("Успешное удаление курьера")
    def test_delete_courier_success(self, courier):
        client = CourierClient(BASE_URL)
        response = client.delete_courier(courier["id"])

        assert response.status_code == 200
        assert response.json() == {"ok": True}

    @allure.title("Ошибка при удалении без id")
    def test_delete_courier_without_id(self):
        client = CourierClient(BASE_URL)
        response = client._send_request("DELETE", COURIER)

        assert response.status_code == 404
        assert response.json()["message"] == ErrorCourier.NOT_FOUND

    @allure.title("Ошибка при удалении с некорректным id")
    def test_delete_courier_with_wrong_id(self):
        client = CourierClient(BASE_URL)
        no_exist_id = 999999999
        response = client.delete_courier(no_exist_id)

        assert response.status_code == 404
        assert response.json()["message"] == ErrorCourier.NON_EXISTENT_ID

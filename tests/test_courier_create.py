import pytest
import allure
from api.courier_client import CourierClient
from helpers.data_generator import generate_courier_data
from data.config import BaseUrl, ErrorCourier


@allure.feature("API Courier")
@allure.story("Создание курьера")
class TestCourier:

    def _cleanup_courier(self, login, password):
        client = CourierClient(BaseUrl.BASE_URL)
        try:
            login_resp = client.login_courier(login, password)
            if login_resp.status_code == 200:
                courier_id = login_resp.json()["id"]
                client.delete_courier(courier_id)
        except:
            pass

    @allure.title("Курьера можно создать: возвращает 201 и {{ok: true}}")
    def test_create_courier_success(self):
        client = CourierClient(BaseUrl.BASE_URL)
        data = generate_courier_data()
        courier_id = None
        try:
            response = client.create_courier(
                data["login"], data["password"], data["firstName"]
            )

            assert response.status_code == 201
            assert response.json() == {"ok": True}

            login_resp = client.login_courier(data["login"], data["password"])
            courier_id = login_resp.json()["id"]
        finally:
            if courier_id:
                client.delete_courier(courier_id)

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_duplicate_courier(self):
        client = CourierClient(BaseUrl.BASE_URL)
        data = generate_courier_data()
        courier_id = None
        try:
            resp1 = client.create_courier(
                data["login"], data["password"], data["firstName"]
            )

            resp2 = client.create_courier(
                data["login"], data["password"], data["firstName"]
            )
            assert resp2.status_code == 409
            assert resp2.json()["message"] == ErrorCourier.IS_ALREADY_LOGIN
            login_resp = client.login_courier(data["login"], data["password"])
            courier_id = login_resp.json()["id"]
        finally:
            if courier_id:
                client.delete_courier(courier_id)

    @allure.title("Поля логин и пароль обязательные")
    @pytest.mark.parametrize(
        "login, password",
        [
            ("", "valid_pass"),
            ("valid_login", ""),
            ("", ""),
        ],
    )
    def test_missing_required_field_fails(self, login, password):
        client = CourierClient(BaseUrl.BASE_URL)
        response = client.create_courier(login, password, "Имя")

        assert response.status_code == 400
        assert response.json()["message"] == ErrorCourier.MISSING_LOGIN_AND_PASSWORD

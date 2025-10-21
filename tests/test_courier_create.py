import pytest
import allure
from api.courier_client import CourierClient
from helpers.data_generator import generate_courier_data
from data.config import BASE_URL, ErrorCourier


@allure.feature("API Courier")
@allure.story("Создание курьера")
class TestCourier:
    @allure.title("Курьера можно создать: возвращает 201 и {{ok: true}}")
    def test_create_courier_success(self):
        client = CourierClient(BASE_URL)
        data = generate_courier_data()

        response = client.create_courier(
            data["login"], data["password"], data["firstName"]
        )

        assert response.status_code == 201
        assert response.json() == {"ok": True}

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_duplicate_courier(self):
        client = CourierClient(BASE_URL)
        data = generate_courier_data()

        resp1 = client.create_courier(
            data["login"], data["password"], data["firstName"]
        )
        assert resp1.status_code == 201

        resp2 = client.create_courier(
            data["login"], data["password"], data["firstName"]
        )
        assert resp2.status_code == 409
        assert resp2.json()["message"] == ErrorCourier.IS_ALREADY_LOGIN

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
        client = CourierClient(BASE_URL)
        response = client.create_courier(login, password, "Имя")

        assert response.status_code == 400
        assert response.json()["message"] == ErrorCourier.MISSING_LOGIN_AND_PASSWORD

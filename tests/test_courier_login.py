import pytest
import allure
from api.courier_client import CourierClient
from data.config import BASE_URL, ErrorCourier
from helpers.data_generator import generate_courier_data


@allure.feature("API Courier")
@allure.story("Авторизация курьера")
class TestCourierLogin:
    @allure.title("Курьер может автоизироваться")
    def test_login_success(self, courier):
        client = CourierClient(BASE_URL)
        response = client.login_courier(courier["login"], courier["password"])

        assert response.status_code == 200
        assert "id" in response.json()
        assert isinstance(response.json()["id"], int)

    @allure.title("Для авторизации нужны логин и пароль")
    @pytest.mark.parametrize("missing", ["login", "password"])
    def test_login_missing_field_fails(self, missing):
        client = CourierClient(BASE_URL)
        login = "test" if missing != "login" else ""
        password = "test" if missing != "password" else ""

        response = client.login_courier(login, password)

        assert response.status_code == 400
        assert response.json()["message"] == ErrorCourier.MISSING_LOGIN_OR_PASSWORD

    @allure.title("Ошибка при неверных логине/пароле")
    def test_login_with_wrong_credentials_fails(self):
        client = CourierClient(BASE_URL)
        response = client.login_courier("nonexistent_login", "wrong_password")

        assert response.status_code == 404
        assert response.json()["message"] == ErrorCourier.IS_NO_ACCOUNT

    @allure.title("Ошибка при верном логине и неверном пароле")
    def test_login_valid_login_wrong_password_fails(self, courier):
        client = CourierClient(BASE_URL)
        response = client.login_courier(courier["login"], "wrong_password")
        assert response.status_code == 404
        assert response.json()["message"] == ErrorCourier.IS_NO_ACCOUNT

    @allure.title("Ошибка при неверном логине и верном пароле")
    def test_login_wrong_login_valid_password_fails(self, courier):
        client = CourierClient(BASE_URL)
        response = client.login_courier("wrong_login", courier["password"])
        assert response.status_code == 404
        assert response.json()["message"] == ErrorCourier.IS_NO_ACCOUNT

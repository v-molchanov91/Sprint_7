import pytest
import allure
from api.order_client import OrderClient
from helpers.data_generator import generate_order_data
from data.config import BASE_URL


@allure.feature("Order API")
@allure.story("Создание заказа")
class TestOrderCreate:
    @pytest.mark.parametrize(
        "colors",
        [["BLACK"], ["GRAY"], ["BLACK", "GRAY"], None],
        ids=["BLACK", "GRAY", "BLACK+GRAY", "None"],
    )
    @allure.title("Проверка создания заказа с разными цветами: {colors}")
    def test_create_with_various_colors(self, colors):
        client = OrderClient(BASE_URL)
        payload = generate_order_data(color=colors)

        response = client.create_order(payload)

        assert response.status_code == 201
        response_json = response.json()
        assert "track" in response_json
        assert isinstance(response_json["track"], int)
        assert response_json["track"] > 0

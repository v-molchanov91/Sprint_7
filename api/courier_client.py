from api.base_client import BaseApiClient
from data.config import BaseUrl
import requests


class CourierClient(BaseApiClient):
    def __init__(self, base_url: str):
        super().__init__(base_url)

    def create_courier(
        self, login: str, password: str, first_name: str
    ) -> requests.Response:
        payload = {"login": login, "password": password, "firstName": first_name}
        return self._send_request("POST", BaseUrl.COURIER, json=payload)

    def login_courier(self, login: str, password: str) -> requests.Response:
        payload = {"login": login, "password": password}
        return self._send_request("POST", BaseUrl.COURIER_LOGIN, json=payload)

    def delete_courier(self, courier_id: int) -> requests.Response:
        return self._send_request("DELETE", f"{BaseUrl.COURIER}/{courier_id}")

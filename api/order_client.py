from api.base_client import BaseApiClient
from data.config import ORDERS, ORDER_TRACK, ACCEPT_ORDER
import requests


class OrderClient(BaseApiClient):
    def __init__(self, base_url: str):
        super().__init__(base_url)

    def create_order(self, payload: dict) -> requests.Response:
        return self._send_request("POST", ORDERS, json=payload)

    def get_orders(self) -> requests.Response:
        return self._send_request("GET", ORDERS)

    def accept_order(self, order_id: int, courier_id: int) -> requests.Response:
        params = {"courierId": courier_id}
        return self._send_request("PUT", f"{ACCEPT_ORDER}/{order_id}", params=params)

    def get_order_by_track(self, track: int) -> requests.Response:
        return self._send_request("GET", ORDER_TRACK, params={"t": track})

import requests
from requests import Response
from data.config import *


class BaseApiClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    def _send_request(self, method: str, endpoint: str, **kwargs) -> Response:
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, **kwargs)
        return response

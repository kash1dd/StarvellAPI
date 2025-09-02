import requests
from requests import Session
import urllib3

from StarvellAPI.common.exceptions import RequestFailedError, UnauthorizedError

urllib3.disable_warnings()

class StarvellSession:
    def __init__(self, session_id: str):
        self.request = Session()

        self.request.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) Gecko/20100101 Firefox/141.0"
        }
        self.request.cookies["session"] = session_id

    def send_request(self, method: str, url: str, body: dict | None = None,
                     raise_not_200: bool = False) -> requests.Response:
        if body:
            response: requests.Response = getattr(self.request, method)(url, headers=self.request.headers, json=body,
                                                     allow_redirects=False, verify=False)
        else:
            response: requests.Response = getattr(self.request, method)(url, headers=self.request.headers,
                                                     allow_redirects=False, verify=False)

        if response.status_code == 403:
            raise UnauthorizedError(response)
        elif response.status_code not in (200, 201) and raise_not_200:
            raise RequestFailedError(response)
        return response

    def get(self, url: str, body: dict | None = None, raise_not_200: bool = True):
        return self.send_request("get", url, body, raise_not_200=raise_not_200)

    def post(self, url: str, body: dict | None = None, raise_not_200: bool = True):
        return self.send_request("post", url, body, raise_not_200=raise_not_200)
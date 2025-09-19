from StarvellAPI.errors import RequestFailedError, UnauthorizedError

from requests import Session, Response
from datetime import datetime

import requests

class StarvellSession:
    def __init__(self, session_id: str, proxy: dict[str, str] | None = None):
        """
        :param session_id: ID Сессии на Starvell
        :param proxy: Прокси с которого будут осуществляться запросы (пример: {"http": "http://user:password@your_proxy_ip:port"})
        """

        self.request = Session()
        self.proxy_dict: dict[str, str] | None = proxy

        if self.proxy_dict:
            self.request.proxies = self.proxy_dict

        self.requests_count: int = 0
        self.last_429_error: int = 0

        self.request.cookies["session"] = session_id

    def send_request(self, method: str, url: str, body: dict = None,
                     raise_not_200: bool = False) -> Response:
        """
        Отправляет запрос используя сессию Starvell
        
        :param method: Метод (post/get/patch)
        :param url: Ссылка, куда отправить запрос
        :param body: JSON к запросу (Можно не указывать)
        :param raise_not_200: Возбуждать-ли исключение, если ответ не 200?
        
        :return: Response
        """

        response: Response | None = None

        for i in range(5):
            self.requests_count += 1

            if body:

                response: Response = getattr(self.request, method)(url=url, headers=self.request.headers, json=body)
            else:
                response: Response = getattr(self.request, method)(url=url, headers=self.request.headers)

            if response.status_code in (200, 201):
                break
            elif response.status_code not in (200, 201) and not raise_not_200:
                break
            elif response.status_code == 403:
                raise UnauthorizedError(response)
            elif response.status_code == 429:
                self.last_429_error = datetime.now().timestamp()
                continue

        if raise_not_200 and response.status_code not in (200, 201):
            raise RequestFailedError(response)

        return response

    def get(self, url: str, body: dict = None, raise_not_200: bool = True) -> requests.Response:
        """
        Отправляет GET запрос к Starvell

        :param url: Ссылка, куда отправить запрос
        :param body: JSON к запросу (Можно не указывать)
        :param raise_not_200: Возбуждать-ли исключение, если ответ не 200?

        :return: Response
        """

        return self.send_request("get", url, body, raise_not_200=raise_not_200)

    def post(self, url: str, body: dict = None, raise_not_200: bool = True):
        """
        Отправляет POST запрос к Starvell

        :param url: Ссылка, куда отправить запрос
        :param body: JSON к запросу (Можно не указывать)
        :param raise_not_200: Возбуждать-ли исключение, если ответ не 200?

        :return: Response
        """

        return self.send_request("post", url, body, raise_not_200=raise_not_200)

    def patch(self, url: str, body: dict = None, raise_not_200: bool = True):
        """
        Отправляет PATCH запрос к Starvell

        :param url: Ссылка, куда отправить запрос
        :param body: JSON к запросу (Можно не указывать)
        :param raise_not_200: Возбуждать-ли исключение, если ответ не 200?

        :return: Response
        """

        return self.send_request("patch", url, body, raise_not_200=raise_not_200)
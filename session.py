from .common.exceptions import RequestFailedError, UnauthorizedError

from requests import Session

import requests

class StarvellSession:
    def __init__(self, session_id: str):
        self.request = Session()


        self.request.cookies["session"] = session_id

    def send_request(self, method: str, url: str, body: dict = None,
                     raise_not_200: bool = False) -> requests.Response:
        """
        Отправляет запрос используя сессию Starvell
        
        :param method: Метод
        :param url: Ссылка, куда отправить запрос
        :param body: JSON к запросу (Можно не указывать)
        :param raise_not_200: Возбуждать-ли исключение, если ответ не 200?
        
        :return: Response
        """
        
        if body:
            resp: requests.Response = getattr(self.request, method)(url, headers=self.request.headers, json=body,
                                                     allow_redirects=False)
        else:
            resp = getattr(self.request, method)(url, headers=self.request.headers,
                                                     allow_redirects=False)

        if resp.status_code == 403:
            raise UnauthorizedError(resp)
        elif resp.status_code not in (200, 201) and raise_not_200:
            raise RequestFailedError(resp)
        return resp

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
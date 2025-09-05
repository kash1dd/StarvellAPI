import requests
from requests import Session

from StarvellAPI.common.exceptions import RequestFailedError, UnauthorizedError

class StarvellSession:
    def __init__(self, session_id: str):
        self.request = Session()


        self.request.cookies["session"] = session_id

    def send_request(self, method: str, url: str, body: dict | None = None,
                     raise_not_200: bool = False) -> requests.Response:
        """
        Отправляет запрос используя сессию Starvell
        
        :param method: Метод
        :param url: Ссылка, куда отправить запрос
        :param body: JSON к запросу (Можно не указывать)
        :param raise_not_200: Возбуждать-ли исключение, если ответ не 200?
        
        :return: requests.Response
        """
        
        if body:
            response: requests.Response = getattr(self.request, method)(url, headers=self.request.headers, json=body,
                                                     allow_redirects=False)
        else:
            response: requests.Response = getattr(self.request, method)(url, headers=self.request.headers,
                                                     allow_redirects=False)

        if response.status_code == 403:
            raise UnauthorizedError(response)
        elif response.status_code not in (200, 201) and raise_not_200:
            raise RequestFailedError(response)
        return response

    def get(self, url: str, body: dict | None = None, raise_not_200: bool = True) -> requests.Response:
        """
        Отправляет GET запрос к Starvell
        
        :param url: Ссылка, куда отправить запрос
        :param body: JSON к запросу (Можно не указывать)
        :param raise_not_200: Возбуждать-ли исключение, если ответ не 200?
        
        :return: requests.Response
        """
        
        return self.send_request("get", url, body, raise_not_200=raise_not_200)

    def post(self, url: str, body: dict | None = None, raise_not_200: bool = True):
        """
        Отправляет POST запрос к Starvell
        
        :param url: Ссылка, куда отправить запрос
        :param body: JSON к запросу (Можно не указывать)
        :param raise_not_200: Возбуждать-ли исключение, если ответ не 200?
        
        :return: requests.Response
        """
        
        return self.send_request("post", url, body, raise_not_200=raise_not_200)
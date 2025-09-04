import requests

class RequestFailedError(Exception):
    """
    Исключение, которое возбуждается, если статус код ответа != 200.
    """

    def __init__(self, response: requests.Response):
        """
        :param response: объект ответа.
        """
        self.response = response
        self.status_code = response.status_code
        self.url = response.request.url
        self.request_headers = response.request.headers
        if "cookie" in self.request_headers:
            self.request_headers["cookie"] = "HIDDEN"
        self.request_body = response.request.body
        self.log_response = False

    def short_str(self):
        return f"Ошибка запроса к {self.url}. (Статус-код: {self.status_code})"

    def __str__(self):
        msg = f"Ошибка запроса к {self.url} .\n" \
              f"Метод: {self.response.request.method} .\n" \
              f"Статус-код ответа: {self.status_code} .\n" \
              f"Заголовки запроса: {self.request_headers} .\n" \
              f"Тело запроса: {self.request_body} .\n" \
              f"Текст ответа: {self.response.text}"
        if self.log_response:
            msg += f"\n{self.response.content.decode()}"
        return msg

class UnauthorizedError(RequestFailedError):
    """
    Исключение, которое возбуждается, если не удалось найти идентифицирующий аккаунт элемент и / или произошло другое
    событие, указывающее на отсутствие авторизации.
    """

    def __init__(self, response: requests.Response):
        self.response = response
        self.session_id = self.response.cookies

    def __str__(self):
        return "Ошибка авторизации (возможно, введен неверный session_id?)."

class WithdrawError(Exception):
    """
    Возбуждается при какой-либо ошибке на вывод средств
    """

    def __init__(self, msg_from_response: str):
        self.msg = msg_from_response

    def __str__(self):
        return self.msg

class SendMessageError(Exception):
    """
    Возбуждается при какой-либо ошибке на отправку сообщения
    """

    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return self.msg

class ReadChatError(Exception):
    """
    Возбуждается при какой-либо ошибке прочтения чата
    """

    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return self.msg

class RefundError(Exception):
    """
    Возбуждается при какой-либо ошибке в возврате заказа
    """

    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return self.msg

class EditReviewError(Exception):
    """
    Возбуждается при какой-либо ошибке в редактировании ответа на отзыв
    """

    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return self.msg

class SendReviewError(Exception):
    """
    Возбуждается при какой-либо ошибке отправки ответа на отзыв
    """

    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return self.msg

class SaveLotError(Exception):
    """
    Возбуждается при какой-либо ошибке сохранения лота
    """

    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return self.msg
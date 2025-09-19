from requests import Response
from typing import Literal

class RequestFailedError(Exception):
    """
    Исключение, которое возбуждается, если статус код ответа != 200.
    """

    def __init__(self, response: Response) -> None:
        self.response = response
        self.status_code = response.status_code
        self.url = response.request.url
        self.request_headers = response.request.headers
        if "cookie" in self.request_headers:
            self.request_headers["cookie"] = "HIDDEN"
        self.request_body = response.request.body
        self.log_response: bool = False

    def short_str(self) -> str:
        return f"Ошибка запроса к {self.url}. (Статус-код: {self.status_code})"
    
    
    def __str__(self) -> str:
        msg = f"Ошибка запроса к {self.url} .\n" \
              f"Метод: {self.response.request.method} .\n" \
              f"Статус-код ответа: {self.status_code} .\n" \
              f"Заголовки запроса: {self.request_headers} .\n" \
              f"Тело запроса: {self.request_body} .\n" \
              f"Текст ответа: {self.response.text}"
        if self.log_response:
            msg += f"\n{self.response.content.decode() if self.response.content else 'HIDDEN'}"
        return msg

class UnauthorizedError(RequestFailedError):
    """
    Исключение, которое возбуждается, если не удалось найти идентифицирующий аккаунт элемент и / или произошло другое
    событие, указывающее на отсутствие авторизации.
    """

    def __init__(self, response: Response) -> None:
        self.response = response

    def __str__(self) -> str:
        return "Ошибка авторизации (возможно, введен неверный session_id?)."

class NotFoundJSONError(Exception):
    """
    Возбуждается когда JSON с основной страницы не найден.
    """

    def __str__(self) -> Literal['JSON не найден']:
        return "JSON не найден"

class HandlerError(Exception):
    """
    Возбуждается при ошибке в каком-либо хэндлере.
    """

    def __init__(self, error_msg: str) -> None:
        self.msg: str = error_msg

    def __str__(self):
        return self.msg

class StarvellAPIError(Exception):
    def __init__(self, msg_from_response: str) -> None:
        self.msg: str = msg_from_response

    def __str__(self) -> str:
        return self.msg

class WithdrawError(StarvellAPIError):
    """
    Возбуждается при какой-либо ошибке на вывод средств.
    """

class SendMessageError(StarvellAPIError):
    """
    Возбуждается при какой-либо ошибке на отправку сообщения.
    """

class ReadChatError(StarvellAPIError):
    """
    Возбуждается при какой-либо ошибке прочтения чата.
    """

class RefundError(StarvellAPIError):
    """
    Возбуждается при какой-либо ошибке в возврате заказа.
    """

class EditReviewError(StarvellAPIError):
    """
    Возбуждается при какой-либо ошибке в редактировании ответа на отзыв.
    """

class SendReviewError(StarvellAPIError):
    """
    Возбуждается при какой-либо ошибке отправки ответа на отзыв.
    """

class BlockError(StarvellAPIError):
    """
    Возбуждается при какой-либо ошибке отправки пользователя в ЧС.
    """

class UnBlockError(StarvellAPIError):
    """
    Возбуждается при какой-либо ошибке удаления пользователя из ЧС.
    """

class CreateLotError(StarvellAPIError):
    """
    Возбуждается при какой-либо ошибке создания лота.
    """

class DeleteLotError(StarvellAPIError):
    """
    Возбуждается при какой-либо ошибке удаления лота.
    """

class SaveSettingsError(StarvellAPIError):
    """
    Возбуждается при какой-либо ошибке сохранения настроек.
    """
from StarvellAPI.account import Account
from StarvellAPI.socket import Socket
from StarvellAPI.common.enums import MessageTypes, SocketTypes

from typing import Callable

class Runner:
    def __init__(self, acc: Account, always_online: bool = True):
        """
        :param acc: Экземпляр класса Account
        :param always_online: Поддерживать-ли постоянный онлайн? (True - при использовании API, аккаунт всегда будет в онлайне)
        """

        self.acc = acc
        self.socket = Socket(acc.session_id, always_online)

    def msg_handler(self, func: Callable, event_type: MessageTypes) -> None:
        """
        Добавляет хэндлер в обработчики новых сообщений вебсокета класса Socket

        :param func: Функция (хэндлер), которая будет обрабатывать ивент (Должна принимать только 1 аргумент)
        :param event_type: Тип ивента (хэндлера)

        :return: None
        """

        self.socket.msg_handlers[event_type].append(func)

    def socket_handler(self, func: Callable, handler_type: SocketTypes) -> None:
        """
        Добавляет хэндлер в хэндлеры сокета

        :param func: Функция (хэндлер), которая будет вызываться при определённом событии сокета
        :param handler_type: Тип хэндлера (На запуск/Ошибку), SocketTypes

        :return: None
        """

        self.socket.other_handlers[handler_type].append(func)
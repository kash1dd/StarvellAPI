from StarvellAPI.account import Account
from StarvellAPI.socket import Socket
from StarvellAPI.common.enums import MessageTypes

class Runner:
    def __init__(self, acc: Account, always_online: bool = True):
        """
        :param acc: Экземпляр класса Account
        :param always_online: Поддерживать-ли постоянный онлайн? (True - при использовании API, аккаунт всегда будет в онлайне)
        """

        self.acc = acc
        self.socket = Socket(acc.session_id, always_online)

    def add_handler(self, func, event_type: MessageTypes) -> None:
        """
        Добавляет хэндлер в обработчики класса Socket

        :param func: Функция (хэндлер), которая будет обрабатывать ивент (Должна принимать только 1 аргумент - NewMessageEvent)
        :param event_type: Тип ивента (хэндлера)
        """

        self.socket.handlers[event_type].append(func)
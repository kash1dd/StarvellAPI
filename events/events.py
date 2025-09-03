from StarvellAPI.account import Account
from StarvellAPI.socket import Socket

class Runner:
    def __init__(self, acc: Account, always_online: bool = True):
        """
        :param acc: Экземпляр класса Account
        :param always_online: Поддерживать-ли постоянный онлайн? (Да - при использовании API, аккаунт всегда будет в онлайне)
        """

        self.acc = acc
        self.socket = Socket(acc.session_id, always_online)

    def msg_handler(self, func) -> None:
        """
        Добавляет хэндлер в обработчики класса Socket

        :param func: Функция (хэндлер), которая будет обрабатывать ивент (Должна принимать только 1 аргумент - NewMessageEvent)
        """

        self.socket.event_handlers.append(func)
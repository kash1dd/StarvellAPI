import threading
from typing import Any, Callable

from websocket import WebSocketApp

from starvell.account import Account
from starvell.enums import MessageType, SocketTypes
from starvell.errors import HandlerError
from starvell.socket import Socket
from starvell.types import NewMessageEvent, OrderEvent, ServiceMessageEvent


class Runner:
    def __init__(self, acc: Account, always_online: bool = True):
        """
        :param acc: Экземпляр класса Account
        :param always_online: Поддерживать-ли постоянный онлайн? (True - при использовании API, аккаунт всегда будет онлайн)
        """

        self.acc: Account = acc

        self.socket: Socket = Socket(acc.session_id, always_online)
        self.socket.handlers[SocketTypes.OPEN].append(self.on_open_process)
        self.socket.handlers[SocketTypes.NEW_MESSAGE].append(
            self.on_new_message
        )

        self.handlers: dict[MessageType | SocketTypes, list] = {
            MessageType.NEW_MESSAGE: [],
            MessageType.NEW_ORDER: [],
            MessageType.CONFIRM_ORDER: [],
            MessageType.ORDER_REOPENED: [],
            MessageType.ORDER_REFUND: [],
            MessageType.NEW_REVIEW: [],
            MessageType.REVIEW_DELETED: [],
            MessageType.REVIEW_CHANGED: [],
            MessageType.REVIEW_RESPONSE_EDITED: [],
            MessageType.REVIEW_RESPONSE_CREATED: [],
            MessageType.REVIEW_RESPONSE_DELETED: [],
            MessageType.BLACKLIST_YOU_ADDED: [],
            MessageType.BLACKLIST_USER_ADDED: [],
            MessageType.BLACKLIST_YOU_REMOVED: [],
            MessageType.BLACKLIST_USER_REMOVED: [],
            SocketTypes.OPEN: [],
            SocketTypes.NEW_MESSAGE: [],
        }

        self.event_types: dict[
            MessageType,
            type[NewMessageEvent | OrderEvent | ServiceMessageEvent],
        ] = {
            MessageType.NEW_MESSAGE: NewMessageEvent,
            MessageType.NEW_ORDER: OrderEvent,
            MessageType.CONFIRM_ORDER: OrderEvent,
            MessageType.ORDER_REFUND: OrderEvent,
            MessageType.ORDER_REOPENED: OrderEvent,
            MessageType.NEW_REVIEW: OrderEvent,
            MessageType.REVIEW_DELETED: OrderEvent,
            MessageType.REVIEW_CHANGED: OrderEvent,
            MessageType.REVIEW_RESPONSE_EDITED: OrderEvent,
            MessageType.REVIEW_RESPONSE_CREATED: OrderEvent,
            MessageType.REVIEW_RESPONSE_DELETED: OrderEvent,
            MessageType.BLACKLIST_YOU_REMOVED: ServiceMessageEvent,
            MessageType.BLACKLIST_USER_REMOVED: ServiceMessageEvent,
            MessageType.BLACKLIST_YOU_ADDED: ServiceMessageEvent,
            MessageType.BLACKLIST_USER_ADDED: ServiceMessageEvent,
        }

        self.add_handler(
            SocketTypes.NEW_MESSAGE,
            handler_filter=lambda msg, *args: msg.startswith("42/chats"),
        )(self.msg_process)
        self.add_handler(
            SocketTypes.NEW_MESSAGE,
            handler_filter=lambda msg, *args: msg == "2",
        )(lambda _, ws: ws.send("3"))

    @staticmethod
    def handling(handler: list[Callable[[Any], None] | dict], *args) -> None:
        """
        Вызывает хэндлер с переданными аргументами

        :param handler: Хэндлер который будет обрабатывать
        :param args: Аргументы к этому хэндлеру

        :return: None
        """

        if handler[1] is None:
            threading.Thread(target=handler[0], args=args).start()
        else:
            if not isinstance(handler[1], (list, tuple, set)):
                if handler[1](*args, **handler[2]):
                    threading.Thread(target=handler[0], args=args).start()
            else:
                if all([h(*args, **handler[2]) for h in handler[1]]):
                    threading.Thread(target=handler[0], args=args).start()

    def add_handler(
        self,
        handler_type: MessageType | SocketTypes,
        handler_filter: list[Callable] | Callable | None = None,
        **kwargs: object,
    ) -> Callable[[Any], None]:
        """
        Добавляет хэндлер

        Примеры:

        ``@add_handler(MessageType.NEW_MESSAGE)``

        ``@add_handler(SocketTypes.NEW_MESSAGE)``

        :param handler_type: MessageType либо SocketTypes
        :param handler_filter: Функция-фильтр, указывать необязательно, в случае если эта функция вернёт False, хэндлер не сработает

        :return: Callable
        """

        def decorator(func):
            self.handlers[handler_type].append([func, handler_filter, kwargs])
            return func

        return decorator

    def msg_process(self, msg: str, _: WebSocketApp) -> None:
        """
        Вызывается при новом сообщении в веб-сокете
        в случае если это новое событие на Starvell, определяет событие
        и вызывает все привязанные к этому событию хэндлеры (функции)

        Каждый хэндлер (функция), вызывается в отдельном потоке

        :param _: WebSocketApp
        :param msg: Сообщение с веб-сокета

        :return: None
        """
        ...

    def on_open_process(self, ws: WebSocketApp) -> None:
        """
        Вызывается при открытии веб-сокета, и вызывает все привязанные к этому событию хэндлере

        Каждый хэндлер (функция), вызывается в отдельном потоке

        :param ws: WebSocketApp

        :return: None
        """

        for func in self.handlers[SocketTypes.OPEN]:
            try:
                self.handling(func, ws)
            except Exception as e:
                raise HandlerError(str(e))

    def on_new_message(self, ws: WebSocketApp, msg: str) -> None:
        """
        Вызывается при новом сообщении в веб-сокете, и вызывает все привязанные к этому событию хэндлеры (Не путать с новым сообщением на Starvell)

        Каждый хэндлер (функция), вызывается в отдельном потоке

        :param ws: WebSocketApp
        :param msg: Сообщение веб-сокета (Строка)

        :return: None
        """

        for func in self.handlers[SocketTypes.NEW_MESSAGE]:
            try:
                self.handling(func, msg, ws)
            except Exception as e:
                raise HandlerError(str(e))

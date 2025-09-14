from StarvellAPI.account import Account
from StarvellAPI.socket import Socket
from StarvellAPI.common import MessageTypes, SocketTypes, identify_ws_starvell_message, HandlerError
from StarvellAPI.types import *

from websocket import WebSocketApp
import threading
from typing import Callable

class Runner:
    def __init__(self, acc: Account, always_online: bool = True):
        """
        :param acc: Экземпляр класса Account
        :param always_online: Поддерживать-ли постоянный онлайн? (True - при использовании API, аккаунт всегда будет в онлайне)
        """

        self.acc: Account = acc

        self.socket: Socket = Socket(acc.session_id, always_online)
        self.socket.handlers[SocketTypes.OPEN].append(self.on_open_process)
        self.socket.handlers[SocketTypes.NEW_MESSAGE].append(self.on_new_message)

        self.handlers: dict = {
            MessageTypes.NEW_MESSAGE: [],
            MessageTypes.NEW_ORDER: [],
            MessageTypes.CONFIRM_ORDER: [],
            MessageTypes.ORDER_REFUND: [],
            MessageTypes.NEW_REVIEW: [],
            MessageTypes.REVIEW_DELETED: [],
            MessageTypes.REVIEW_CHANGED: [],

            SocketTypes.OPEN: [],
            SocketTypes.NEW_MESSAGE: []
        }

        self.event_types: dict = {
            MessageTypes.NEW_MESSAGE: NewMessageEvent,
            MessageTypes.NEW_ORDER: OrderEvent,
            MessageTypes.CONFIRM_ORDER: OrderEvent,
            MessageTypes.ORDER_REFUND: OrderEvent,
            MessageTypes.NEW_REVIEW: OrderEvent,
            MessageTypes.REVIEW_DELETED: OrderEvent,
            MessageTypes.REVIEW_CHANGED: OrderEvent
        }

        self.add_handler(SocketTypes.NEW_MESSAGE, handler_filter=lambda msg, *args: msg.startswith('42/chats'))(self.msg_process)
        self.add_handler(SocketTypes.NEW_MESSAGE, handler_filter=lambda msg, ws: msg == "2")(lambda _, ws: ws.send('3'))

    @staticmethod
    def handling(handler: list[Callable], *args, **kwargs) -> None:
        """
        Вызывает хэндлер с переданными аргументами

        :param handler: Хэндлер который будет обрабатывать
        :param args: Аргументы к этому хэндеру
        :param kwargs: Именованные аргументы к этому хэндлеру

        :return: None
        """

        if handler[1] is None:
            threading.Thread(target=handler[0], args=args, kwargs=kwargs).start()
        else:
            if handler[1](*args, **kwargs):
                threading.Thread(target=handler[0], args=args, kwargs=kwargs).start()

    def add_handler(
        self,
        handler_type: MessageTypes | SocketTypes,
        handler_filter: Callable | None = None,
    ):
        """
        Добавляет хэндлер

        Примеры:

        ``@add_handler(MessageTypes.NEW_MESSAGE)``

        ``@add_handler(SocketTypes.NEW_MESSAGE)``

        :param handler_type: MessageTypes либо SocketTypes
        :param handler_filter: Функция-фильтр, указывать необязательно, в случае если эта функция вернёт False, хэндлер не сработает

        :return: Callable
        """

        def decorator(func):
            self.handlers[handler_type].append([func, handler_filter])
            return func
        return decorator

    def msg_process(self, msg: str, _: WebSocketApp) -> None:
        """
        Вызывается при новом сообщении в вебсокете, и в случае если это новое событие на Starvell, определяет событие, и вызывает все привязанные к этому событию хэндлеры (функции)

        Каждый хэндлер (функция), вызывается в отдельном потоке

        :param _: WebSocketApp
        :param msg: Сообщение с вебсокета

        :return: None
        """

        try:
            dict_with_data = identify_ws_starvell_message(msg)

            if not dict_with_data:
                return

            data = self.event_types[dict_with_data['type']].model_validate(dict_with_data)

            for handler in self.handlers[dict_with_data['type']]:
                try:
                    self.handling(handler, data)
                except Exception as e:
                    print(f"Ошибка в хэндлере {handler[0].__name__}: {e}")

        except Exception as e:
            raise HandlerError(e)

    def on_open_process(self, ws: WebSocketApp) -> None:
        """
        Вызывается при открытии вебсокета, и вызывает все привязанные к этому событию хэндлере

        Каждый хэндлер (функция), вызывается в отдельном потоке

        :param ws: WebSocketApp

        :return: None
        """

        for func in self.handlers[SocketTypes.OPEN]:
            try:
                self.handling(func, ws)
            except Exception as e:
                raise HandlerError(e)

    def on_new_message(self, ws: WebSocketApp, msg: str) -> None:
        """
        Вызывается при новом сообщении в вебсокете, и вызывает все привязанные к этому событию хэндлеры (Не путать с новым сообщением на Starvell)

        Каждый хэндлер (функция), вызывается в отдельном потоке

        :param ws: WebSocketApp
        :param msg: Сообщение вебсокета (Строка)

        :return: None
        """

        for func in self.handlers[SocketTypes.NEW_MESSAGE]:
            try:
                self.handling(func, msg, ws)
            except Exception as e:
                raise HandlerError(e)
import threading
from typing import Callable

import websocket

from .enums import SocketTypes
from .errors import HandlerError


class Socket:
    def __init__(self, session_id: str, online: bool = True):
        """
        :param session_id: ID Сессии на Starvell
        :param online: Поддерживать-ли постоянный онлайн? (True - при использовании API, аккаунт всегда будет онлайн)
        """

        self.s: str = session_id
        self.online: bool = online
        self.run_socket()

        self.handlers: dict[SocketTypes, list[Callable]] = {
            SocketTypes.OPEN: [],
            SocketTypes.NEW_MESSAGE: [],
        }

    def on_message(self, ws: websocket.WebSocket, msg: str) -> None:
        """
        Вызывается при новом сообщении в веб сокете, и соответственно вызывает все привязанные хэндлеры

        :param ws: Экземпляр класса WebSocket
        :param msg: Сообщение веб сокета

        :return: None
        """

        for func in self.handlers[SocketTypes.NEW_MESSAGE]:
            try:
                func(ws, msg)
            except Exception as e:
                raise HandlerError(str(e))

    def on_open(self, ws: websocket.WebSocket) -> None:
        """
        Вызывается при открытии веб сокета, и вызывает все хэндлеры привязанные к этому событию

        Каждый хэндлер (функция), вызывается в отдельном потоке

        :param ws: Экземпляр класса WebSocket

        :return: None
        """

        ws.send("40/chats,")

        if self.online:
            ws.send("40/online,")

        for func in self.handlers[SocketTypes.OPEN]:
            try:
                threading.Thread(target=func, args=[ws]).start()
            except Exception as e:
                raise HandlerError(str(e))

    def init(self) -> None:
        """
        Запускает веб сокет

        :return: None
        """

        url = "wss://starvell.com/socket.io/?EIO=4&transport=websocket"
        ws = websocket.WebSocketApp(
            url=url,
            cookie=f"session={self.s}",
            on_message=self.on_message,
            on_open=self.on_open,
        )
        ws.run_forever(reconnect=True)

    def run_socket(self) -> None:
        """
        Запускает веб сокет в отдельном потоке

        :return: None
        """

        threading.Thread(target=self.init).start()

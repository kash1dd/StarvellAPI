import websocket
import threading


from StarvellAPI.common.enums import SocketTypes

class Socket:
    def __init__(self, session_id: str, online: bool = True):
        """
        :param session_id: session_id со Starvell
        :param online: Поддерживать-ли постоянный онлайн? (True - при использовании API, аккаунт всегда будет в онлайне)
        """

        self.s = session_id
        self.online = online
        self.run_socket()

        self.other_handlers = {
            SocketTypes.OPEN: [],
            SocketTypes.NEW_MESSAGE: [],
            SocketTypes.ERROR: [] # todo добавить
        }

        self.event_types_tuple = ('ORDER_PAYMENT', 'REVIEW_CREATED', 'ORDER_COMPLETED', 'ORDER_REFUND', 'REVIEW_UPDATED', 'REVIEW_DELETED')

    def on_message(self, ws: websocket.WebSocket, msg: str) -> None:
        """
        Вызывается при новом сообщении в веб сокете, и соответственно вызывает все привязанные хэндлеры

        :param ws: Экземпляр класса WebSocket
        :param msg: Сообщение веб сокета

        :return: None
        """

        for func in self.other_handlers[SocketTypes.NEW_MESSAGE]:
            try:
                func(ws, msg)
            except Exception as e:
                print(f"Произошла ошибка в хэндлере вебсокета: {e}")

        if msg == "2":
            ws.send("3")

    def on_open(self, ws: websocket.WebSocket) -> None:
        """
        Вызывается при открытии веб сокета

        :param ws: Экземпляр класса WebSocket

        :return: None
        """

        ws.send("40/chats,")

        if self.online:
            ws.send('40/online,')

        for func in self.other_handlers[SocketTypes.OPEN]:
            try:
                threading.Thread(target=func, args=[ws]).start()
            except Exception as e:
                print(f"Произошла ошибка в хэндлере {func.__name__}: {e}")

    def init(self, **kwargs) -> None:
        """
        Запускает веб сокет

        :param kwargs: Аргументы, которые можно указать в классе WebSocketApp (Не используется на данный момент)

        :return: None
        """

        url = "wss://starvell.com/socket.io/?EIO=4&transport=websocket"
        ws = websocket.WebSocketApp(
            url,
            header={"cookie": f"session={self.s}"},
            on_message=self.on_message,
            on_open=self.on_open,
            **kwargs
        )
        ws.run_forever(reconnect=True)

    def run_socket(self) -> None:
        """
        Запускает веб сокет в отдельном потоке

        :return: None
        """

        threading.Thread(target=self.init).start()
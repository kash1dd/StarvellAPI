import websocket
import threading
import json

from StarvellAPI.models.new_msg import NewMessageEvent
from StarvellAPI.models.order_event import OrderEvent
from StarvellAPI.common.utils import format_message_types
from StarvellAPI.common.enums import MessageTypes

class Socket:
    def __init__(self, session_id: str, online: bool = True):
        """
        :param session_id: session_id со Starvell
        :param online: Поддерживать-ли постоянный онлайн? (Да - при использовании API, аккаунт всегда будет в онлайне)
        """

        self.s = session_id
        self.online = online
        self.run_socket()

        self.handlers = {
            MessageTypes.NEW_MESSAGE: [],
            MessageTypes.NEW_ORDER: [],
            MessageTypes.CONFIRM_ORDER: [],
            MessageTypes.ORDER_REFUND: [],
            MessageTypes.NEW_REVIEW: [],
            MessageTypes.REVIEW_DELETED: [],
            MessageTypes.REVIEW_CHANGED: []
        }
        self.event_types = {
            MessageTypes.NEW_MESSAGE: NewMessageEvent,
            MessageTypes.NEW_ORDER: OrderEvent,
            MessageTypes.CONFIRM_ORDER: OrderEvent,
            MessageTypes.ORDER_REFUND: OrderEvent,
            MessageTypes.NEW_REVIEW: OrderEvent,
            MessageTypes.REVIEW_DELETED: OrderEvent,
            MessageTypes.REVIEW_CHANGED: OrderEvent
        }
        self.event_types_tuple = ('ORDER_PAYMENT', 'REVIEW_CREATED', 'ORDER_COMPLETED', 'ORDER_REFUND', 'REVIEW_UPDATED', 'REVIEW_DELETED')

    def on_message(self, ws: websocket.WebSocket, msg: str) -> None:
        """
        Вызывается при новом сообщении в веб сокете, и соответственно вызывает все привязанные хэндлеры

        :param ws: Экземпляр класса WebSocket
        :param msg: Сообщение веб сокета
        """

        if msg.startswith('42/chats'):
            try:

                dict_with_data = json.loads(msg[len('42/chats,["message_created",'):-1])

                if dict_with_data['metadata'] is None or 'notificationType' not in dict_with_data['metadata']:
                    dict_with_data['type'] = MessageTypes.NEW_MESSAGE
                elif dict_with_data['metadata']['notificationType'] in self.event_types_tuple:
                    dict_with_data['type'] = format_message_types(dict_with_data['metadata']['notificationType'])

                dict_with_data['author'] = dict_with_data['author'] if 'author' in dict_with_data else dict_with_data['buyer']

                for event in self.handlers[dict_with_data['type']]:
                    data = self.event_types[dict_with_data['type']].model_validate(dict_with_data)
                    event(data)

            except Exception as e:
                print(e)

        elif msg == "2":
            ws.send("3")

    def on_open(self, ws: websocket.WebSocket) -> None:
        """
        Вызывается при открытии веб сокета

        :param ws: Экземпляр класса WebSocket
        """

        ws.send("40/chats,")

        if self.online:
            ws.send('40/online,')

    def init(self, **kwargs) -> None:
        """
        Запускает веб сокет

        :param kwargs: Аргументы, которые можно указать в классе WebSocketApp (Не используется)
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
        """

        threading.Thread(target=self.init).start()
from StarvellAPI.account import Account
from StarvellAPI.socket import Socket
from StarvellAPI.common.enums import MessageTypes, SocketTypes
from StarvellAPI.common.utils import format_message_types
from StarvellAPI.models.new_msg import NewMessageEvent
from StarvellAPI.models.order_event import OrderEvent

from websocket import WebSocket
import json
import threading

class Runner:
    def __init__(self, acc: Account, always_online: bool = True):
        """
        :param acc: Экземпляр класса Account
        :param always_online: Поддерживать-ли постоянный онлайн? (True - при использовании API, аккаунт всегда будет в онлайне)
        """

        self.acc = acc
        self.socket = Socket(acc.session_id, always_online)
        self.socket.other_handlers[SocketTypes.NEW_MESSAGE].append(self.msg_process)

        self.event_types_tuple = ('ORDER_PAYMENT', 'REVIEW_CREATED', 'ORDER_COMPLETED', 'ORDER_REFUND',
                                  'REVIEW_UPDATED', 'REVIEW_DELETED')
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


    def add_handler(self, event_type: MessageTypes):
        def decorator(func):
            self.handlers[event_type].append(func)
            return func
        return decorator

    def msg_process(self, _: WebSocket, msg: str):
        if msg.startswith('42/chats'):
            try:
                dict_with_data = json.loads(msg[len('42/chats,["message_created",'):-1])

                if dict_with_data['metadata'] is None or 'notificationType' not in dict_with_data['metadata']:
                    dict_with_data['type'] = MessageTypes.NEW_MESSAGE
                elif dict_with_data['metadata']['notificationType'] in self.event_types_tuple:
                    dict_with_data['type'] = format_message_types(dict_with_data['metadata']['notificationType'])

                dict_with_data['author'] = dict_with_data['author'] if 'author' in dict_with_data else dict_with_data['buyer']
                data = self.event_types[dict_with_data['type']].model_validate(dict_with_data)

                for handler in self.handlers[dict_with_data['type']]:
                    try:
                        threading.Thread(target=handler, args=[data]).start()
                    except Exception as e:
                        print(f"Ошибка в хэндлере {handler.__name__}: {e}")


            except Exception as e:
                print(f"Произошла ошибка в хэндлере сообщений вебсокета: {e}")
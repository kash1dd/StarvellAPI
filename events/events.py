from StarvellAPI.models.chat import Message
from StarvellAPI.account import Account

from typing import Generator
import time
from datetime import datetime, timedelta
import pytz

class Runner:
    def __init__(self, acc: Account):
        self.acc = acc

    def listen(self, request_delay: float | int) -> Generator[Message, None, None]:
        message_ids = []
        chats = self.acc.get_chats(0, 10000)

        for chat in chats:
            message_ids.append(chat.last_message.msg_id)

        while True:
            chatss = self.acc.get_chats(0, 10)
            for chats in chatss:
                last_message_id = chats.last_message.msg_id

                if last_message_id not in message_ids:
                    dt = chats.last_message.created_at
                    year = dt.year
                    month = dt.month
                    date = dt.day
                    hour = dt.hour
                    minute = dt.minute
                    second = dt.second
                    currently = datetime(year, month, date, hour, minute, second, tzinfo=pytz.UTC) - timedelta(
                        seconds=10, hours=3)

                    chat_history = self.acc.get_chat_history(chats.chat_id, 15)

                    for h in chat_history[::-1]:
                        if h.created_at > currently and h.msg_id not in message_ids:
                            message_ids.append(h.msg_id)
                            yield h
            time.sleep(request_delay)
from StarvellAPI.types import NewMessageEvent
from StarvellAPI.account import Account

import re

def is_command(msg: NewMessageEvent, symbol: str = "!"):
    """
    Начинается-ли текст с символа?

    :param msg: NewMessageEvent
    :param symbol: Символ с которого должно начинаться сообщение

    :return: bool (True - Да, False - Нет)
    """

    return msg.content.startswith(symbol)

def not_me(msg: NewMessageEvent, account: Account):
    """
    Являюсь автором сообщения я?

    :param msg: NewMessageEvent
    :param account: Экземпляр Account

    :return: bool (True - не является, False - Является)
    """

    return not msg.author.username == account.info.username

def has_email(msg: NewMessageEvent):
    """
    Есть-ли в тексте сообщения почта?

    :param msg: NewMessageEvent

    :return: bool (True - есть, False - нету)
    """

    regex = re.findall(r'\w+@\w+\.\w+', msg.content)

    if regex:
        return True

    return False

def has_images(msg: NewMessageEvent):
    """
    Есть-ли в сообщении изображение/я?

    :param msg: NewMessageEvent

    :return: bool (True - есть, False - нет)
    """

    if msg.images:
        return True

    return False
from starvellapi import Account, Runner
from starvellapi.enums import MessageTypes
from starvellapi.types import NewMessageEvent
from starvellapi.filters import is_command

acc = Account("session_id")  # session_id со Starvell
print(f"Привет {acc.username}!\n")
runner = Runner(acc)


@runner.add_handler(
    MessageTypes.NEW_MESSAGE, is_command, symbol="?"
)  # именованный аргумент symbol можно не указывать, значение по умолчанию там стоит "!"
def msg_hook(msg: NewMessageEvent) -> None:
    """
    Будет выполнять только в том случае, если текст сообщения начинается с symbol
    """

    print(msg.author.username, msg.content, sep=": ")

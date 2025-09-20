from StarvellAPI import Account, Runner
from StarvellAPI.enums import MessageTypes
from StarvellAPI.types import NewMessageEvent
from StarvellAPI.filters import is_command

acc = Account("session_id") # session_id со Starvell
print(f"Привет {acc.username}!\n")
runner = Runner(acc)

@runner.add_handler(MessageTypes.NEW_MESSAGE, is_command,
                    symbol="?") # именованный аргумент symbol можно не указывать, значение по умолчанию там стоит "!"
def msg_hook(msg: NewMessageEvent) -> None:
    """
    Будет выполнять только в том случае, если текст сообщения начинается с symbol
    """

    print(msg.author.username, msg.content, sep=': ')
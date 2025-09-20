from StarvellAPI import Account, Runner
from StarvellAPI.enums import MessageTypes
from StarvellAPI.types import NewMessageEvent
from StarvellAPI.filters import has_email

acc = Account("session_id")  # session_id со Starvell
print(f"Привет {acc.username}!\n")
runner = Runner(acc)

@runner.add_handler(MessageTypes.NEW_MESSAGE, has_email) # не указываем никаких дополнительных именованных аргументов
def msg_hook(msg: NewMessageEvent) -> None:
    """
    Будет выполнять только в том случае, если в тексте сообщения есть почта
    """

    print(msg.author.username, msg.content, sep=': ')
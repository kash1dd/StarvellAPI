from starvell import Account, Runner
from starvell.enums import MessageTypes
from starvell.types import NewMessageEvent
from starvell.filters import not_me

acc = Account("session_id")  # session_id со Starvell
print(f"Привет {acc.username}!\n")
runner = Runner(acc)


@runner.add_handler(
    MessageTypes.NEW_MESSAGE, not_me, account=acc
)  # обязательно указывать именованный аргумент account, и передаём туда экземпляр Account
def msg_hook(msg: NewMessageEvent) -> None:
    """
    Будет выполнять только в том случае, если автором сообщения не является имя аккаунта
    """

    print(msg.author.username, msg.content, sep=": ")

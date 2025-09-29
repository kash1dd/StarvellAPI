from StarvellAPI.enums import MessageTypes
from StarvellAPI.types import NewMessageEvent
from StarvellAPI.account import Account
from StarvellAPI.events import Runner

acc = Account("41363d86-f386-4e38-818e-a0b546dcee3a")
runner = Runner(acc)

@runner.add_handler(MessageTypes.NEW_MESSAGE)
def msg_hook(msg: NewMessageEvent):
    print(msg.author.username, msg.content, sep=': ')
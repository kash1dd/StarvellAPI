from starvellapi.enums import MessageTypes
from starvellapi.types import NewMessageEvent
from starvellapi.account import Account
from starvellapi.events import Runner

acc = Account("41363d86-f386-4e38-818e-a0b546dcee3a")
runner = Runner(acc)

@runner.add_handler(MessageTypes.NEW_MESSAGE)
def msg_hook(msg: NewMessageEvent):
    print(msg.author.username, msg.content, sep=': ')
from StarvellAPI.account import Account
from StarvellAPI.socket import Socket

class Runner:
    def __init__(self, acc: Account):
        self.acc = acc
        self.socket = Socket(acc.session_id)

    def msg_handler(self, func):
        self.socket.event_handlers.append(func)
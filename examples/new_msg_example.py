from starvellapi import Account, Runner
from starvellapi.enums import MessageTypes
from starvellapi.types import NewMessageEvent

acc = Account("session_id")  # session_id со Starvell
print(f"Привет {acc.username}!\n")
runner = Runner(acc)

@runner.add_handler(MessageTypes.NEW_MESSAGE) # можем указать дополнительный фильтр, в таком случае будет выполняться только в том случае, если функция-предикат вернёт True
def msg_hook(msg: NewMessageEvent) -> None:
    """
    Будет выполняться при новом сообщении
    """

    print(msg.author.username, msg.content, sep=': ')

# пример с использованием фильтра

def my_filter(msg: NewMessageEvent) -> bool:
    """
    Функция-предикат

    Возвращает True если сообщение начинается с "!", иначе False
    """

    return msg.content.startswith('!')

@runner.add_handler(MessageTypes.NEW_MESSAGE, my_filter) # указываем нашу функцию-предикат в качестве фильтра
def msg_hook_with_filter(msg: NewMessageEvent) -> None:
    """
    Будет выполняться только в том случае, если функция-предикат вернёт True
    """

    print(f"Пользователь {msg.author.username} отправил сообщение, которое начинается с !")
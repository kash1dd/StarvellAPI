# Первое API для Starvell на Python!

---
### 📕 _Информация_
* __API Полностью синхронное__
* __API Полностью написано с использованием ООП__
* __Все JSON Ответы от Starvell валидируются pydantic'ом__
---
### _🤖 Пример использования_
```
from StarvellAPI.account import Account
from StarvellAPI.events.events import Runner
from StarvellAPI.models.new_msg import NewMessageEvent

acc = Account("session_id") # создаём экземпляр аккаунта, указывая session_id полученный со starvell.com

print(f"Никнейм - {acc.username}")
print(f"ID - {acc.id}")

runner = Runner(acc) # создаём экземпляр раннера

def message(msg: NewMessageEvent):
    """
    Хэндлер, который обрабатывает новое сообщение
    """

    if msg.type is msg.type.NEW_MESSAGE: # проверяем, является ли тип сообщения, именно сообщением
        print(msg.author.username, msg.content, sep=': ') # выводим новое сообщение

runner.msg_handler(message) # добавляем функцию в хэндлеры
```
___
### ❓ _Прочее_
* [Чат в Telegram](https://t.me/starvell_api)

### ⭐ Звездочки
* Если тебе показалось удобным использование этого API - Поставь звезду (__Star it__), мне будет приятно :)
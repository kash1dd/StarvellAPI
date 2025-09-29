# Starvell API на Python

---
### 📕 _Информация_
* __API Полностью синхронное__
* __API Полностью написано с использованием ООП__
* __Все JSON Ответы от Starvell валидируются с помощью `Pydantic`__
* __API Активно разрабатывается, и постепенно улучшается__
---
### 👨‍💻 Стек
* __`pydantic`__
* __`websocket-client`__
* __`requests`__
___
### 👑 Требования
* __Python >= 3.10__
* __Рекомендуемая версия Python: [3.13.7](https://www.python.org/downloads/release/python-3137/)__
___
### _🤖 Пример использования_

```python
from starvellapi import Account, Runner
from starvellapi.types import NewMessageEvent, OrderEvent
from starvellapi.enums import MessageTypes

acc = Account("session_id")  # создаём экземпляр аккаунта, указывая session_id полученный со starvell.com

print(f"Никнейм - {acc.info.username}")
print(f"ID - {acc.info.id}\n")

runner = Runner(acc)  # создаём экземпляр раннера


@runner.add_handler(MessageTypes.NEW_MESSAGE)  # с помощью декоратора, добавляем нашу функцию в хэндлеры новых сообщений
def msg_handler(msg: NewMessageEvent):
    """
    Хэндлер (функция), которая будет вызываться при новом сообщении
    """

    print(f"{msg.author.username}: {msg.content}")


@runner.add_handler(MessageTypes.NEW_ORDER)  # с помощью декоратора, добавляем нашу функцию в хэндлеры новых заказов
def order_handler(order: OrderEvent):
    """
    Хэндлер (функция), которая будет вызываться при новом заказе
    """

    print(f"Покупатель {order.buyer.username} оплатил заказ {order.order.id}")
```
* [Все примеры использования](https://github.com/kash1dd/StarvellAPI/tree/main/examples)
___
### ❓ _Прочее_
* [Чат в Telegram](https://t.me/starvell_api)

### ⭐ Звездочки
* Если тебе показалось удобным использование этого API - Поставь звезду (__Star it__), мне будет приятно :)
# Первое API для Starvell на Python!

---
### 📕 _Информация_
* __API Полностью синхронное__
* __API Полностью написано с использованием ООП__
* __Все JSON Ответы от Starvell валидируются pydantic'ом__
---
### _🤖 Пример использования_
```python
from StarvellAPI.account import Account
from StarvellAPI.events.events import Runner
from StarvellAPI.models.new_msg import NewMessageEvent
from StarvellAPI.models.order_event import OrderEvent
from StarvellAPI.common.enums import MessageTypes

acc = Account("session_id") # создаём экземпляр аккаунта, указывая session_id полученный со starvell.com

print(f"Никнейм - {acc.username}")
print(f"ID - {acc.id}\n")

runner = Runner(acc) # создаём экземпляр раннера

def msg_handler(msg: NewMessageEvent):
    """
    Хэндлер новых сообщений
    """

    print(msg.author.username, msg.content, sep=': ')

def review_handler(order: OrderEvent):
    """
    Хэндлер новых отзывов
    """

    print(f"Новый отзыв в заказе: {order.order.id}")

def review_changed(order: OrderEvent):
    """
    Хэндлер ивента на изменение отзыва
    """

    print(f"Пользователь {order.buyer.username} изменил отзыв в заказе {order.order.id}")

runner.add_handler(msg_handler, MessageTypes.NEW_MESSAGE) # добавляем наш хэндлер новых сообщений
runner.add_handler(review_handler, MessageTypes.NEW_REVIEW) # добавляем наш хэндлер новых отзывов
runner.add_handler(review_changed, MessageTypes.REVIEW_CHANGED) # добавляем наш хэндлер на ивент изменения отзыва
```
___
### ❓ _Прочее_
* [Чат в Telegram](https://t.me/starvell_api)

### ⭐ Звездочки
* Если тебе показалось удобным использование этого API - Поставь звезду (__Star it__), мне будет приятно :)
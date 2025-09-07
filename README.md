# Starvell API на Python

---
### 📕 _Информация_
* __API Полностью синхронное__
* __API Полностью написано с использованием ООП__
* __Все JSON Ответы от Starvell валидируются с помощью `Pydantic`__
* __API Активно разрабатывается, и постепенно улучшается__
---
### _🤖 Пример использования_
```python
from StarvellAPI.account import Account
from StarvellAPI.events.events import Runner
from StarvellAPI.common.enums import MessageTypes
from StarvellAPI.models.new_msg import NewMessageEvent
from StarvellAPI.models.order_event import OrderEvent

acc = Account("session_id") # создаём экземпляр аккаунта, указывая session_id полученный со starvell.com

print(f"Никнейм - {acc.username}")
print(f"ID - {acc.id}\n")

runner = Runner(acc) # создаём экземпляр раннера

@runner.add_handler(MessageTypes.NEW_MESSAGE) # декоратор на новое сообщение
def msg_handler(msg: NewMessageEvent):
    """
    Хэндлер (функция), которая будет вызываться при новом сообщении
    """
    
    print(f"{msg.author.username}: {msg.content}")

@runner.add_handler(MessageTypes.NEW_ORDER) # декоратор на новый заказ
def order_handler(order: OrderEvent):
    """
    Хэндлер (функция), которая будет вызываться при новом заказе
    """
    
    print(f"Покупатель {order.buyer.username} оплатил заказ {order.order.id}")
```
___
### ❓ _Прочее_
* [Чат в Telegram](https://t.me/starvell_api)

### ⭐ Звездочки
* Если тебе показалось удобным использование этого API - Поставь звезду (__Star it__), мне будет приятно :)
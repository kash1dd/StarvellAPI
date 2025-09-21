from StarvellAPI.session import StarvellSession
from .enums import MessageTypes, PaymentTypes
from .errors import (
    SendReviewError,
    SendMessageError,
    RefundError,
    BlockError,
    EditReviewError,
    UnBlockError,
    WithdrawError,
    CreateLotError,
    ReadChatError,
    DeleteLotError,
    SaveSettingsError,
    UserNotFoundError,
    RequestFailedError,
    GetReviewError,
    ReviewNotFoundError,
    SendImageError,
    SendTypingError
)
from .utils import (
    format_order_status,
    format_types,
    format_message_types,
    format_payment_methods,
    format_statuses,
    format_directions
)
from .types import (
    MyProfile,
    PreviewSettings,
    OrderInfo,
    ReviewInfo,
    TransactionInfo,
    ChatInfo,
    Message,
    Order,
    OfferTableInfo,
    LotFields,
    BlockListedUser,
    User,
    CreateLotFields,
    ExchangeRate
)

from datetime import datetime
from typing import Optional, Any

import json

class Account:
    def __init__(self, session_id: str, proxy: dict[str, str] | None = None) -> None:
        """
        :param session_id: ID Сессии на Starvell
        :param proxy: Прокси с которого будут осуществляться запросы (пример: {"http": "http://user:password@your_proxy_ip:port"})
        """

        # информация об аккаунте
        self.username: str | None = None
        self.id: int | None = None
        self.session_id: str = session_id
        self.email: str | None = None
        self.created_date: datetime | None = None
        self.avatar_id: str | None = None
        self.banner_id: str | None = None
        self.description: str | None = None
        self.is_verified: bool | None = None
        self.rating: int | float | None = None
        self.reviews_count: int | None = None
        self.balance_hold: float | None = None
        self.balance: float | None = None
        self.active_orders: int | None = None

        # прочее
        self.proxy: dict[str, str] | None = proxy
        self.request: StarvellSession = StarvellSession(session_id, self.proxy)

        # авто запуск
        self.get_info()

    def get_info(self) -> MyProfile:
        """
        Получает информацию об аккаунте.
        
        :return: Возвращает модель Profile
        """

        url = "https://starvell.com/api/users-profile"
        response = MyProfile.model_validate(self.request.get(url=url, raise_not_200=True).json())

        self.username = response.user.username
        self.id = response.user.id
        self.email = response.user.email
        self.created_date = response.user.created_at
        self.avatar_id = response.user.avatar
        self.banner_id = response.user.banner
        self.description = response.user.description
        self.is_verified = response.user.is_kyc_verified
        self.rating = response.user.rating
        self.reviews_count = response.user.reviews_count
        self.balance_hold = response.holded_balance / 100
        self.balance = response.balance.rub_balance / 100 if \
        isinstance(response.balance.rub_balance, int) else None
        self.active_orders = response.active_orders.sales

        return response

    def get_settings(self) -> PreviewSettings:
        """
        Получает настройки аккаунта.

        :return: Настройки пользователя
        """

        url = "https://starvell.com/api/user/settings"
        response = self.request.get(url=url, raise_not_200=True).json()
        return PreviewSettings.model_validate(response)


    def get_sales(self, offset: int = 0, limit: int = 100000000, filter_sales: dict[str, Any] | None = None) -> list[OrderInfo]:
        """
        Получает продажи.

        :param offset: С какой продажи начинать? (По умолчанию с 0)
        :param limit: Количество продаж
        :param filter_sales: Фильтр который можно установить в JSON запроса

        :return: Список с продажами
        """

        default: dict[str, str] = {"userType": "seller"}

        url = "https://starvell.com/api/orders/list"
        body = {
            "filter": default if filter_sales is None else filter_sales,
            "with": {
                "buyer": True
            },
            "orderBy": {
                "field": "createdAt",
                "order": "DESC"
            },
            "limit": limit,
            "offset": offset
        }
        response = self.request.post(url, body, raise_not_200=True)

        list_with_sales = []
        orders = response.json()

        for obj in orders:
            obj['status'] = format_order_status(obj['status'])
            ord_2 = OrderInfo.model_validate(obj)
            list_with_sales.append(ord_2)

        return list_with_sales

    def get_reviews(self, offset: int = 0, limit: int = 100000000) -> list[ReviewInfo]:
        """
        Получает отзывы профиля.

        :param offset: С какого отзыва начинать? (По умолчанию с 0)
        :param limit: Количество отзывов, которое надо получить (По умолчанию все)

        :return: Список с отзывами
        """

        url = "https://starvell.com/api/reviews/list"
        body = {
            "filter": {
                "recipientId": self.id
            },
            "pagination": {
                "offset": offset,
                "limit": limit
            }
        }
        response = self.request.post(url, body, raise_not_200=True).json()

        return [ReviewInfo.model_validate(i) for i in response]

    def get_transactions(self, offset: int = 0, limit: int = 100000000) -> list[TransactionInfo]:
        """
        Получает транзакции.

        :param offset: С какой транзакции начинать? (По умолчанию с 0)
        :param limit: Количество транзакций, которое надо получить (По умолчанию все)

        :return: Список с транзакциями
        """

        url = "https://starvell.com/api/transactions/list"
        body = {
            "filter": {},
            "limit": limit,
            "offset": offset
        }
        response = self.request.post(url, body, raise_not_200=True)

        list_with_transactions = []
        transactions = response.json()

        for t in transactions:
            t['direction'] = format_directions(t['direction'])
            t['type'] = format_types(t['type'])
            t['status'] = format_statuses(t['status'])
            t = TransactionInfo.model_validate(t)
            list_with_transactions.append(t)

        return list_with_transactions

    def get_chats(self, offset: int, limit: int) -> list[ChatInfo]:
        """
        Получает чаты.

        :param offset: С какого чата начинать
        :param limit: Количество чатов, которое надо получить

        :return: Список с чатами
        """

        url = "https://starvell.com/api/chats/list"
        body = {
            "offset": offset,
            "limit": limit
        }
        response = self.request.post(url, body=body, raise_not_200=True).json()

        return [ChatInfo.model_validate(i) for i in response]

    def get_chat(self, chat_id: str, limit: int) -> list[Message]:
        """
        Получает историю сообщений чата.

        :param chat_id: ID Чата
        :param limit: Количество сообщений, которое надо получить

        :return: Список с сообщениями в чате
        """

        url = "https://starvell.com/api/messages/list"
        body = {
            "chatId": str(chat_id),
            "limit": limit
        }
        messages = []

        response = self.request.post(url, body, raise_not_200=True).json()

        for r in response:
            if r['metadata'] is None or 'notificationType' not in r['metadata']:
                r['event_type'] = MessageTypes.NEW_MESSAGE
            else:
                if r['metadata']['notificationType'] in ('ORDER_PAYMENT', 'REVIEW_CREATED', 'ORDER_COMPLETED', 'ORDER_REFUND', 'REVIEW_UPDATED', 'REVIEW_DELETED'):
                    r['event_type'] = format_message_types(r['metadata']['notificationType'])
                else:
                    continue

            r['author'] = r['author'] if r['author'] else r['buyer']
            messages.append(Message.model_validate(r))

        return messages

    def get_order(self, order_id: str) -> Order:
        """
        Получает полную информацию об заказе.

        :param order_id: ID Заказа

        :return: Полная информация об заказе
        """

        url = f"https://starvell.com/api/orders/{order_id}"
        body = {
            "orderId": order_id
        }

        response = self.request.get(url, body, raise_not_200=True).json()
        response['status'] = format_order_status(response['status'])
        response['basePrice'] = response['basePrice'] / 100 if isinstance(response['basePrice'], int) else 0
        response['totalPrice'] = response['totalPrice'] / 100 if isinstance(response['totalPrice'], int) else 0
        return Order.model_validate(response)

    def get_review(self, order_id: str) -> ReviewInfo:
        """
        Получает отзыв по ID Заказа

        :param order_id: ID Заказа

        :return: ReviewInfo
        """

        url = f"https://starvell.com/api/reviews/by-order-id"
        param = {
            "id": order_id
        }

        response = self.request.get(url=url, params=param, raise_not_200=False)

        if response.status_code == 404:
            raise ReviewNotFoundError(response.json().get('message'))

        if response.status_code != 200:
            raise GetReviewError(response.json().get('message'))

        return ReviewInfo.model_validate(response.json())


    def get_category_lots(self, category_id: int,
                          offset: int = 0,
                          limit: int = 100000000,
                          only_online: bool = False,
                          other_filters: dict[str, str] | None = None) -> list[OfferTableInfo]:
        """
        Получает лоты категории.

        :param category_id: ID Категории
        :param offset: С какого лота начинать (По умолчанию с 0)
        :param limit: Количество лотов, которое нужно получить (По умолчанию все лоты)
        :param only_online: Только онлайн продавцы? (По умолчанию False)

        :return: Список с лотами
        """

        url = "https://starvell.com/api/offers/list-by-category"
        body = {
            "categoryId": category_id,
            "onlyOnlineUsers": only_online,
            "attributes": [],
            "numericRangeFilters": [],
            "limit": limit,
            "offset": offset,
            "sortBy": "price",
            "sortDir": "ASC",
            "sortByPriceAndBumped": True
        }

        if other_filters:
            body.update(**other_filters)

        response = self.request.post(url, body, raise_not_200=True).json()

        return [OfferTableInfo.model_validate(i) for i in response]

    def get_my_category_lots(self, category_id: int, offset: int = 0, limit: int = 10000000) -> list[LotFields]:
        """
        Получает свои лоты категории.

        :param category_id: ID Категории
        :param offset: С какого лота начинать (По умолчанию 0)?
        :param limit: Сколько лотов получить? (По умолчанию все)?

        :return: Список с лотами (list[LotFields])
        """

        url = "https://starvell.com/api/offers/list-my"
        body = {
            "categoryId": category_id,
            "limit": limit,
            "offset": offset
        }

        response = self.request.post(url, body=body, raise_not_200=True).json()

        return [LotFields.model_validate(i) for i in response]

    def get_lot_fields(self, lot_id: int) -> LotFields:
        """
        Получает все поля лота.

        :param lot_id: ID Лота

        :return: LotFields
        """

        url = f"https://starvell.com/api/offers/{lot_id}"
        response = self.request.get(url, raise_not_200=True).json()

        return LotFields.model_validate(response)

    def get_black_list(self) -> list[BlockListedUser]:
        """
        Получает список заблокированных пользователей на Starvell.

        :return: List[BlockListedUser]
        """

        url = "https://starvell.com/api/blacklisted-users/list"
        response = self.request.post(url).json()

        return [BlockListedUser.model_validate(i) for i in response]

    def get_user(self, user_id: str | int) -> User:
        """
        Получает информацию об профиле пользователя.

        :param user_id: ID Пользователя

        :return: Полная информация об пользователе
        """

        url = f"https://starvell.com/api/users/{user_id}"
        response = self.request.get(url=url, raise_not_200=False)

        if response.status_code == 404:
            raise UserNotFoundError(response.json().get('message'))
        elif response.status_code != 200:
            raise RequestFailedError(response)

        return User.model_validate(response)

    def get_usdt_rub_exchange_rate(self) -> ExchangeRate:
        """
        Получает курс USDT к рублю на Starvell

        :return: ExchangeRate
        """

        return ExchangeRate.model_validate(
            self.request.get(url="https://starvell.com/api/exchange-rates/usdt-rub").json())

    def get_usdt_ltc_exchange_rate(self) -> ExchangeRate:
        """
        Получает курс USDT к LTC на Starvell

        :return: ExchangeRate
        """

        return ExchangeRate.model_validate(
            self.request.get(url="https://starvell.com/api/exchange-rates/usdt-ltc").json())

    def create_lot(self, fields: LotFields) -> LotFields:
        """
        Создаёт лот на Starvell.

        :param fields: LotFields

        :return: LotFields созданного лота
        :raise CreateLotError: Если произошла ошибка при создании лота
        """

        url = "https://starvell.com/api/offers-operations/create"

        lot_fields = json.loads(fields.model_dump_json(by_alias=True))
        lot_fields['numericAttributes'] = lot_fields['attributes']
        create_fields = json.loads(CreateLotFields.model_validate(lot_fields).model_dump_json(by_alias=True))

        response = self.request.post(url, create_fields, raise_not_200=False)

        if response.status_code != 201:
            raise CreateLotError(response.json().get('message'))

        return LotFields.model_validate(response.json())

    def delete_lot(self, lot_id: int):
        """
        Удаляет лот со Starvell.

        :param lot_id: ID Лота

        :return: None
        :raise DeleteLotError: Если произошла ошибка при удалении лота
        """

        url = f"https://starvell.com/api/offers/{lot_id}/delete"
        response = self.request.post(url, raise_not_200=False)
        js = response.json()

        if response.status_code != 200:
            raise DeleteLotError(js.get('message'))

    def send_message(self, chat_id: str, content: str, read_chat: bool = True) -> None:
        """
        Отправляет сообщение в чат.

        :param chat_id: ID Чата
        :param content: Текст, который нужно отправить
        :param read_chat: Прочитывать-ли чат, после отправки сообщения?

        :return: None
        :raise SendMessageError: Если произошла ошибка при отправке сообщения
        """

        url = "https://starvell.com/api/messages/send"
        body = {
            "chatId": chat_id,
            "content": f"‎{content}",
        }
        response = self.request.post(url, body, raise_not_200=False)

        if response.status_code != 201:
            raise SendMessageError(response.json().get('message'))

        if read_chat:
            self.read_chat(chat_id)

    def send_image(self, chat_id: str, image_bytes: bytes, read_chat: bool = True) -> None:
        """
        Отправляет изображение в чат

        :param chat_id: ID Чата
        :param image_bytes: Байты изображения
        :param read_chat: Прочитывать-ли чат, после отправки изображения?

        :return: None
        """

        url = "https://starvell.com/api/messages/send-with-image"
        param = {
            "chatId": chat_id
        }
        files = {
            "image": ("StarvellAPI.png", image_bytes, "image/png")
        }

        response = self.request.post(url=url,  files=files, params=param, raise_not_200=False)

        if response.status_code != 201:
            raise SendImageError(response.json().get("message"))

        if read_chat:
            self.read_chat(chat_id)

    def read_chat(self, chat_id: str) -> None:
        """
        Помечает чат прочитанным.

        :param chat_id: ID Чата

        :return: None
        :raise ReadChatError: Если произошла ошибка при чтении чата
        """

        url = "https://starvell.com/api/chats/read"
        body = {
            "chatId": chat_id
        }

        response = self.request.post(url, body, raise_not_200=False)

        if response.status_code != 200:
            raise ReadChatError(response.json().get('message'))

    def save_lot(self, lot: LotFields) -> None:
        """
        Сохраняет лот с переданными полями.

        :param lot: Поля лота (Класс LotFields)

        :return: None
        """

        url = f"https://starvell.com/api/offers-operations/{lot.id}/update"
        data = lot.model_dump(by_alias=True)

        if "subCategory" in data:
            data.pop("subCategory")

        for key, value in data.items():
            if type(value) is datetime:
                data[key] = value.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        self.request.post(url, data, raise_not_200=False)

    def send_review(self, review_id: str, content: str) -> None:
        """
        Отправляет ответ на отзыв только в том случае, если на отзыв ещё нет ответа.

        :param review_id: ID Отзыва, на который нужно ответить
        :param content: Текст ответа

        :return: None
        :raise SendReviewError: Если произошла ошибка при отправке отзыва
        """

        url = "https://starvell.com/api/review-responses/create"
        body = {
            "content": content,
            "reviewId": review_id
        }
        response = self.request.post(url, body, raise_not_200=False)

        if response.status_code != 200:
            raise SendReviewError(response.json().get('message'))

    def edit_review(self, review_id: str, content: str):
        """
        Редактирует ответ на отзыв.
        
        Именно редактирует, если на отзыв ещё нет ответа, может возникнуть ошибка
        
        :param review_id: ID Отзыва, на который нужно изменить ответ
        :param content: Текст ответа

        :return: None
        :raise EditReviewError: Если произошла ошибка при редактировании отзыва
        """

        url = f"https://starvell.com/api/review-responses/{review_id}/update"
        body = {
            "content": content,
            "reviewId": review_id
        }
        response = self.request.post(url, body, raise_not_200=False)

        if response.status_code != 200:
            raise EditReviewError(response.json().get('message'))

    def refund(self, order_id: str):
        """
        Оформляет возврат в заказе.

        :param order_id: ID Заказа

        :return: None
        :raise RefundError: Если произошла ошибка при возврате
        """

        url = "https://starvell.com/api/orders/refund"
        body = {
            "orderId": order_id
        }

        response = self.request.post(url, body, raise_not_200=False)

        if response.status_code != 200:
            raise RefundError(response.json().get('message'))

    def withdraw(self, payment_system: PaymentTypes, requisite: str, amount: float, bank=None):
        """
        Создаёт заявку на вывод средств.

        :param payment_system: Тип платёжной системы для вывода
        :param requisite: Реквизиты для вывода (Номер карты / Номер СБП / Адрес крипты)
        :param amount: Сумма для вывода
        :param bank: Только если вывод с помощью СБП, тогда указывай там айди банка, иначе даже не трогай

        :return: None
        :raise WithdrawError: Если произошла ошибка при выводе
        """

        url = "https://starvell.com/api/payouts/create"
        body = {
            "paymentSystemId": format_payment_methods(payment_system),
            "amount": amount * 100,
            "address": requisite,
            'cardHolder' if payment_system is not PaymentTypes.SBP else 'sbpBankId': "StarvellAPI" if payment_system is not PaymentTypes.SBP else bank
        }

        response = self.request.post(url, body, raise_not_200=False).json()

        if response.status_code != 200:
            raise WithdrawError(response.get('message'))


    def save_settings(self, is_offers_visible: bool, updated_parameter: Optional[dict[str, Any]] = None):
        """
        Сохраняет настройки аккаунта.

        :param is_offers_visible: Отображать-ли лоты в профиле?
        :param updated_parameter: Обновлённый параметр (словарь (обновлённый параметр: значение)), если требовалось изменение только видимости лотов, то можно не указывать

        :raise SaveSettingsError: При какой-либо ошибке сохранения настроек
        :return: None
        """

        url = "https://starvell.com/api/user/settings"
        body: dict[str, str | bool | None] = {
            "avatar": self.avatar_id,
            "email": self.email,
            "isOffersVisibleOnlyInProfile": is_offers_visible,
            "username": self.username
        }
        if updated_parameter:
            body.update(**updated_parameter)

        response = self.request.patch(url, body, raise_not_200=False)

        if response.status_code != 200:
            raise SaveSettingsError(response.json().get('message'))

    def block(self, user_id: int):
        """
        Отправляет пользователя в ЧС на Starvell.

        :param user_id: ID Пользователя, которого нужно заблокировать

        :return: None
        :raise BlockError: Если произошла ошибка при блокировке
        """

        url = "https://starvell.com/api/blacklisted-users/block"
        body: dict[str, int] = {
            "targetId": user_id
        }

        response = self.request.post(url, body, raise_not_200=False)

        if response.status_code != 200:
            raise BlockError(response.json().get('message'))

    def unblock(self, user_id: int):
        """
        Удаляет пользователя из ЧС на Starvell.

        :param user_id: ID Пользователя, которого нужно удалить

        :return: None
        :raise UnBlockError: Если произошла ошибка при разблокировке
        """

        url = "https://starvell.com/api/blacklisted-users/unblock"
        body: dict[str, int] = {
            "targetId": user_id
        }

        response = self.request.post(url, body, raise_not_200=False)

        if response.status_code != 200:
            raise UnBlockError(response.json().get('message'))

    def send_typing(self, chat_id: str, is_typing: bool) -> None:
        """
        Отправляет "Печатает..." в чат на 5 секунд

        :param chat_id: ID Чата
        :param is_typing: bool - Отправляет "Печатает...", False - Останавливает "Печатает..."

        :return: None
        """

        url = "https://starvell.com/api/chats/send-typing"
        body = {
            "chatId": chat_id,
            "isTyping": is_typing
        }

        response = self.request.post(url=url, body=body, raise_not_200=False)

        if response.status_code != 200:
            raise SendTypingError(response.json().get('message'))
# todo
# удалить StarvellAPI.models.profile_offers import OfferInfoShortCut

from datetime import datetime
import re
import json

from StarvellAPI.session import StarvellSession

from StarvellAPI.common.utils import format_directions, format_types, format_statuses, format_order_status, format_message_types, format_payment_methods
from StarvellAPI.common.enums import MessageTypes, PaymentTypes
from StarvellAPI.common.exceptions import WithdrawError, SendMessageError, ReadChatError, RefundError, EditReviewError, \
    SendReviewError
from StarvellAPI.models.order import OrderFullInfo
from StarvellAPI.models.preview_order import OrderInfo
from StarvellAPI.models.review import ReviewInfo
from StarvellAPI.models.transaction import TransactionInfo
from StarvellAPI.models.chats import ChatInfo
from StarvellAPI.models.chat import Message
from StarvellAPI.models.offers_list import OfferTableInfo
from StarvellAPI.models.offer_fields import LotFields
from StarvellAPI.models.user import User
from StarvellAPI.models.settings import PreviewSettings
from StarvellAPI.models.profile import Profile

class Account:
    def __init__(self, session_id: str):
        # инфа об аккаунте
        self.username: str | None = None
        self.id: int | None = None
        self.build_id: str | None = None
        self.session_id: str | None = session_id
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
        self.request = StarvellSession(session_id)

        # авто запуск
        self.get_info()
        self.get_build()

    def get_build(self) -> None:
        """
        Получает BUILD ID для некоторых запросов

        :return: None
        """

        url = "https://starvell.com"
        response = self.request.get(url=url, raise_not_200=True).text

        match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', response, re.S)
        data = json.loads(match.group(1))
        self.build_id = data['buildId']

    def get_info(self) -> Profile:
        """
        Получает профиль, пока-что не реализована в мейне

        :return: Возвращает модель Profile
        """

        url = "https://starvell.com/api/users-profile"
        response = Profile.model_validate(self.request.get(url=url, raise_not_200=True).json())

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
        self.balance_hold = response.holded_balance
        self.balance = response.balance.rub_balance
        self.active_orders = response.active_orders

        return response

    def get_settings(self) -> PreviewSettings:
        """
        Получает настройки аккаунта

        :return: Настройки пользователя
        """

        url = "https://starvell.com/api/user/settings"
        response = self.request.get(url=url, raise_not_200=True).json()
        return PreviewSettings.model_validate(response)

    def get_sales(self, offset: int, limit: int) -> list[OrderInfo]:
        """
        Получает продажи

        :param offset: С какой продажи начинать
        :param limit: Количество продаж, которое надо получить

        :return: Список с продажами
        """

        url = "https://starvell.com/api/orders/list"
        body = {
  "filter": {
    "userType": "seller"
  },
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

    def get_reviews(self, offset: int, limit: int) -> list[ReviewInfo]:
        """
        Получает отзывы профиля

        :param offset: С какого отзыва начинать
        :param limit: Количество отзывов, которое надо получить

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
        response = self.request.post(url, body, raise_not_200=True)

        list_with_reviews = []
        reviews = response.json()

        for review in reviews:
            r = ReviewInfo.model_validate(review)
            list_with_reviews.append(r)

        return list_with_reviews

    def get_transactions(self, offset: int, limit: int) -> list[TransactionInfo]:
        """
        Получает транзакции

        :param offset: С какой транзакции начинать
        :param limit: Количество транзакций, которое надо получить

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

        for transaction in transactions:
            transaction['direction'] = format_directions(transaction['direction'])
            transaction['type'] = format_types(transaction['type'])
            transaction['status'] = format_statuses(transaction['status'])
            t = TransactionInfo.model_validate(transaction)
            list_with_transactions.append(t)

        return list_with_transactions

    def get_order(self, order_id: str) -> OrderFullInfo:
        """
        Получает полную информацию об заказе

        :param order_id: ID Заказа

        :return: Полная информация об заказе
        """

        url = f"https://starvell.com/_next/data/{self.build_id}/order/{str(order_id)}.json?order_id={str(order_id)}"
        body = {
            "order_id": str(order_id)
        }

        response = self.request.get(url, body, raise_not_200=True).json()

        return OrderFullInfo.model_validate(response['pageProps'])

    def get_chats(self, offset: int, limit: int) -> list[ChatInfo]:
        """
        Получает чаты

        :param offset: С какого чата начинать
        :param limit: Количество чатов, которое надо получить

        :return: Список с чатами
        """

        chats = []
        url = "https://starvell.com/api/chats/list"
        body = {
            "offset": offset,
            "limit": limit
        }
        response = self.request.post(url, body=body, raise_not_200=True).json()

        for r in response:
            chats.append(ChatInfo.model_validate(r))
        return chats

    def get_chat(self, chat_id: str, limit: int) -> list[Message]:
        """
        Получает историю сообщений чата

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

    def send_message(self, content: str, chat_id: str, read_chat: bool = True) -> None:
        """
        Отправляет сообщение в чат

        :param content: Текст, который нужно отправить
        :param chat_id: ID Чата
        :param read_chat: Прочитывать-ли чат, после отправки сообщения?

        :return: None
        """

        url = "https://starvell.com/api/messages/send"
        body = {
            "chatId": chat_id,
            "content": f"{content} ",
        }
        response = self.request.post(url, body, raise_not_200=False).json()

        if not response['success']:
            raise SendMessageError(response['message'])

        if read_chat:
            self.read_chat(chat_id)

    def read_chat(self, chat_id: str) -> None:
        """
        Помечает чат прочитанным

        :param chat_id: ID Чата

        :return: None
        """

        url = "https://starvell.com/api/chats/read"
        body = {
            "chatId": chat_id
        }

        response = self.request.post(url, body, raise_not_200=False).json()

        if not response['success']:
            raise ReadChatError(response['message'])


    def get_category_lots(self, category_id: int, limit: int, offset: int, only_online: bool = False) -> list[OfferTableInfo]:
        """
        Получает лоты категории

        :param category_id: ID Категории
        :param limit: Количество лотов, которое нужно получить
        :param offset: С какого лота начинать
        :param only_online: Только онлайн продавцы

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
        list_with_offers = []

        response = self.request.post(url, body, raise_not_200=True).json()

        for r in response:
            obj = OfferTableInfo.model_validate(r)
            list_with_offers.append(obj)

        return list_with_offers

    def get_my_category_lots(self, game: str, game_category: str) -> list[LotFields]:
        """
        Получает свои лоты категории

        :param game: Название категории (slug)
        :param game_category: Категория в игре (slug)

        :return: Список с лотами
        """

        url = f"https://starvell.com/_next/data/{self.build_id}/{game}/{game_category}/trade.json?game={game}&game={game_category}&game=trade"
        response = self.request.get(url, raise_not_200=True).json()
        list_with_my_lots = []

        for r in response['pageProps']['offers']:
            obj = LotFields.model_validate(r)
            list_with_my_lots.append(obj)

        return list_with_my_lots

    def get_user(self, user_id: str | int) -> User:
        """
        Получает информацию об профиле пользователя

        :param user_id: ID Пользователя

        :return: Полная информация об пользователе
        """

        url = f"https://starvell.com/api/users/{user_id}"
        response = self.request.get(url=url, raise_not_200=True).json()

        return User.model_validate(response)

    def save_lot(self, lot: LotFields) -> None:
        """
        Сохраняет лот с переданными филдами

        :param lot: Поля лота (Класс LotFields)

        :return: None
        """

        url = f"https://starvell.com/api/offers-operations/{lot.id}/update"
        data = lot.model_dump(by_alias=True)

        if 'subCategory' in data:
            data.pop('subCategory')

        for key, value in data.items():
            if type(value) is datetime:
                data[key] = value.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        self.request.post(url, data, raise_not_200=False)

    def send_review(self, review_id: str, content: str) -> None:
        """
        Отправляет ответ на отзыв только в том случае, если на отзыв ещё нет ответа

        :param review_id: ID Отзыва, на который нужно ответить
        :param content: Текст ответа

        :return: None
        """

        url = "https://starvell.com/api/review-responses/create"
        body = {
            "content": content,
            "reviewId": review_id
        }
        response = self.request.post(url, body, raise_not_200=False).json()

        if not response['success']:
            raise SendReviewError(response['message'])

    def edit_review(self, review_id: str, content: str) -> None:
        """
        Редактирует ответ на отзыв

        Именно редактирует, если на отзыв ещё нет ответа, может возникнуть ошибка

        :param review_id: ID Отзыва, на который нужно изменить ответ
        :param content: Текст ответа

        :return: None
        """

        url = f"https://starvell.com/api/review-responses/{review_id}/update"
        body = {
            "content": content,
            "reviewId": review_id
        }
        response = self.request.post(url, body, raise_not_200=False).json()

        if not response['success']:
            raise EditReviewError(response['message'])

    def refund(self, order_id: str) -> None:
        """
        Оформляет возврат в заказе

        :param order_id: ID Заказа

        :return: None
        """

        url = "https://starvell.com/api/orders/refund"
        body = {
            "orderId": order_id
        }

        response = self.request.post(url, body, raise_not_200=False).json()

        if not response['success']:
            raise RefundError(response['message'])

    def withdraw(self, payment_system: PaymentTypes, requisite: str, amount: float, bank=None) -> None:
        """
        Создаёт заявку на вывод средств

        При ошибке вывода возбуждается WithdrawError

        :param payment_system: Тип платёжной системы для вывода
        :param requisite: Реквизиты для вывода (Номер карты / Номер СБП / Адрес крипты)
        :param amount: Сумма для вывода
        :param bank: Только если вывод с помощью СБП, тогда указывай там айди банка, иначе даже не трогай

        :return: None
        """

        url = "https://starvell.com/api/payouts/create"
        body = {
            "paymentSystemId": format_payment_methods(payment_system),
            "amount": amount * 100,
            "address": requisite,
            'cardHolder' if payment_system is not PaymentTypes.SBP else 'sbpBankId': "StarvellAPI" if payment_system is not PaymentTypes.SBP else bank
        }

        response = self.request.post(url, body, raise_not_200=False).json()

        if not response['success']:
            raise WithdrawError(response.get('message'))
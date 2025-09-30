from typing import Optional

from starvell.enums import (
    MessageTypes,
    OrderStatuses,
    PaymentTypes,
    TransactionDirections,
    TransactionStatuses,
    TransactionTypes,
)

NOTIFICATION_TYPES = (
    "ORDER_PAYMENT",
    "REVIEW_CREATED",
    "ORDER_COMPLETED",
    "ORDER_REFUND",
    "REVIEW_UPDATED",
    "REVIEW_DELETED",
    "ORDER_REOPENED",
    "REVIEW_RESPONSE_CREATED",
    "REVIEW_RESPONSE_UPDATED",
    "REVIEW_RESPONSE_DELETED",
    "BLACKLIST_YOU_ADDED",
    "BLACKLIST_USER_ADDED",
    "BLACKLIST_YOU_REMOVED",
    "BLACKLIST_USER_REMOVED",
)
NOTIFICATION_ORDER_TYPES = (
    "ORDER_PAYMENT",
    "REVIEW_CREATED",
    "ORDER_COMPLETED",
    "ORDER_REFUND",
    "REVIEW_UPDATED",
    "REVIEW_DELETED",
    "ORDER_REOPENED",
    "REVIEW_RESPONSE_CREATED",
    "REVIEW_RESPONSE_UPDATED",
    "REVIEW_RESPONSE_DELETED",
)


def format_directions(direction: str) -> TransactionDirections:
    """
    Форматирует направление транзакции со Starvell на TransactionDirections (Enum)

    :param direction:Направление транзакции, полученное с ответа Starvell
    :return: TransactionDirections (Enum)
    """

    directions = {
        "EXPENSE": TransactionDirections.EXPENSE,
        "INCOME": TransactionDirections.INCOME,
    }

    return directions.get(direction, TransactionDirections.UNKNOWN)


def format_types(order_type: str) -> TransactionTypes:
    """
    Форматирует тип транзакции со Starvell на TransactionTypes (Enum)

    :param order_type: Тип транзакции, полученный с ответа Starvell

    :return: TransactionTypes (Enum)
    """

    order_types = {
        "ORDER_FULFILLMENT": TransactionTypes.ORDER_FULFILLMENT,
        "ORDER_PAYMENT": TransactionTypes.ORDER_PAYMENT,
        "BALANCE_TOPUP": TransactionTypes.BALANCE_TOPUP,
        "ORDER_REFUND": TransactionTypes.ORDER_REFUND,
        "PAYOUT": TransactionTypes.PAYOUT,
        "OTHER": TransactionTypes.OTHER,
    }

    return order_types.get(order_type, TransactionTypes.UNKNOWN)


def format_statuses(status: str) -> TransactionStatuses:
    """
    Форматирует статус транзакции со Starvell на TransactionStatuses (Enum)

    :param status: Статус транзакции, полученный с ответа Starvell
    :return: TransactionStatuses (Enum)

    """

    order_statuses = {
        "COMPLETED": TransactionStatuses.COMPLETED,
        "CANCELLED": TransactionStatuses.CANCELLED,
    }

    return order_statuses.get(status, TransactionStatuses.UNKNOWN)


def format_order_status(status: str) -> OrderStatuses:
    """
    Форматирует строку со статусом заказа на OrderStatuses (Enum)

    :param status: Статус заказа, полученный с ответа Starvell

    :return: OrderStatuses (Enum)
    """

    order_statuses = {
        "COMPLETED": OrderStatuses.CLOSED,
        "REFUND": OrderStatuses.REFUNDED,
        "CREATED": OrderStatuses.PAID,
    }

    return order_statuses.get(status, OrderStatuses.UNKNOWN)


def format_message_types(msg_type: str) -> MessageTypes:
    """
    Форматирует строку с notification_type на MessageTypes (Enum)

    :param msg_type: notification_type строка с ответа от Starvell

    :return: MessageTypes (Enum)
    """

    msg_types = {
        "ORDER_PAYMENT": MessageTypes.NEW_ORDER,
        "REVIEW_CREATED": MessageTypes.NEW_REVIEW,
        "ORDER_COMPLETED": MessageTypes.CONFIRM_ORDER,
        "ORDER_REFUND": MessageTypes.ORDER_REFUND,
        "ORDER_REOPENED": MessageTypes.ORDER_REOPENED,
        "REVIEW_UPDATED": MessageTypes.REVIEW_CHANGED,
        "REVIEW_DELETED": MessageTypes.REVIEW_DELETED,
        "REVIEW_RESPONSE_CREATED": MessageTypes.REVIEW_RESPONSE_CREATED,
        "REVIEW_RESPONSE_UPDATED": MessageTypes.REVIEW_RESPONSE_EDITED,
        "REVIEW_RESPONSE_DELETED": MessageTypes.REVIEW_RESPONSE_DELETED,
        "BLACKLIST_YOU_ADDED": MessageTypes.BLACKLIST_YOU_ADDED,
        "BLACKLIST_USER_ADDED": MessageTypes.BLACKLIST_USER_ADDED,
        "BLACKLIST_YOU_REMOVED": MessageTypes.BLACKLIST_YOU_REMOVED,
        "BLACKLIST_USER_REMOVED": MessageTypes.BLACKLIST_USER_REMOVED,
    }

    return msg_types.get(msg_type, MessageTypes.OTHER)


def format_payment_methods(method: PaymentTypes) -> Optional[int]:
    """
    Форматирует способы вывода Starvell (Enum), на ID со Starvell

    :param method: PaymentTypes

    :return: ID На Starvell
    """

    p_types = {
        PaymentTypes.BANK_CARD_RU: 13,
        PaymentTypes.SBP: 15,
        PaymentTypes.USDT_TRC20: 11,
        PaymentTypes.LTC: 12,
    }

    return p_types.get(method)

from StarvellAPI.common.enums import (
    TransactionDirections,
    TransactionTypes,
    TransactionStatuses,
    OrderStatuses,
    MessageTypes,
    PaymentTypes)

def format_directions(direction: str) -> TransactionDirections:
    directions = {
        "EXPENSE": TransactionDirections.EXPENSE,
        "INCOME": TransactionDirections.INCOME
    }

    return directions.get(direction, TransactionDirections.UNKNOWN)

def format_types(order_type: str) -> TransactionTypes:
    order_types = {
        "ORDER_FULFILLMENT": TransactionTypes.ORDER_FULFILLMENT,
        "ORDER_PAYMENT": TransactionTypes.ORDER_PAYMENT,
        "BALANCE_TOPUP": TransactionTypes.BALANCE_TOPUP,
        "ORDER_REFUND": TransactionTypes.ORDER_REFUND,
        "PAYOUT": TransactionTypes.PAYOUT,
        "OTHER": TransactionTypes.OTHER
    }

    return order_types.get(order_type, TransactionTypes.UNKNOWN)

def format_statuses(status: str) -> TransactionStatuses:
    order_statuses = {
        "COMPLETED": TransactionStatuses.COMPLETED,
        "CANCELLED": TransactionStatuses.CANCELLED
    }

    return order_statuses.get(status, TransactionStatuses.UNKNOWN)

def format_order_status(status: str) -> OrderStatuses:
    order_statuses = {
        "COMPLETED": OrderStatuses.CLOSED,
        "REFUND": OrderStatuses.REFUNDED,
        "CREATED": OrderStatuses.PAID
    }

    return order_statuses.get(status, OrderStatuses.UNKNOWN)

def format_message_types(msg_type: str) -> MessageTypes:
    msg_types = {
        "ORDER_PAYMENT": MessageTypes.NEW_ORDER,
        "REVIEW_CREATED": MessageTypes.NEW_REVIEW,
        "ORDER_COMPLETED": MessageTypes.CONFIRM_ORDER,
        "ORDER_REFUND": MessageTypes.ORDER_REFUND,
        "REVIEW_UPDATED": MessageTypes.REVIEW_CHANGED,
        "REVIEW_DELETED": MessageTypes.REVIEW_DELETED
    }

    return msg_types.get(msg_type, MessageTypes.UNKNOWN)

def format_payment_methods(method: PaymentTypes) -> int:
    p_types = {
        PaymentTypes.BANK_CARD_RU: 13,
        PaymentTypes.SBP: 15,
        PaymentTypes.USDT_TRC20: 11,
        PaymentTypes.LTC: 12
    }

    return p_types.get(method)
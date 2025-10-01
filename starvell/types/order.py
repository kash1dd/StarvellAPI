from pydantic import BaseModel, Field
from starvell.enums import OrderStatuses
from starvell.types import User
from datetime import datetime


class SubCategory(BaseModel):
    name: str
    """Название"""


class Game(SubCategory):
    id: int
    """ID"""
    slug: str
    """Слаг"""


class Category(Game): ...


class TimeRange(BaseModel):
    unit: str
    """Тип времени"""
    value: int | float
    """Значение (например 10)"""


class DeliveryTime(BaseModel):
    from_: TimeRange = Field(alias="from")
    """От"""
    to: TimeRange
    """До"""


class Description(BaseModel):
    full_description: str | None = Field(None, alias="description")
    """Полное описание заказа"""
    short_description: str | None = Field(None, alias="briefDescription")
    """Короткое описание заказа (Заголовок лота)"""


class Descriptions(BaseModel):
    ru: Description | None = Field(None, alias="rus")
    """Описания на русском"""
    en: Description | None = Field(None, alias="eng")
    """Описания на английском"""


class AttributeValue(BaseModel):
    id: str
    """ID Значения атрибута"""
    name_ru: str | None = Field(alias="nameRu")
    """Название значения атрибута на русском"""
    name_en: str | None = Field(alias="nameEn")
    """Название значения атрибута на английском"""


class OfferAttributes(BaseModel):
    id: str
    """ID атрибута"""
    value: AttributeValue
    """Значение атрибута"""
    name_ru: str | None = Field(alias="nameRu")
    """Название атрибута на русском"""
    name_en: str | None = Field(alias="nameEn")
    """Название атрибута на английском"""


class OfferDetails(BaseModel):
    game: Game
    """Игра (Основная категория)"""
    category: Category
    """Категория игры"""
    attributes: list[OfferAttributes] | None
    """Атрибуты лота"""
    subcategory: SubCategory | None = Field(alias="subCategory")
    """Подкатегория категории"""
    delivery_time: DeliveryTime | None = Field(alias="deliveryTime")
    """Время доставки"""
    descriptions: Descriptions
    """Описания лота"""
    images: list
    """Изображения лота"""
    availability: int | float
    """Количество доступного товара"""
    auto_delivery: bool = Field(alias="instantDelivery")
    """Авто-выдача от старвелла?"""


class OrderArgs(BaseModel):
    id: str
    """ID Аргумента"""
    value: str | None
    """Значение аргумента"""
    name_ru: str = Field(alias="nameRu")
    """Название аргуминета на русском"""
    name_en: str = Field(alias="nameEn")
    """Название аргумента на английском"""


class OrderShortCut(BaseModel):
    id: str
    """ID Заказа"""
    status: OrderStatuses
    """Статус заказа"""
    price_for_me: float = Field(alias="basePrice")
    """Прайс для меня (Без комиссии покупателя)"""
    price_for_buyer: float = Field(alias="totalPrice")
    """Прайс для покупателя (С комиссией покупателя)"""
    quantity: int
    """Количество купленного товара"""
    offer_details: OfferDetails = Field(alias="offerDetails")
    """Купленный лот"""
    order_args: list[OrderArgs] | None = Field(alias="orderArgs")
    """Аргументы к заказу (какие-то параметры, которые покупатель указал при оплате)"""
    review_visible_after_refund: bool = Field(alias="reviewVisibleAfterRefund")
    """Виден-ли отзыв после возврата?"""
    created_at: datetime = Field(alias="createdAt")
    """Дата создания"""
    updated_at: datetime = Field(alias="updatedAt")
    """Дата последнего изменения статуса заказа"""


class Order(OrderShortCut):
    offer_id: int | None = Field(alias="offerId")
    """ID Оплаченного лота"""

class OrderFull(Order):
    user: User
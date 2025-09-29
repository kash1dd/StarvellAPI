from pydantic import BaseModel, Field
from datetime import datetime

from starvellapi.enums import OrderStatuses


class BaseConfig(BaseModel):
    class Config:
        validate_by_name = True


class Game(BaseConfig):
    id: int
    name: str
    slug: str


class GameCategory(Game): ...


class SubCategory(BaseConfig):
    name: str


class TimeRange(BaseConfig):
    unit: str
    value: int


class DeliveryTime(BaseConfig):
    from_: TimeRange = Field(alias="from")
    to: TimeRange


class Description(BaseConfig):
    description: str
    lot_title: str | None = Field(None, alias="briefDescription")


class Descriptions(BaseConfig):
    rus: Description


class OfferDetails(BaseConfig):
    full_lot_title: str
    game: Game
    game_category: GameCategory = Field(alias="category")
    images: list[str]
    sub_category: SubCategory | None = Field(None, alias="subCategory")
    availability: int
    delivery_time: DeliveryTime | None = Field(None, alias="deliveryTime")
    descriptions: Descriptions
    is_auto_delivery: bool = Field(alias="instantDelivery")


class Order(BaseConfig):
    id: str
    status: OrderStatuses
    price_for_me: float = Field(alias="basePrice")
    price_for_buyer: float = Field(alias="totalPrice")
    buyer_id: int = Field(alias="buyerId")
    offer_id: int | None = Field(alias="offerId")
    offer: OfferDetails = Field(alias="offerDetails")
    order_args: list[str] = Field(alias="orderArgs")
    quantity: int
    review_visible_after_refund: bool = Field(alias="reviewVisibleAfterRefund")
    created_at: datetime = Field(alias="createdAt")
    refunded_at: datetime | None = Field(alias="refundedAt")
    completed_at: datetime | None = Field(alias="completedAt")

from pydantic import BaseModel, Field
from datetime import datetime

from .order import SubCategory, DeliveryTime, Descriptions, Game
from StarvellAPI.enums import OrderStatuses

class BaseConfig(BaseModel):
    class Config:
        validate_by_name = True

class Category(BaseConfig):
    id: int
    name: str
    slug: str

class OfferDetailsPreview(BaseConfig):
    game: Game
    images: list[str]
    category: Category
    attributes: list[str]
    sub_category: SubCategory = Field(alias="subCategory")
    availability: int
    delivery_time: DeliveryTime = Field(alias="deliveryTime")
    descriptions: Descriptions
    is_auto_delivery: bool = Field(alias="instantDelivery")

class UserPreviewOrder(BaseConfig):
    id: int
    username: str
    avatar: str | None
    banner: str | None
    description: str | None
    is_online: bool = Field(alias="isOnline")
    is_banned: bool = Field(alias="isBanned")
    roles: list[str]
    rating: int
    reviews_count: int = Field(alias="reviewsCount")
    last_online_at: datetime = Field(alias="lastOnlineAt")
    created_at: datetime = Field(alias="createdAt")

class OrderInfo(BaseConfig):
    id: str
    status: OrderStatuses
    base_price: int = Field(alias="basePrice")
    total_price: int = Field(alias="totalPrice")
    offer_id: int | None = Field(alias="offerId")
    offer_details: OfferDetailsPreview = Field(alias="offerDetails")
    order_args: list[str] = Field(alias="orderArgs")
    review_visible_after_refund: bool = Field(alias="reviewVisibleAfterRefund")
    completed_at: datetime | None = Field(alias="completedAt")
    refunded_at: datetime | None = Field(alias="refundedAt")
    created_at: datetime | None = Field(alias="createdAt")
    updated_at: datetime | None = Field(alias="updatedAt")
    buyer: UserPreviewOrder = Field(alias="user")
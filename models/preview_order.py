from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

from StarvellAPI.models.order import SubCategory, DeliveryTime, Descriptions
from StarvellAPI.common.enums import OrderStatuses

class BaseConfig(BaseModel):
    class Config:
        validate_by_name = True

class Game(BaseConfig):
    id: int
    name: str
    slug: str

class Category(BaseConfig):
    id: int
    name: str
    slug: str

class OfferDetails(BaseConfig):
    game: Game
    images: list[str]
    category: Category
    attributes: list[str]
    sub_category: SubCategory = Field(alias="subCategory")
    availability: int
    delivery_time: DeliveryTime = Field(alias="deliveryTime")
    descriptions: Descriptions
    is_auto_delivery: bool = Field(alias="instantDelivery")

class User(BaseConfig):
    id: int
    username: str
    avatar: Optional[str]
    banner: Optional[str]
    description: Optional[str]
    is_online: bool = Field(alias="isOnline")
    is_instant_payout_enabled: bool = Field(alias="isInstantPayoutEnabled")
    is_payout_enabled: bool = Field(alias="isPayoutEnabled")
    is_kyc_verified: bool = Field(alias="isKycVerified")
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
    buyer_id: int = Field(alias="buyerId")
    offer_id: Optional[int] = Field(alias="offerId")
    offer_details: OfferDetails = Field(alias="offerDetails")
    order_args: list[str] = Field(alias="orderArgs")
    review_visible_after_refund: bool = Field(alias="reviewVisibleAfterRefund")
    completed_at: Optional[datetime] = Field(alias="completedAt")
    refunded_at: Optional[datetime] = Field(alias="refundedAt")
    created_at: Optional[datetime] = Field(alias="createdAt")
    updated_at: Optional[datetime] = Field(alias="updatedAt")
    user: User
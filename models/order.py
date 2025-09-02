from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class BaseConfig(BaseModel):
    class Config:
        validate_by_name = True

class Game(BaseConfig):
    game_id: int = Field(alias="id")
    name: str
    slug: str

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
    lot_title: Optional[str] = Field(None, alias="briefDescription")

class Descriptions(BaseConfig):
    rus: Description

class OfferDetails(BaseConfig):
    game: Game
    images: list[str]
    sub_category: SubCategory = Field(None, alias="subCategory")
    availability: int
    delivery_time: DeliveryTime = Field(None, alias="deliveryTime")
    descriptions: Descriptions
    is_auto_delivery: bool = Field(alias="instantDelivery")

class UserInfo(BaseConfig):
    id: int
    username: str
    created_at: datetime = Field(alias="createdAt")
    avatar_id: Optional[str] = Field(alias="avatar")

class UserInfoExtendedLow(UserInfo):
    rating: float
    reviews_count: int = Field(alias="reviewsCount")

class Chat(BaseConfig):
    chat_id: str = Field(alias="id")
    participants: list[UserInfo]
    is_black_listed: bool = Field(alias="isBlacklisted")
    is_me_black_listed: bool = Field(alias="isMeBlacklisted")

class Order(BaseConfig):
    order_id: str = Field(alias="id")
    price_wo_comission: int = Field(alias="basePrice")
    price_w_comission: int = Field(alias="totalPrice")
    lot_id: int = Field(alias="offerId")
    offer_details: OfferDetails = Field(alias="offerDetails")
    quantity: int
    created_at: datetime = Field(alias="createdAt")
    buyer: UserInfoExtendedLow

class ReviewResponse(BaseConfig):
    response_id: str = Field(alias="id")
    text: str = Field(alias="content")

class Review(BaseConfig):
    review_id: str = Field(alias="id")
    text: str = Field(alias="content")
    rating: int
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    is_hidden: bool = Field(alias="isHidden")
    review_response: Optional[ReviewResponse] = Field(alias="reviewResponse")

class OrderFullInfo(BaseConfig):
    order: Order
    chat: Chat
    review: Optional[Review]
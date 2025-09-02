from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

from StarvellAPI.models.preview_order import OfferDetails

class BaseConfig(BaseModel):
    class Config:
        validate_by_name = True

class ReviewAuthor(BaseConfig):
    user_id: int = Field(alias='id')
    username: str
    avatar_id: Optional[str] = Field(alias='avatar')

class ReviewShortcutOrder(BaseConfig):
    offer_details: OfferDetails = Field(alias="offerDetails")
    amount: int

class ReviewResponse(BaseConfig):
    response_id: str = Field(alias="id")
    text: str = Field(alias="content")

class ReviewInfo(BaseConfig):
    review_id: str = Field(alias="id")
    text: str = Field(alias="content")
    rating: int
    buyer_id: int = Field(alias="authorId")
    order_id: str = Field(alias="orderId")
    is_hidden: bool = Field(alias="isHidden")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    author: ReviewAuthor
    order: ReviewShortcutOrder
    review_response: Optional[ReviewResponse] = Field(alias="reviewResponse")
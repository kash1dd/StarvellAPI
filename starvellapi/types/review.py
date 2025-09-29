from pydantic import BaseModel, Field
from datetime import datetime


class BaseConfig(BaseModel):
    class Config:
        validate_by_name = True


class ReviewAuthor(BaseConfig):
    id: int
    username: str
    avatar_id: str | None = Field(alias="avatar")


class ReviewShortcutOrder(BaseConfig):
    amount: int


class ReviewResponse(BaseConfig):
    id: str
    text: str = Field(alias="content")


class ReviewInfo(BaseConfig):
    id: str
    content: str
    rating: int
    buyer_id: int = Field(alias="authorId")
    order_id: str = Field(alias="orderId")
    is_hidden: bool = Field(alias="isHidden")
    created_at: datetime = Field(alias="createdAt")
    author: ReviewAuthor
    order: ReviewShortcutOrder
    review_response: ReviewResponse | None = Field(alias="reviewResponse")

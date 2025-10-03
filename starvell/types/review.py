from pydantic import BaseModel, Field
from datetime import datetime

from starvell.types import MessageAuthor


class Response(BaseModel):
    id: str
    content: str


class Review(BaseModel):
    id: str
    content: str
    rating: int
    author_id: int = Field(alias="authorId")
    order_id: str = Field(alias="orderId")
    is_hidden: bool = Field(alias="isHidden")
    created_at: datetime
    updated_at: datetime
    author: MessageAuthor
    response: Response | None = Field(None, alias="reviewResponse")

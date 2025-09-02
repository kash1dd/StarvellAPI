from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

from StarvellAPI.common.enums import MessageTypes
from StarvellAPI.models.order import OfferDetails

class BaseConfig(BaseModel):
    class Config:
        validate_by_name = True

class Author(BaseConfig):
    id: int
    username: str

class MiniOrder(BaseConfig):
    id: str
    quantity: int
    offer_details: OfferDetails = Field(alias="offerDetails")

class MetaData(BaseConfig):
    is_auto_response: bool = Field(None, alias="isAutoResponse")
    notification_type: str = Field(None, alias="notificationType")

class Message(BaseConfig):
    id: str
    text: str = Field(alias="content")
    metadata: Optional[MetaData]
    chat_id: str = Field(alias="chatId")
    created_at: datetime = Field(alias="createdAt")
    author: Optional[Author] = None
    buyer: Optional[dict]
    seller: Optional[dict]
    admin: Optional[dict]
    order: Optional[MiniOrder]
    event_type: MessageTypes
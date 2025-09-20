from pydantic import BaseModel, Field
from datetime import datetime

from StarvellAPI.enums.enums import MessageTypes
from .order import OfferDetails

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
    is_auto_response: bool | None = Field(None, alias="isAutoResponse")
    notification_type: str | None = Field(None, alias="notificationType")

class Message(BaseConfig):
    id: str
    text: str = Field(alias="content")
    metadata: MetaData | None
    chat_id: str = Field(alias="chatId")
    created_at: datetime = Field(alias="createdAt")
    author: Author | None = None
    buyer: dict | None
    seller: dict | None
    admin: dict | None
    order: MiniOrder | None
    event_type: MessageTypes
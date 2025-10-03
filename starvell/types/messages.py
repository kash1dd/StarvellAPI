from pydantic import BaseModel, Field, field_validator
from datetime import datetime

from starvell.enums import MessageType
from .order import OrderShortCut
from .user import MessageAuthor
from starvell.utils import format_message_types


class BaseMessage(BaseModel):
    metadata: MessageType
    id: str
    chat_id: str = Field(alias="chatId")
    created_at: datetime = Field(alias="createdAt")
    user: MessageAuthor

    @field_validator("metadata", mode="before")
    @classmethod
    def identify_msg(cls, field: dict[str, str | bool] | None):
        if not field:
            return MessageType.NEW_MESSAGE

        data = field.get("notificationType") or field.get("isAutoResponse")
        return format_message_types(data)


class Message(BaseMessage):
    content: str
    images: list[str]


class NewMessageEvent(Message): ...


class OrderEvent(BaseMessage):
    order: OrderShortCut

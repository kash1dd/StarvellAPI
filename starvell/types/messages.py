from pydantic import BaseModel, Field, AliasChoices, field_validator
from datetime import datetime

from starvell.enums import MessageType
from starvell.types import MessageAuthor
from starvell.utils import format_message_types


class BaseMessage(BaseModel):
    type: MessageType = Field(alias="metadata")
    id: str
    chat_id: str = Field(alias="chatId")
    created_at: datetime = Field(alias="createdAt")
    user: MessageAuthor = Field(
        validation_alias=AliasChoices("author", "buyer", "seller", "admin")
    )

    @field_validator("type", mode="before")
    @classmethod
    def identify_msg(cls, field: dict[str, str | bool] | None):
        if not field:
            return MessageType.NEW_MESSAGE

        data = field.get("notificationType") or field.get("isAutoResponse")
        return format_message_types(data)


class NewMessageEvent(BaseMessage):
    content: str
    images: list[str]

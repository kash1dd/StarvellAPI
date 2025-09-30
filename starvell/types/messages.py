from pydantic import BaseModel, Field, AliasChoices
from datetime import datetime

from starvell.enums import MessageTypes
from starvell.types import MessageAuthor


class BaseMessage(BaseModel):
    type: MessageTypes
    id: str
    chat_id: str = Field(alias="chatId")
    created_at: datetime = Field(alias="createdAt")
    user: MessageAuthor = Field(
        validation_alias=AliasChoices("author", "buyer", "seller", "admin")
    )


class NewMessageEvent(BaseMessage):
    content: str
    images: list[str]

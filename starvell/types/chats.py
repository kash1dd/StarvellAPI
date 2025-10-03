from pydantic import BaseModel, Field

from starvell.types import Message, UserShortCut


class ChatShortCut(BaseModel):
    id: str
    participants: list[UserShortCut]
    last_message: Message = Field(alias="lastMessage")
    unread_message_count: int = Field(alias="unreadMessageCount")

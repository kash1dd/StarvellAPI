from pydantic import BaseModel, Field
from datetime import datetime


class BaseConfig(BaseModel):
    class Config:
        validate_by_name = True


class UserChatInfo(BaseConfig):
    id: int
    username: str
    avatar_id: str | None = Field(alias="avatar")
    is_online: bool = Field(alias="isOnline")
    is_operator: bool = Field(alias="isOperator")
    last_online_at: datetime = Field(alias="lastOnlineAt")


class MessagePreview(BaseConfig):
    id: str
    text: str = Field(alias="content")
    created_at: datetime = Field(alias="createdAt")
    type: str
    metadata: dict | None
    buyer: dict | None
    seller: dict | None
    admin: dict | None
    order: dict | None
    images: list | None


class ChatInfo(BaseConfig):
    id: str
    users_info: list[UserChatInfo] = Field(alias="participants")
    last_message: MessagePreview = Field(alias="lastMessage")
    unread_message_count: int = Field(alias="unreadMessageCount")

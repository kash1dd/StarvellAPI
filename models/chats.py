from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class BaseConfig(BaseModel):
    class Config:
        validate_by_name = True

class User(BaseConfig):
    id: int
    username: str
    avatar_id: Optional[str] = Field(alias="avatar")
    is_online: bool = Field(alias="isOnline")
    is_operator: bool = Field(alias="isOperator")
    last_online_at: datetime = Field(alias="lastOnlineAt")

class Message(BaseConfig):
    id: str
    text: str = Field(alias="content")
    created_at: datetime = Field(alias="createdAt")
    type: str
    metadata: Optional[dict]
    buyer: Optional[dict]
    seller: Optional[dict]
    admin: Optional[dict]
    order: Optional[dict]
    images: Optional[list]

class ChatInfo(BaseConfig):
    id: str
    users_info: list[User] = Field(alias="participants")
    last_message: Message = Field(alias="lastMessage")
    unread_message_count: int = Field(alias="unreadMessageCount")
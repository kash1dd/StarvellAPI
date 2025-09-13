from pydantic import BaseModel, Field
from typing import Optional

from .chat import MetaData, Author
from StarvellAPI.common.enums import MessageTypes

class BaseConfig(BaseModel):
    class Config:
        validate_by_name = True

class NewMessageEvent(BaseModel):
    id: str
    content: Optional[str]
    metadata: Optional[MetaData]
    images: list[str]
    chat_id: str = Field(alias="chatId")
    author: Optional[Author]
    type: MessageTypes
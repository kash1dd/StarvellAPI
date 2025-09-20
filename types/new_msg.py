from pydantic import BaseModel, Field

from StarvellAPI.enums import MessageTypes
from .chat import MetaData, Author

class BaseConfig(BaseModel):
    class Config:
        validate_by_name = True

class NewMessageEvent(BaseModel):
    id: str
    content: str | None
    metadata: MetaData | None
    images: list[str]
    chat_id: str = Field(alias="chatId")
    author: Author
    type: MessageTypes
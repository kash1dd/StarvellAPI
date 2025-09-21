from pydantic import BaseModel, Field

from StarvellAPI.enums import MessageTypes
from .chat import MetaData, Author

class BaseConfig(BaseModel):
    class Config:
        validate_by_name = True

class Images(BaseConfig):
    id: str
    width: int | float | str
    height: int | float | str
    extension: str

class NewMessageEvent(BaseConfig):
    id: str
    content: str | None
    metadata: MetaData | None
    images: list[Images]
    chat_id: str = Field(alias="chatId")
    author: Author
    type: MessageTypes
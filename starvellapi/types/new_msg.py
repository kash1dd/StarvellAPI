from pydantic import BaseModel, Field

from starvellapi.enums import MessageTypes
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
    by_api: bool | None = None
    by_admin: bool
    is_auto_response: bool
    id: str
    content: str | None
    metadata: MetaData | None
    images: list[Images]
    chat_id: str = Field(alias="chatId")
    author: Author
    type: MessageTypes

class ServiceMessageEvent(BaseConfig):
    id: str
    type: MessageTypes
    chat_id: str | None = None
from pydantic import BaseModel, Field

from StarvellAPI.models.chat import Author, MiniOrder

class BaseConfig(BaseModel):
    class Config:
        validate_by_name = True

class OrderEvent(BaseModel):
    chat_id: str = Field(alias="chatId")
    buyer: Author
    order: MiniOrder
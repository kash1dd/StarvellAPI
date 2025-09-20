from pydantic import BaseModel, Field
from datetime import datetime

class BaseConfig(BaseModel):
    class Config:
        validate_by_name = True

class BlockListedUser(BaseModel):
    id: int
    username: str
    avatar: str | None
    black_listed_at: datetime = Field(alias="blacklistedAt")
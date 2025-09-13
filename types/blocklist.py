from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class BaseConfig(BaseModel):
    class Config:
        validate_by_name = True

class BlockListedUser(BaseModel):
    id: int
    username: str
    avatar: Optional[str]
    black_listed_at: datetime = Field(alias="blacklistedAt")
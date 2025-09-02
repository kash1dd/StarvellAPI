from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class BaseConfig(BaseModel):
    class Config:
        validate_by_name = True

class User(BaseConfig):
    user_id: int = Field(alias="id")
    username: str
    last_online_at: Optional[datetime] = Field(alias="lastOnlineAt")
    created_at: Optional[datetime] = Field(alias="createdAt")
    avatar: Optional[str]
    banner: Optional[str]
    description: Optional[str]
    is_kyc_verified: bool = Field(alias="isKycVerified")
    is_banned: bool = Field(alias="isBanned")
    roles: list[str]
    rating: float
    reviews_count: int = Field(alias="reviewsCount")
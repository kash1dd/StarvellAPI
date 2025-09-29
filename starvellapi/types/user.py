from pydantic import BaseModel, Field
from datetime import datetime


class BaseConfig(BaseModel):
    class Config:
        validate_by_name = True


class UserInfo(BaseConfig):
    id: int
    username: str
    created_at: datetime = Field(alias="createdAt")
    avatar_id: str | None = Field(alias="avatar")


class UserInfoExtendedLow(UserInfo):
    rating: float
    reviews_count: int = Field(alias="reviewsCount")


class User(UserInfoExtendedLow):
    last_online_at: datetime | None = Field(alias="lastOnlineAt")
    banner: str | None
    description: str | None
    is_kyc_verified: bool = Field(alias="isKycVerified")
    is_banned: bool = Field(alias="isBanned")
    roles: list[str]

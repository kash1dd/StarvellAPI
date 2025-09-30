from pydantic import BaseModel, Field
from datetime import datetime


class MessageAuthor(BaseModel):
    id: int
    username: str


class User(MessageAuthor):
    is_online: bool = Field(alias="isOnline")
    last_online_at: datetime = Field(alias="lastOnlineAt")
    created_at: datetime = Field(alias="createdAt")
    avatar_id: str | None = Field(alias="avatar")
    banner_id: str | None = Field(alias="banner")
    description: str | None
    is_verified: bool = Field(alias="isKycVerified")
    is_banned: bool = Field(alias="isBanned")
    roles: list[str]
    rating: int | float
    reviews: int = Field(alias="reviewsCount")

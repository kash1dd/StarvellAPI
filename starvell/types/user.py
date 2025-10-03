from pydantic import BaseModel, Field
from datetime import datetime


class MessageAuthor(BaseModel):
    id: int
    username: str


class BlockListedUser(MessageAuthor):
    avatar_id: str | None = Field(alias="avatar")
    block_listed_at: datetime = Field(alias="blacklistedAt")


class UserShortCut(MessageAuthor):
    avatar_id: str | None = Field(alias="avatar")
    is_online: bool = Field(alias="isOnline")
    is_banned: bool = Field(alias="isBanned")
    last_online_at: datetime = Field(alias="lastOnlineAt")
    created_at: datetime = Field(alias="createdAt")


class User(UserShortCut):
    banner_id: str | None = Field(alias="banner")
    description: str | None
    is_verified: bool = Field(alias="isKycVerified")
    roles: list[str]
    rating: int | float
    reviews: int = Field(alias="reviewsCount")
    email: str | None = Field(None)


class Balance(BaseModel):
    rub: int = Field(alias="rubBalance")


class ActiveOrders(BaseModel):
    purchases: int = Field(alias="purchaseOrdersCount")
    sales: int = Field(alias="salesOrdersCount")


class Profile(BaseModel):
    user: User
    balance: Balance
    balance_hold: int | None = None
    orders: ActiveOrders | None = None
    unreadChatIds: list[str]

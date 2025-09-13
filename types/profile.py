from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class BaseConfig(BaseModel):
    class Config:
        validate_by_name = True

class MyProfileUser(BaseModel):
    id: int
    username: str
    email: str
    is_online: bool = Field(alias="isOnline")
    last_online_at: datetime = Field(alias="lastOnlineAt")
    created_at: datetime = Field(alias="createdAt")
    is_kyc_verified: bool = Field(alias="isKycVerified")
    is_banned: bool = Field(alias="isBanned")
    avatar: Optional[str]
    banner: Optional[str]
    description: Optional[str]
    roles: list[str]
    rating: int | float
    reviews_count: int = Field(alias="reviewsCount")
    is_phone_linked: bool = Field(alias="isPhoneLinked")
    has_password: bool = Field(alias="hasPassword")

class Balance(BaseModel):
    rub_balance: Optional[int] = Field(None, alias="rubBalance")
    usd_balance: Optional[int] = Field(None, alias="usdBalance")
    eur_balance: Optional[int] = Field(None, alias="eurBalance")

class OrdersCount(BaseModel):
    purchases: int = Field(alias="purchaseOrdersCount")
    sales: int = Field(alias="salesOrdersCount")

class MyProfile(BaseModel):
    user: MyProfileUser
    is_imitated: bool = Field(alias="isImitated")
    is_offers_hide: None = Field(alias="offersHide")
    offers_in_hide: list[str | int] = Field(alias="offersHides")
    balance: Balance
    holded_balance: int = Field(alias="holdedAmount")
    active_orders: OrdersCount = Field(alias="orderCountsByType")
    has_at_least_one_completed_order: bool = Field(alias="hasAtLeastOneCompletedOrder")
    unread_chat_ids: list[Optional[str]] = Field(alias="unreadChatIds")
from pydantic import BaseModel, Field
from typing import Any
from datetime import datetime

from starvell.types.order import (
    Descriptions,
    DeliveryTime,
    SubCategory,
)


class OfferFields(BaseModel):
    id: int
    type: str
    price: str
    price_type: str = Field(alias="priceType")
    availability: int
    descriptions: Descriptions
    delivery_time: DeliveryTime | None = Field(None, alias="deliveryTime")
    attributes: list[Any]
    message_after_pay: str | None = Field(None, alias="postPaymentMessage")
    lot_profile_position: int | None = Field(alias="profilePosition")
    is_auto_delivery: bool = Field(alias="instantDelivery")
    goods: list[Any] | None = None
    is_active: bool = Field(alias="isActive")
    is_hidden: bool = Field(alias="isHidden")
    is_profile_visible_only: bool = Field(alias="isProfileVisibleOnly")
    user_id: int = Field(alias="userId")
    game_id: int = Field(alias="gameId")
    category_id: int = Field(alias="categoryId")
    sub_category_id: int | None = Field(None, alias="subCategoryId")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    basic_attributes: list = Field([], alias="basicAttributes")
    numeric_attributes: list[Any] = Field([], alias="numericAttributes")
    sub_category: SubCategory | None = Field(None, alias="subCategory")


class CreatedOfferFields(BaseModel):
    attributes: list[Any] | None = None
    availability: int
    basicAttributes: list[Any] | None = None
    categoryId: int
    deliveryTime: DeliveryTime | None = None
    descriptions: Descriptions
    goods: list
    isActive: bool
    numericAttributes: list[Any]
    postPaymentMessage: str | None = None
    price: str
    subCategoryId: int
    type: str

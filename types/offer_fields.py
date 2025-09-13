from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

from .order import Descriptions, DeliveryTime, SubCategory

class BaseConfig(BaseModel):
    class Config:
        validate_by_name = True

class Attributes(BaseModel):
    id: str
    numericValue: int

class LotFields(BaseConfig):
    id: int
    type: str
    price: str
    price_type: str = Field(alias="priceType")
    availability: int
    descriptions: Descriptions
    delivery_time: Optional[DeliveryTime] = Field(None, alias="deliveryTime")
    attributes: List[Attributes]
    message_after_pay: Optional[str] = Field(None, alias="postPaymentMessage")
    lot_profile_position: Optional[int] = Field(alias="profilePosition")
    is_auto_delivery: bool = Field(alias="instantDelivery")
    goods: list = None
    is_active: bool = Field(alias="isActive")
    is_hidden: bool = Field(alias="isHidden")
    is_profile_visible_only: bool = Field(alias="isProfileVisibleOnly")
    user_id: int = Field(alias="userId")
    game_id: int = Field(alias="gameId")
    category_id: int = Field(alias="categoryId")
    sub_category_id: int = Field(None, alias="subCategoryId")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    basic_attributes: list = Field([], alias="basicAttributes")
    numeric_attributes: list[Attributes] = Field([], alias="numericAttributes")
    sub_category: Optional[SubCategory] = Field(None, alias="subCategory")
from pydantic import BaseModel, Field
from typing import Optional

from StarvellAPI.models.order import Descriptions, UserInfoExtendedLow, SubCategory

class BaseConfig(BaseModel):
    class Config:
        validate_by_name = True

class OfferTableInfo(BaseConfig):
    lot_id: int = Field(alias="id")
    price: str
    descriptions: Descriptions
    availability: int
    is_auto_delivery: bool = Field(alias="instantDelivery")
    user: UserInfoExtendedLow
    sub_category: Optional[SubCategory] = Field(alias="subCategory")
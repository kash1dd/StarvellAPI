from pydantic import BaseModel, Field

from .order import Descriptions, SubCategory
from .user import UserInfoExtendedLow

class BaseConfig(BaseModel):
    class Config:
        validate_by_name = True

class OfferTableInfo(BaseConfig):
    id: int
    price: str
    descriptions: Descriptions
    availability: int
    is_auto_delivery: bool = Field(alias="instantDelivery")
    user: UserInfoExtendedLow
    sub_category: SubCategory | None = Field(alias="subCategory")
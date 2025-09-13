from typing import Optional
from pydantic import BaseModel, Field

from StarvellAPI.models.order import SubCategory, Descriptions

class BaseConfig(BaseModel):
    class Config:
        validate_by_name = True

class OfferInfoShortCut(BaseConfig):
    id: int
    price: float
    attributes: Optional[list[str]]
    sub_category: SubCategory = Field(alias="subCategory")
    quantity: int = Field(alias="availability")
    descriptions: Descriptions
    is_auto_delivery: bool = Field(alias="instantDelivery")
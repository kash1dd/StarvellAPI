from pydantic import BaseModel
from typing import List, Optional

from .offer_fields import Attributes, DeliveryTime, Descriptions

class BaseConfig(BaseModel):
    class Config:
        validate_by_name = True

class CreateLotFields(BaseModel):
    attributes: Optional[List[Attributes]] = None
    availability: int
    basicAttributes: Optional[list[Attributes]] = None
    categoryId: int
    deliveryTime: Optional[DeliveryTime] = None
    descriptions: Descriptions
    goods: list
    isActive: bool
    numericAttributes: List[Attributes]
    postPaymentMessage: Optional[str] = None
    price: str
    subCategoryId: int
    type: str
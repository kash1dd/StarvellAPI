from pydantic import BaseModel, Field
from typing import List, Optional

from StarvellAPI.models.offer_fields import Attributes
from StarvellAPI.models.order import DeliveryTime, Descriptions

class BaseConfig(BaseModel):
    class Config:
        validate_by_name = True

class CreateLotFields(BaseModel):
    attributes: List[Attributes] = None
    availability: int
    basicAttributes: list[Attributes] = None
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
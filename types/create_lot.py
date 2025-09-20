from pydantic import BaseModel

from .offer_fields import Attributes, DeliveryTime, Descriptions

class BaseConfig(BaseModel):
    class Config:
        validate_by_name = True

class CreateLotFields(BaseModel):
    attributes: list[Attributes] | None = None
    availability: int
    basicAttributes: list[Attributes] | None = None
    categoryId: int
    deliveryTime: DeliveryTime | None = None
    descriptions: Descriptions
    goods: list
    isActive: bool
    numericAttributes: list[Attributes]
    postPaymentMessage: str | None = None
    price: str
    subCategoryId: int
    type: str
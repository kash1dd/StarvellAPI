from pydantic import BaseModel, Field

from .order import SubCategory, Descriptions

class BaseConfig(BaseModel):
    class Config:
        validate_by_name = True

class OfferInfoShortCut(BaseConfig):
    id: int
    price: float
    attributes: list[str] | None
    sub_category: SubCategory = Field(alias="subCategory")
    quantity: int = Field(alias="availability")
    descriptions: Descriptions
    is_auto_delivery: bool = Field(alias="instantDelivery")
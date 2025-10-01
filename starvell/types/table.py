from pydantic import BaseModel, Field

from starvell.types.order import Descriptions, SubCategory
from starvell.types import User


class OfferShortCut(BaseModel):
    id: int
    price: str
    descriptions: Descriptions
    availability: int
    auto_delivery: bool = Field(alias="instantDelivery")
    user: User
    sub_category: SubCategory | None = Field(alias="subCategory")
